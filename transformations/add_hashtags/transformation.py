from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import random
from spacy import load


def extract_dep_nodes(dep_parse, be_class_verb, subj_obj_list):
    """method for extracting VERB, NSUBJ phrase and DOBJ phrase dependency nodes"""
    verb = ""
    nsubj_phrase = []
    dobj_phrase = []
    for token in dep_parse:
        if token.dep_ == "ROOT":
            if token.text.lower() not in be_class_verb:
                verb = token.text

    for token in dep_parse:
        if token.dep_ == "dobj" and token.head.dep_ == "ROOT":
            dobj_phrase.append(token.text.title())
        elif token.dep_ == "dobj" and token.head.head.dep_ == "dobj":
            dobj_phrase.append(token.text.title())

    for token in dep_parse:
        if token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
            nsubj_phrase.append(token.text.title())
        elif token.dep_ == "nsubj" or token.head.head.dep_ == "nsubj":
            nsubj_phrase.append(token.text.title())
    return verb.title(), "".join(nsubj_phrase), "".join(dobj_phrase)


def generate_hashtag_from_noun_chunk(chunk_list, subj_obj_list):
    """method for generating hastags from noun chunks"""
    hash_tag_list = []
    if not chunk_list:
        return None
    else:
        for chunk in chunk_list:
            if chunk.lower() not in subj_obj_list:
                chunk_words = [word.title() for word in chunk.split(" ")]
                hash_tag_list.append("#"+"".join(chunk_words))
    return hash_tag_list


def extract_noun_chunks_hashtag(dep_parse, subj_obj_list):
    """Method for extracting noun chunks from dependency parse"""
    chunk_list = []
    for chunk in dep_parse.noun_chunks:
        if len(str(chunk.text.split(" ")))>0:
            chunk_list.append(chunk.text)
    return generate_hashtag_from_noun_chunk(chunk_list, subj_obj_list)


def extract_hashtags(sentence, nlp, be_class_verb, subj_obj_list):
    # method for gathering all hashtags
    dep_parse = nlp(sentence)
    verb, nsubj, dobj = extract_dep_nodes(dep_parse, be_class_verb, subj_obj_list)
    hash_tag_list = []
    for dep_n in [verb, nsubj, dobj]:
        if(dep_n != ""):
            hash_tag_list.append("#"+dep_n)
    if verb != "" and dobj != "":
        hash_tag_list.append("#"+verb+dobj)
    noun_chunks_hashtags = extract_noun_chunks_hashtag(dep_parse, subj_obj_list)
    if noun_chunks_hashtags is not None:
        hash_tag_list.extend(noun_chunks_hashtags) # merging both hashtag list
        return verb, list(set(hash_tag_list))
    return verb, hash_tag_list


def get_hash_tags(sentence, be_class_verb, subj_obj_list, seed=0, max_outputs=1, nlp=None):
    """method for appending hashtags to sentence"""
    verb, hashtag_list = extract_hashtags(sentence, nlp, be_class_verb, subj_obj_list)
    #random.seed(seed)
    # num = random.randint(1, len(hashtag_list))
    # print(num)
    # selected_hastags = random.sample(hashtag_list, num)
    # print(selected_hastags)
    # trans_sentence = sentence + " ".join(selected_hastags)
    # # if bool(random.getrandbits(1)):
    # #     trans_sentence = sentence + "".join(selected_hastags)
    # # else:
    # #     trans_sentence = sentence + " ".join(selected_hastags)
    # return trans_sentence

    transformation_list = []
    #random.seed(0)
    for _ in range(max_outputs):
        num = random.randint(1, len(hashtag_list))
        selected_hastag = random.sample(hashtag_list, num)
        print(hashtag_list[:5], "*****")
        print(num)
        print(selected_hastag)
        trans_sent = sentence + " ".join(selected_hastag)
        transformation_list.append(trans_sent)
        # if bool(random.getrandbits(1)):
        #     transformation_list.append(sentence + " " + " ".join(selected_hastag))
        # else:
        #     transformation_list.append(sentence + "".join(selected_hastag))
    return transformation_list


class HashtagGeneration(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.SENTIMENT_ANALYSIS,
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=1):
        super().__init__(seed)
        self.max_outputs=max_outputs
        self.nlp = load('en_core_web_sm')
        self.be_class_verb = ["is", "am", "are", "was", "were", "will", "shall"]
        self.subj_obj_list = ["i", "you", "we", "they", "he", "she"]

    def generate(self, sentence: str):
        transformed_sentences = get_hash_tags(sentence, self.be_class_verb, self.subj_obj_list,
                                            self.seed, self.max_outputs, self.nlp)
        return transformed_sentences


if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = HashtagGeneration()
    test_cases = []
    input_sent = ["I love domino's pizza .",
                  #"Virat Kohli made a big hundred against Australian team .",
                  #"Many people like T20 cricket these days .",
                  #"Attention is all you need .",
                  #"Natural Language Processing research is awesome ."
                ]

    # for i,sentence in enumerate(input_sent):
    #     transformed_sentence = tf.generate(sentence)
    #     test_cases.append({
    #                 "class": tf.name(),
    #                 "inputs": {"sentence": sentence},
    #                 "outputs": [],}
    #         )
    #     for trans_sentence in transformed_sentence:
    #         test_cases[i]["outputs"].append({"sentence":trans_sentence})
    # json_file = {"type": convert_to_snake_case("add_hashtags"), "test_cases": test_cases}
    #print(json.dumps(json_file))
    for ip in input_sent:
        random.seed(0)
        print(ip)
        res = tf.generate(ip)
        print(res)
