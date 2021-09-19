from functools import partial

import numpy as np
import torch
import torch.nn.functional as F

"""
    Note: This codebase is based upon, adapted and refactored from code
    from this repository:
    https://github.com/martiansideofthemoon/style-transfer-paraphrase

"""


def _beam_search(
    model,
    length,
    context,
    segments,
    eos_token_id,
    beam_size: int = 1,
    beam_search_scoring="normalize",
):
    """
    Performs a beam search.

    Args:
        model: The GPT2-model loaded and used.
        length: The length of the desired output.
        context: The sentence encoded, for which we generate output.
        segments: The segments of the context.
        eos_token_id: The id of the end of sentence token.
        beam_size: The size of the beam.
        beam_search_scoring: The scoring function to use. If set to "normalize" (which is default), the score is normalized.
    """

    def merge_pasts(all_beams, prev_past):
        past_indices = [
            beam["past"] for element in all_beams for beam in element
        ]
        return [pp[:, past_indices, :, :, :] for pp in prev_past]

    def merge_input_ids(all_beams):
        input_ids = [
            beam["sequence"][-1] for element in all_beams for beam in element
        ]
        return torch.cat(input_ids, dim=0)

    __score_fn = partial(
        _score_fn, length_normalize=(beam_search_scoring == "normalize")
    )

    if length is None:
        new_length = 1024 - context.shape[1]
    else:
        new_length = length

    with torch.no_grad():

        logits, past = model(input_ids=context, token_type_ids=segments)

        log_probs = F.log_softmax(logits[:, -1, :], dim=-1)
        top_scores, top_indices = torch.topk(
            input=log_probs, k=beam_size, dim=-1
        )

        all_beams = []
        for elem_num, (ts, ti) in enumerate(zip(top_scores, top_indices)):
            curr_element = []
            for bs in range(beam_size):
                curr_element.append(
                    {
                        "score": ts[bs],
                        "past": elem_num,
                        "sequence": [
                            x.unsqueeze(0).unsqueeze(0)
                            for x in context[elem_num]
                        ]
                        + [ti[bs].unsqueeze(0).unsqueeze(0)],
                        "eos_emitted": False,
                    }
                )
            all_beams.append(curr_element)

        # one time step here since segment IDs remain constant during generation
        tiled_segments = torch.cat(
            [segments[:, -1:] for _ in range(beam_size)], dim=-1
        )

        for _ in range(1, new_length):
            # check if all beams have emitted an EOS token
            all_eos = all(
                [
                    beam["eos_emitted"]
                    for element in all_beams
                    for beam in element
                ]
            )
            if all_eos:
                break

            latest_input_ids = merge_input_ids(all_beams)
            past = merge_pasts(all_beams, past)

            logits, past = model(
                input_ids=latest_input_ids,  # input_ids[:, -1:],
                token_type_ids=tiled_segments,
                past=past,
            )
            log_probs = F.log_softmax(logits[:, -1, :], dim=-1)
            top_scores, top_indices = torch.topk(
                input=log_probs, k=beam_size, dim=-1
            )

            new_beams = []
            curr_element = []
            for mb_num, (ts, ti) in enumerate(zip(top_scores, top_indices)):
                current_elem_num = mb_num // beam_size
                current_elem_beam_num = mb_num % beam_size
                old_beam = all_beams[current_elem_num][current_elem_beam_num]

                if old_beam["eos_emitted"]:
                    curr_element.append(old_beam)
                else:
                    for bs in range(beam_size):
                        token = ti[bs].unsqueeze(0).unsqueeze(0)
                        curr_element.append(
                            {
                                "score": old_beam["score"] + ts[bs],
                                "past": mb_num,
                                "sequence": old_beam["sequence"] + [token],
                                "eos_emitted": token.item() == eos_token_id,
                            }
                        )
                if current_elem_beam_num == beam_size - 1:
                    new_beams.append(curr_element)
                    curr_element = []

            # Sort the beams by score and keep only top scoring elements
            all_beams = []
            for elem in new_beams:
                elem.sort(key=lambda x: __score_fn(x), reverse=True)
                all_beams.append(elem[:beam_size])

        final_beams = []
        for elem in all_beams:
            elem.sort(key=lambda x: __score_fn(x), reverse=True)
            # just return the highest scoring prediction
            final_beams.append(elem[:1])

        final_input_ids = [
            torch.cat(elem[0]["sequence"], dim=1).squeeze(0)
            for elem in final_beams
        ]
        return final_input_ids


def _top_k_top_p_filtering(
    logits, top_k=0, top_p=0.0, filter_value=-float("Inf")
):
    """Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
    Args:
        logits: logits distribution shape (batch size x vocabulary size)
        top_k > 0: keep only top k tokens with highest probability (top-k filtering).
        top_p > 0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
            Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
    From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(
            F.softmax(sorted_logits, dim=-1), dim=-1
        )
        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
            ..., :-1
        ].clone()
        sorted_indices_to_remove[..., 0] = 0

        # scatter sorted tensors to original indexing
        indices_to_remove = sorted_indices_to_remove.scatter(
            dim=1, index=sorted_indices, src=sorted_indices_to_remove
        )
        logits[indices_to_remove] = filter_value

    elif top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = (
            logits < torch.topk(logits, top_k)[0][..., -1, None]
        )
        logits[indices_to_remove] = filter_value

    return logits


def _sample_sequence(
    model,
    length: int,
    context: torch.Tensor,
    segments,
    eos_token_id,
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: int = 0.0,
):
    """
    Samples a sequence of a given length from a given context.

    Args:
        model: model to use to sample (the GPT2 model)
        length: length of the sequence to sample


    """
    if length is None:
        new_length = 1024 - context.shape[1]
    else:
        new_length = length

    batch_size = context.shape[0]
    eos_emitted = [False for _ in range(batch_size)]
    generated = context

    with torch.no_grad():
        past = None
        for i in range(new_length):
            pred__ = (
                model(
                    input_ids=generated,
                    token_type_ids=segments,
                    return_dict=True,
                )
                if i == 0
                else model(
                    input_ids=generated[:, -1:],
                    token_type_ids=segments[:, -1:],
                    past_key_values=past,
                    return_dict=True,
                )
            )
            logits = pred__["logits"]
            past = pred__["past_key_values"]
            next_token_logits = logits[:, -1, :] / (
                temperature if temperature > 0 else 1.0
            )
            filtered_logits = _top_k_top_p_filtering(
                next_token_logits, top_k=top_k, top_p=top_p
            )
            do_greedy = temperature == 0 and top_k in [0, 1] and top_p == 0.0
            next_token = (
                torch.argmax(filtered_logits, dim=-1).unsqueeze(-1)
                if do_greedy
                else torch.multinomial(
                    F.softmax(filtered_logits, dim=-1), num_samples=1
                )
            )
            generated = torch.cat((generated, next_token), dim=1)
            segments = torch.cat((segments, segments[:, -1:]), dim=1)

            for batch_elem in range(batch_size):
                if next_token[batch_elem].item() == eos_token_id:
                    eos_emitted[batch_elem] = True

            if length is None and all(eos_emitted):
                break
    return generated


def _score_fn(x, length_normalize):
    if length_normalize:
        return x["score"] / len(x["sequence"])
    else:
        return x["score"]


class Instance(object):
    """
    Instance of a sentence to generate a paraphrase for.

    Args:
        args: Standard, default arguments to use.
        config : configurations specified.
        instance_dict : dictionary containing the sentence to paraphrase.

    """

    def __init__(self, args, config, instance_dict):
        self.dict = instance_dict
        self.args = args
        self.config = config
        self.truncated = False
        self.sent1_tokens = np.array(
            instance_dict["sent1_tokens"], dtype=np.int32
        )
        self.sent2_tokens = np.array(
            instance_dict["sent2_tokens"], dtype=np.int32
        )
        self.init_context_size = config["max_prefix_length"] + 1

    def preprocess(self, tokenizer):
        self.truncate()
        self.build_sentence(tokenizer)
        self.build_segment(tokenizer)

    def truncate(self):
        config = self.config
        max_prefix_length = config["max_prefix_length"]
        max_suffix_length = config["max_suffix_length"]
        if len(self.sent1_tokens) > max_prefix_length:
            self.truncated = True
            self.sent1_tokens = self.sent1_tokens[:max_prefix_length]
        if len(self.sent2_tokens) > max_suffix_length:
            self.truncated = True
            self.sent2_tokens = self.sent2_tokens[:max_suffix_length]

    def build_sentence(self, tokenizer):
        tokens_to_pad = self.config["max_prefix_length"] - len(
            self.sent1_tokens
        )
        self.sent_prefix = np.pad(
            self.sent1_tokens,
            (tokens_to_pad, 0),
            constant_values=tokenizer.pad_token_id,
        )

        self.sent_suffix = self.right_padding(
            np.append(self.sent2_tokens, tokenizer.eos_token_id),
            tokenizer.pad_token_id,
            self.config["max_suffix_length"] + 1,
        )
        self.sentence = np.concatenate(
            [self.sent_prefix, [tokenizer.bos_token_id], self.sent_suffix]
        )

    def right_padding(self, data, pad_token, total_length):
        tokens_to_pad = total_length - len(data)
        return np.pad(data, (0, tokens_to_pad), constant_values=pad_token)

    def build_segment(self, tokenizer):
        prefix_segment = [
            tokenizer.additional_special_tokens_ids[1]
            for _ in self.sent_prefix
        ]
        suffix_segment_tag = tokenizer.additional_special_tokens_ids[2]
        self.segment = np.concatenate(
            [
                [],
                prefix_segment,
                [suffix_segment_tag],
                [suffix_segment_tag for _ in self.sent_suffix],
            ]
        ).astype(np.int64)
