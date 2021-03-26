class Triple:
    def __init__ (self, line_triple):
        """breaks down each input triple into subject, property, object"""
        self.subj = line_triple.split(' | ')[0]
        self.prop = line_triple.split(' | ')[1]
        self.obj = line_triple.split(' | ')[2]

    def get_triple(self):
        return "{} | {} | {}".format(self.subj, self.prop, self.obj)
