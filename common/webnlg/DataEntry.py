from common.webnlg.Triple import Triple


class DataEntry:
    def __init__ (self, gem_id, category, triples, references, target, webnlg_id):
        """to store all input data and access all parts when building the output file"""
        self.gem_id = gem_id
        self.category = category
        self.triple_list = []
        for instance_triple in triples:
            triple = Triple(instance_triple)
            self.triple_list.append(triple)
        self.input_size = len(triples)
        self.references = references
        self.target = target
        self.webnlg_id = webnlg_id

    def generate_entry_dict(self):
        input_list = [a_triple.get_triple() for a_triple in self.triple_list]

        return {
            "category": self.category,
            "gem_id": self.gem_id,
            "input": input_list,
            "references": self.references,
            "target": self.target,
            "webnlg_id": self.webnlg_id
        }