NON_TERMINALS = [
    "S",
    "SBAR",
    "SQ",
    "SBARQ",
    "SINV",
    "ADJP",
    "ADVP",
    "CONJP",
    "FRAG",
    "INTJ",
    "LST",
    "NAC",
    "NP",
    "NX",
    "PP",
    "PRN",
    "QP",
    "RRC",
    "UCP",
    "VP",
    "WHADJP",
    "WHAVP",
    "WHNP",
    "WHPP",
    "WHADVP",
    "X",
    "ROOT",
    "NP-TMP",
    "PRT",
]


class Token(object):
    def __init__(self, word, idx):
        self.word = word
        self.idx = idx

    def __repr__(self):
        return repr(self.word)


class Node(object):
    def __init__(self):
        self.root = False
        self.children = []
        self.label = None
        self.parent = None
        self.phrase = ""
        self.terminal = False
        self.start_idx = 0
        self.end_idx = 0


class Sentence(object):
    def __init__(self, parse_string):
        self.num_nodes = 0
        self.tree = self.get_tree(parse_string)
        self.sent = self.tree.phrase

        tokens = {}
        for idx, tok in enumerate(self.tree.phrase.split(" ")):
            tokens[idx] = Token(tok, idx)
        self.tokens = tokens
        self.num_tokens = len(tokens)

    def get_tree(self, parse_string):
        tree = self.contruct_tree_from_parse(parse_string, None)
        tree = self.reduce_tree(tree)
        phrase_whole = self.assign_phrases(tree, 0)
        tree.phrase = phrase_whole
        tree.start_idx = 0
        tree.end_idx = len(phrase_whole.split(" "))
        tree.parent_idx = -1
        self.assign_ids(tree)
        return tree

    def assign_ids(self, tree):
        tree.idx = self.num_nodes
        self.num_nodes += 1

        for child in tree.children:
            child.parent_idx = tree.idx
            self.assign_ids(child)

    @staticmethod
    def get_subtrees(parse_txt_partial):
        parse_txt_partial = parse_txt_partial[1:-1]
        if "(" in parse_txt_partial:
            idx_first_lb = parse_txt_partial.index("(")
            name_const = parse_txt_partial[:idx_first_lb].strip()
            parse_txt_partial = parse_txt_partial[idx_first_lb:]
            count = 0
            partition_indices = []
            for idx in range(len(parse_txt_partial)):
                if parse_txt_partial[idx] == "(":
                    count += 1
                elif parse_txt_partial[idx] == ")":
                    count -= 1
                if count == 0:
                    partition_indices.append(idx + 1)

            partitions = []
            part_idx_prev = 0
            for i, part_idx in enumerate(partition_indices):
                partitions.append(parse_txt_partial[part_idx_prev:part_idx])
                part_idx_prev = part_idx
        else:
            temp = parse_txt_partial.split(" ")
            name_const = temp[0]
            partitions = [temp[1]]

        return name_const, partitions

    # constructs constituency tree from the parse string
    @staticmethod
    def contruct_tree_from_parse(parse_txt, node):

        if parse_txt.startswith("("):
            phrase_name, divisions = Sentence.get_subtrees(parse_txt)

            if node is None:
                node = Node()
                node.root = True

            node.label = phrase_name

            if phrase_name in NON_TERMINALS:
                for phrase in divisions:
                    if phrase.strip() == "":
                        continue
                    node_temp = Node()
                    node_temp.parent = node
                    node.children.append(
                        Sentence.contruct_tree_from_parse(phrase, node_temp)
                    )
            else:
                node.terminal = True
                node.phrase = divisions[0]

        return node

    # only used for debugging
    @staticmethod
    def print_tree(tree):
        print(tree.label)
        print(tree.phrase)
        print(tree.start_idx)
        print(tree.end_idx)
        for child in tree.children:
            Sentence.print_tree(child)

    # remove single child nodes
    @staticmethod
    def reduce_tree(tree):
        while len(tree.children) == 1:
            tree = tree.children[0]
        children = []
        for child in tree.children:
            child = Sentence.reduce_tree(child)
            children.append(child)
        tree.children = children
        return tree

    @staticmethod
    def assign_phrases(tree, phrase_start_idx):
        if tree.terminal:
            tree.start_idx = phrase_start_idx
            tree.end_idx = phrase_start_idx + len(
                tree.phrase.strip().split(" ")
            )
            return tree.phrase
        else:
            phrase = ""
            phrase_idx_add = 0
            for child in tree.children:
                child_phrase = Sentence.assign_phrases(
                    child, phrase_start_idx + phrase_idx_add
                ).strip()
                child.start_idx = phrase_start_idx + phrase_idx_add
                phrase_idx_add += len(child_phrase.strip().split(" "))
                child.end_idx = phrase_start_idx + phrase_idx_add
                child.phrase = child_phrase
                phrase += " " + child_phrase
                phrase = phrase.strip()
            return phrase
