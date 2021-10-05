import itertools
import random
import os
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import jieba
from transformers import (AutoTokenizer, pipeline, AutoModelForTokenClassification)

def chinese_person_named_entities_gender(text,
                                         prob,
                                         seed,
                                         max_outputs,
                                         gender_change,
                                         chinese_names_data
                                         ):
    random.seed(seed)

    tokenizer = AutoTokenizer.from_pretrained('uer/roberta-base-finetuned-cluener2020-chinese')
    model = AutoModelForTokenClassification.from_pretrained('uer/roberta-base-finetuned-cluener2020-chinese')

    ner = pipeline('ner', model=model, tokenizer=tokenizer)
    output = ner(text)
    names_in_text = []
    name = ""
    pronoun_change = ""
    for entity_dict in output:
        if entity_dict['entity'] == 'B-name':
            if(len(name) > 0):
                names_in_text.append(name)
            name = entity_dict['word']
        if entity_dict['entity'] == 'I-name':
            name += entity_dict['word']
    if (len(name) > 0):
        names_in_text.append(name)

    perturbed_texts = []
    names = [chinese_names['name'] for chinese_names in chinese_names_data]
    genders = [chinese_names['gender'] for chinese_names in chinese_names_data]
    output = jieba.lcut(text)

    for _ in itertools.repeat(None, max_outputs):
        butter_text = ""
        for original_word in output:
            perturb_word_len = len(original_word)
            if (perturb_word_len > 1 and original_word in names_in_text):
                name_index = names.index(original_word)
                gender_index = genders[name_index]

                if(gender_index == '女' and gender_change):
                    indices = [index for index, gender in enumerate(genders) if gender == '男']
                    candidate_name = [names[i] for i in indices]
                    pronoun_change = 'female_to_male'
                elif(gender_index == '男' and gender_change):
                    indices = [index for index, gender in enumerate(genders) if gender == '女']
                    candidate_name = [names[i] for i in indices]
                    pronoun_change = 'male_to_female'
                else:
                    indices = [index for index, gender in enumerate(genders) if gender == gender_index]
                    candidate_name = [names[i] for i in indices]
                if random.random() <= prob:
                    new_chinese_character = random.choice(candidate_name)
            else:
                new_chinese_character = original_word

            butter_text += new_chinese_character

        if(pronoun_change == 'female_to_male'):
            butter_text = butter_text.replace('她','他')
        elif(pronoun_change == 'male_to_female'):
            butter_text = butter_text.replace('他','她')
        perturbed_texts.append(butter_text)

    return perturbed_texts


def load_chinese_names_data():
    dirname = os.path.dirname(__file__)
    names_list = []

    with open(os.path.join(dirname, 'Chinese_Names_Corpus_Gender（120W）.txt'), mode='r') as file:
        lines = file.readlines()
        for line in lines:
            if(line.rstrip() != ""):
                names_dict = {}
                name = line.split(",")
                names_dict["name"] = name[0]
                names_dict["gender"] = name[1].rstrip()
                names_list.append(names_dict)

    return names_list


"""
Chinese Person Named Entities and Gender Perturbation
"""

class ChinesePersonNamedEntitiesAndGender(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION
    ]
    languages = ["zh"]
    keywords = ["lexical",
                "rule-based",
                "model-based",
                "transformer-based",
                "external-knowledge-based",
                "tokenizer-required",
                "written",
                "highly-precision"]

    def __init__(self, seed=0, max_outputs=1, prob=1):
        super().__init__(seed, max_outputs=max_outputs)
        self.prob = prob
        self.seed = seed
        self.max_outputs = max_outputs
        self.chinese_names_data = load_chinese_names_data()

    def generate(self, sentence: str, seed: int = 0, gender_change: bool = True):
        perturbed_texts = chinese_person_named_entities_gender(
            text=sentence,
            prob=self.prob,
            seed=seed,
            max_outputs=self.max_outputs,
            gender_change=gender_change,
            chinese_names_data=self.chinese_names_data
        )
        return perturbed_texts
"""
if __name__ == '__main__':
    text = "阿朝只有初中文化程度,担任这样的复杂工种是比较吃力的,但他边干边学,终于胜任了。"
    perturb_func = ChinesePersonNamedEntitiesAndGender()
    new_text = perturb_func.generate(text, seed=42, gender_change=True)
    print(new_text)
"""


