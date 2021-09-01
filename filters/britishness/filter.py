import json
import re

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
from initialize import spacy_nlp
import spacy


class BritishnessFilter(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]

    def __init__(self, britwords_required=1):
        super().__init__()
        self.britwords_required = britwords_required
        # self.keywords = keywords
        # self.nlp = spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")

    def filter(self, sentence: str = None) -> bool:
        britwords = get_britwords()

        num_britwords = 0
        for bword in britwords:
            num_britwords += len(re.findall("(?<![a-zA-Z])"+bword+"(?![a-zA-Z])", sentence))
            num_britwords += len(re.findall("(?<![a-zA-Z])"+bword[0].upper()+bword[1:]+"(?![a-zA-Z])", sentence))

        return (num_britwords >= self.britwords_required)

def get_britwords():
    britwords = []

    spelling_json_file = open('filters/britishness/spelling_map.json')
    spelling_map = json.load(spelling_json_file)

    britwords += spelling_map.values()

    vocab_map = {'Scotch tape': 'sellotape',
     'a little': 'a tad',
     'a look': 'a gander',
     'angry': 'cheesed off',
     'asylum': 'nuthouse',
     'attorney': 'barrister',
     'baby carriage': 'pram',
     'bathroom': 'loo',
     'boss': 'gaffer',
     'broken': 'knackered',
     'call collect': 'reverse charges',
     'cat': 'moggy',
     'checkers': 'draughts',
     'cigarette': 'fag',
     'corn': 'maize',
     'cuffs': 'turn-ups',
     'curb': 'kerb',
     'customer': 'punter',
     'cutlery': 'eating irons',
     'dangerous': 'dodgy',
     'desirable': 'jammy',
     'diaper': 'nappy',
     'difficult': 'dodgy',
     'disgusted': 'cheesed off',
     'dish-towel': 'tea-towel',
     'divided highway': 'dual carriageway',
     'drug store': "chemist's",
     'drunk': 'gassed',
     'eavesdrop': 'earwig',
     'employer': 'gaffer',
     'engineer': 'engine driver',
     'English muffin': 'crumpet',
     'excellent': 'corking',
     'exhausted': 'knackered',
     'fed up': 'cheesed off',
     'fool': 'prat',
     'foolish': 'moony',
     'foreman': 'gaffer',
     'freeway': 'motorway',
     'funds': 'lolly',
     'gambler': 'punter',
     'garbage': 'rubbish',
     'garbage can': 'rubbish-bin',
     'garbage collector': 'dustman',
     'garbageman': 'dustman',
     'gasoline': 'petrol',
     'gear-shift': 'gear-lever',
     'generator': 'dynamo',
     'handcuffs': 'darbies',
     'house': 'gaff',
     'kitten': 'moggy',
     'lavatory': 'loo',
     'lies': 'porkies',
     'liquor store': 'off-license',
     'lucky': 'jammy',
     'mail carrier': 'postman',
     'mailbox': 'postbox',
     'mailman': 'postman',
     'man': 'bloke',
     'math': 'maths',
     'money': 'lolly',
     'moron': 'pillock',
     'mouth': 'gob',
     'nonsense': 'codswallop',
     'nose': 'hooter',
     'nothing': 'nowt',
     'odds and ends': 'odds and sods',
     'offended': 'miffed',
     'oil pan': 'sump',
     'old man': 'geezer',
     'optometrist': 'optician',
     'outstanding': 'corking',
     'patron': 'punter',
     'pavement': 'road surface',
     'pleasant': 'jammy',
     'potato chips': 'potato crisps',
     'railroad': 'railway',
     'railway car': 'railway carriage',
     'raincoat': 'mackintosh',
     'schedule': 'timetable',
     'sedan': 'saloon',
     'shopper': 'punter',
     'sneakers': 'gym shoes',
     'spat': 'gobbed',
     'spool of thread': 'reel of cotton',
     'stroller': 'push-chair',
     'subway': 'underground railway',
     'sucker': 'punter',
     'teeth': 'ivories',
     'the brakes': 'the anchors',
     'the movies': 'the cinema',
     'the police': 'the fuzz',
     'thumbtack': 'drawing pin',
     'tired': 'knackered',
     'trash': 'rubbish',
     'trash can': 'rubbish-bin',
     'trashcan': 'rubbish-bin',
     'truck': 'lorry',
     'turnpike': 'toll motorway',
     'upset': 'miffed',
     'vacation': 'holiday',
     'vacuum cleaner': 'hoover',
     'windshield': 'windscreen',
     'wrench': 'spanner'
    }

    britwords += vocab_map.values()

    britslang = ['tosser', 'blimey', 'wanker', 'chuffed', 'sod off', 'wonky', 'whinge', 'tenner', 'fiver', 'quid', 'toff', 'skive', 'scouse', 'scouser', 'cockney', 'nicked', 'nutter', 'gobsmacked', 'chap', 'bugger', 'anticlockwise', 'anti-clockwise', 'nosh', 'bollocks', 'ponce', 'bangers', 'telly', 'knickers', 'uni', 'albion', 'chunder', 'fortnight', 'grockel', 'kerfuffle', 'scrummy']
    britwords += britslang

    return set(britwords)
