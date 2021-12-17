import copy
import itertools
import string

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from torch.nn.functional import log_softmax
from torchtext.vocab import GloVe
from transformers import BartForConditionalGeneration, BartTokenizer

TAGS_TO_IGNORE = [
    "DT",
    "IN",
    "CD",
    "MD",
    "TO",
    "PRP",
    "PRP$",
    "RB",
    "FW",
    "POS",
]


def get_parent_trajectory(nodes, idx):
    if idx == -1:
        return []
    else:
        parent_idx = nodes[idx].parent_idx
        parents = get_parent_trajectory(nodes, parent_idx)
        parents = [parent_idx] + parents
        return parents


def get_common_parent(nodes, n1, n2):
    parents1 = get_parent_trajectory(nodes, n1)
    parents2 = get_parent_trajectory(nodes, n2)
    for i, p in enumerate(parents1):
        if p in parents2:
            break
    common_parents = parents1[i:]
    return common_parents


def get_all_nodes(tree):
    nodes = [tree]
    for child in tree.children:
        child_list = get_all_nodes(child)
        nodes += child_list
    return nodes


def get_candidate_node_pairs(sentence_parsed):
    nodes = get_all_nodes(sentence_parsed.tree)
    tree = {}
    node_pairs = list(itertools.combinations(range(0, len(nodes)), 2))

    for n1_idx, n2_idx in node_pairs:
        n1 = nodes[n1_idx]
        n2 = nodes[n2_idx]

        # reject if one is subset of another
        if n1.start_idx in range(
            n2.start_idx, n2.end_idx
        ) or n2.start_idx in range(n1.start_idx, n1.end_idx):
            continue

        # ignore if punctuation or trivial abstractions
        if n1.label in TAGS_TO_IGNORE + list(
            string.punctuation
        ) or n2.label in TAGS_TO_IGNORE + list(string.punctuation):
            continue

        parent = get_common_parent(nodes, n1_idx, n2_idx)

        pa = nodes[parent[0]].phrase
        pa_size = len(pa.split())
        n1_size = len(n1.phrase.split())
        n2_size = len(n2.phrase.split())

        # reject if too sparse or too dense
        num_nr = pa_size - (n1_size + n2_size)
        if num_nr > pa_size / 1.7 or num_nr <= 1:
            continue

        if parent[0] in tree.keys():
            tree[parent[0]].append((n1_idx, n2_idx))
        else:
            tree[parent[0]] = [(n1_idx, n2_idx)]

    return nodes, tree


def remove_duplicates(ordered_list):
    if len(ordered_list) == 1:
        return ordered_list

    new_list = []
    all_reorderings = []
    for i, (w_, x_, y_, z_) in enumerate(ordered_list):
        if y_ in all_reorderings:
            continue
        else:
            new_list.append((w_, x_, y_, z_))
            all_reorderings.append(y_)

    return new_list


# given abstracted phrase e.g. if X then Y, and ordering within abstracted phrases X and Y,
# returns ordering for non-abstracted/expanded phrase
def get_global_order(order, loc_x, loc_y, order_x, order_y):
    if loc_x < loc_y:
        loc_y += len(order_x) - 1

    def expand_order(order, loc, order_subphrase_local):
        order_subphrase_global = [
            x + order[loc] for x in order_subphrase_local
        ]
        for idx, idx_order in enumerate(order):
            if idx_order > order[loc]:
                order[idx] += max(order_subphrase_local)
        order = order[:loc] + order_subphrase_global + order[loc + 1 :]
        return order

    order = expand_order(order, loc_x, order_x)
    order = expand_order(order, loc_y, order_y)

    return order


class sowModel(object):
    def __init__(self, model_path, max_outputs):
        self.sow = BartForConditionalGeneration.from_pretrained(model_path)
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
        self.sow
        self.glove = GloVe(name="6B", dim=50)
        self.max_outputs = max_outputs

    def get_reorderings(self, sentence):

        nodes, tree = get_candidate_node_pairs(sentence)
        if len(tree) == 0:
            return []

        minkey = min(list(tree.keys()))
        node_outputs = {}
        reorderings, _ = self.get_reordering_at_node(
            sentence, nodes, tree, minkey, node_outputs
        )

        reorderings_stage2 = []
        for r in reorderings:
            if len(r[1]) > 3:
                continue
            order = r[2]
            reordered_sent = r[0]
            input = sentence.sent
            if input != nodes[minkey].phrase:
                preceeding_count = nodes[minkey].start_idx
                following_count = (
                    len(input.split()) - len(order) - preceeding_count
                )
                order = [x + preceeding_count for x in order]
                order = list(range(preceeding_count)) + order
                order = order + list(
                    range(max(order) + 1, max(order) + 1 + following_count)
                )
                reordered_sent = (
                    " ".join(input.split()[:preceeding_count])
                    + " "
                    + reordered_sent
                )
                reordered_sent += " " + " ".join(
                    input.split()[-following_count:]
                )
            scores = r[3]
            if len(scores) == 0:
                scores = [0]
            reorderings_stage2.append((reordered_sent, r[1], order, scores))
        reorderings_stage2.sort(key=lambda x: np.mean(x[3]), reverse=True)
        reorderings_stage2 = remove_duplicates(reorderings_stage2)[
            1 : self.max_outputs + 1
        ]
        return reorderings_stage2

    def generate_and_score(self, input):
        encoding = self.tokenizer.encode_plus(input, return_tensors="pt")
        input_ids, attention_masks = (
            encoding["input_ids"],
            encoding["attention_mask"],
        )

        input_args = {
            "input_ids": input_ids,
            "attention_mask": attention_masks,
            "num_beams": 1,
            "length_penalty": 1,
            "no_repeat_ngram_size": 1,
            "max_length": 40,
            "min_length": 0,
            "decoder_start_token_id": self.tokenizer.bos_token_id,
            "num_return_sequences": 1,
            "output_scores": True,
            "return_dict_in_generate": True,
        }

        generation = self.sow.generate(**input_args)
        reordering = self.tokenizer.decode(
            generation.sequences[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )

        score = 0.0
        for idx, gen_idx in enumerate(generation.sequences[0]):
            if idx == 0:
                continue
            score += (
                log_softmax(generation.scores[idx - 1], dim=1)[0, gen_idx]
                .cpu()
                .numpy()
            )
        return reordering.strip(), score

    def encode_single_sentence(self, phrase):

        monotone_input_text = f"0 {phrase}"
        reorder_input_text = f"1 {phrase}"

        _, monotone_score = self.generate_and_score(monotone_input_text)
        reordering, reordering_score = self.generate_and_score(
            reorder_input_text
        )
        if "X" not in reordering or "Y" not in reordering:
            return None, None, None

        return reordering, reordering_score, monotone_score

    def abstract_chosen_subtrees(self, p, childen):
        phrase = p.phrase.split(" ")
        phrase_without_label = copy.deepcopy(phrase)

        c1_replacement = f"<{childen[0].label}> X"
        c2_replacement = f"<{childen[1].label}> Y"
        for i, c in enumerate(childen):
            start_idx = c.start_idx - p.start_idx
            end_idx = start_idx + c.end_idx - c.start_idx

            if i == 0:
                phrase[start_idx] = c1_replacement
                phrase_without_label[start_idx] = "X"
            else:
                phrase[start_idx] = c2_replacement
                phrase_without_label[start_idx] = "Y"

            for j in range(start_idx + 1, end_idx):
                phrase[j] = None
                phrase_without_label[j] = None

        phrase = " ".join([p for p in phrase if p is not None])
        phrase_without_label = " ".join(
            [p for p in phrase_without_label if p is not None]
        )
        return phrase, phrase_without_label

    def get_alignment(self, input, output):
        input = input.split()
        output = output.split()

        embed1 = self.glove.get_vecs_by_tokens(input)
        embed2 = self.glove.get_vecs_by_tokens(output)

        mat = cosine_similarity(embed1, embed2)
        mat[input.index("X"), output.index("X")] = 1
        mat[input.index("Y"), output.index("Y")] = 1
        alignments = list(np.argmax(mat, axis=1))
        alignments = list(np.argsort(np.argsort(alignments)))

        return alignments, input.index("X"), input.index("Y")

    def get_subphrase_reordering(self, parent, n1, n2):
        phrase, phrase_without_label = self.abstract_chosen_subtrees(
            parent, [n1, n2]
        )

        (
            reordered_output,
            reordering_score,
            monotone_score,
        ) = self.encode_single_sentence(phrase)
        if reordered_output is None:
            return None, None, monotone_score, phrase_without_label, None
        alignment = self.get_alignment(phrase_without_label, reordered_output)

        # reordered_output_best_score -= monotone_best_score
        return (
            reordered_output,
            reordering_score,
            monotone_score,
            phrase_without_label,
            alignment,
        )

    def get_reordering_at_node(self, sent, nodes, tree, key, node_outputs):
        outputs_final = []

        list_to_prune = []
        input_phrase = sent.sent.split()[
            nodes[key].start_idx : nodes[key].end_idx
        ]
        input_phrase = " ".join(input_phrase)

        for (n1_idx, n2_idx) in tree[key]:
            (
                output,
                score,
                mono_score,
                input_rule,
                order,
            ) = self.get_subphrase_reordering(
                nodes[key], nodes[n1_idx], nodes[n2_idx]
            )
            if output is None:
                continue
            output_phrase = output.replace(
                "X", nodes[n1_idx].phrase.strip()
            ).replace("Y", nodes[n2_idx].phrase.strip())
            list_to_prune.append(
                [
                    output,
                    score,
                    mono_score,
                    input_rule,
                    input_phrase,
                    output_phrase,
                    order,
                    n1_idx,
                    n2_idx,
                ]
            )

        pruned_list = prune_list_of_candidates(list_to_prune, input_phrase)

        for (
            output,
            score,
            mono_score,
            input_rule,
            input_phrase,
            _,
            order,
            n1_idx,
            n2_idx,
        ) in pruned_list:
            output1 = []
            output2 = []
            if n1_idx in tree.keys():
                if n1_idx in node_outputs:
                    output1 = node_outputs[n1_idx]
                else:
                    output1, node_outputs = self.get_reordering_at_node(
                        sent, nodes, tree, n1_idx, node_outputs
                    )
            if n2_idx in tree.keys():
                if n2_idx in node_outputs:
                    output2 = node_outputs[n2_idx]
                else:
                    output2, node_outputs = self.get_reordering_at_node(
                        sent, nodes, tree, n2_idx, node_outputs
                    )

            if len(output1) == 0:
                l1 = len(nodes[n1_idx].phrase.split())
                output1 = [(nodes[n1_idx].phrase, [], list(range(l1)), [])]

            if len(output2) == 0:
                l2 = len(nodes[n2_idx].phrase.split())
                output2 = [(nodes[n2_idx].phrase, [], list(range(l2)), [])]

            pairs_ = itertools.product(output1, output2)

            for o1, o2 in pairs_:
                out_temp = output.replace("X", o1[0]).replace("Y", o2[0])
                rule_temp = (
                    input_phrase + "=>" + input_rule + "======>" + output
                )
                order_new = copy.deepcopy(order[0])
                order_x_idx = copy.deepcopy(order[1])
                order_y_idx = copy.deepcopy(order[2])
                order_new = get_global_order(
                    order_new, order_x_idx, order_y_idx, o1[2], o2[2]
                )
                assert len(input_phrase.split()) == len(
                    order_new
                ), "order indexing error"
                if score == 0:  # monotone
                    outputs_final.append(
                        (out_temp, o1[1] + o2[1], order_new, o1[3] + o2[3])
                    )
                else:
                    score_temp = score  # - mono_score
                    outputs_final.append(
                        (
                            out_temp,
                            [(rule_temp, score_temp)] + o1[1] + o2[1],
                            order_new,
                            o1[3] + o2[3] + [score_temp],
                        )
                    )

        node_outputs[key] = outputs_final[:10]

        return outputs_final, node_outputs


def prune_list_of_candidates(list_to_prune, input_phrase):
    output_phrases = {}
    best_mono_score = -100
    best_mono_input = ""
    n1_mono_best = None
    n2_mono_best = None
    for i, (
        _,
        score,
        mono_score,
        input_rule,
        _,
        output_phrase,
        _,
        n1_idx,
        n2_idx,
    ) in enumerate(list_to_prune):
        if output_phrase in output_phrases.keys():
            if score > output_phrases[output_phrase][0]:
                output_phrases[output_phrase] = (score, i)
        else:
            output_phrases[output_phrase] = (score, i)

        if mono_score > best_mono_score:
            best_mono_score = mono_score
            best_mono_input = input_rule
            n1_mono_best = n1_idx
            n2_mono_best = n2_idx

    pruned_list = []
    for p in output_phrases:
        pruned_list.append(list_to_prune[output_phrases[p][1]])

    if best_mono_input != "":
        mono_alignment = list(range(len(best_mono_input.split())))
        mono_alignment_x_idx = best_mono_input.split().index("X")
        mono_alignment_y_idx = best_mono_input.split().index("Y")
        alignmnent = (
            mono_alignment,
            mono_alignment_x_idx,
            mono_alignment_y_idx,
        )
        pruned_list.append(
            (
                best_mono_input,
                0,
                0,
                best_mono_input,
                input_phrase,
                input_phrase,
                alignmnent,
                n1_mono_best,
                n2_mono_best,
            )
        )
    return pruned_list
