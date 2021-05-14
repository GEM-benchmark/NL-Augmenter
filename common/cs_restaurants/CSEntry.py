class CSEntry:
    def __init__(self, entry):
        self.dialog_act = entry['dialog_act'].split('(')[0]
        self.lexicalised = self.get_components(entry['dialog_act'])
        self.delexicalised = self.get_components(entry['dialog_act_delexicalized'])

    def get_components(self, act):
        "Get components from a dialog act."
        components = dict()
        for item in act[:-1].split('(')[1].split(','):
            if item:
                if '=' in item:
                    key, value = item.split('=')
                    components[key] = value
                else:
                    components['item'] = None
        return components