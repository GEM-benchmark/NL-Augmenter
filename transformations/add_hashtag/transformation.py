from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import random
from spacy import load

be_class_verb = ["is", "am", "are", "was", "were", "will", "shall"]
subj_obj_list = ["i", "you","we", "they", "he", "she"]
nlp=load('en_core_web_sm')


def extract_dep_nodes(dep_parse):
    # method for extracting VERB, NSUBJ and DOBJ dependency nodes
    verb, nsubj, dobj = "", "", ""
    for token in dep_parse:
        if token.dep_ == "ROOT":
            if token.text.lower() not in be_class_verb:
                verb = token.text
    for token in dep_parse:
        if token.dep_ == "dobj" and token.head.dep_ == "ROOT":
            if token.text.lower() not in subj_obj_list:
                dobj = token.text
        if token.dep_ == "nsubj" and token.head.dep_ == "ROOT":
            if token.text.lower() not in subj_obj_list:
                nsubj = token.text
    return verb.title(), nsubj.title(), dobj.title()


def generate_hashtag_from_noun_chunk(chunk_list):
    hash_tag_list = []
    if not chunk_list:
        return None
    else:
        for chunk in chunk_list:
            if chunk.lower() not in subj_obj_list:
                chunk_words = chunk.split(" ")
                chunk_words = [word.title() for word in chunk_words]
                hash_tag_list.append("#"+"".join(chunk_words))
    return hash_tag_list


def extract_noun_chunks_hashtag(dep_parse):
    chunk_list = []
    for chunk in dep_parse.noun_chunks:
        if len(str(chunk.text.split(" ")))>0:
            chunk_list.append(chunk.text)
    return generate_hashtag_from_noun_chunk(chunk_list)


def extract_hashtags(sentence):
    # method for gathering all hashtags
    dep_parse = nlp(sentence)
    verb, nsubj, dobj = extract_dep_nodes(dep_parse)
    hash_tag_list = []
    for dep_n in [verb, nsubj, dobj]:
        if(dep_n != ""):
            hash_tag_list.append("#"+dep_n)
    if verb != "" and dobj != "":
        hash_tag_list.append("#"+verb+dobj)
    noun_chunks_hashtags = extract_noun_chunks_hashtag(dep_parse)
    if noun_chunks_hashtags is not None:
        hash_tag_list.extend(noun_chunks_hashtags) # merging both hashtag list
        return set(hash_tag_list)
    return hash_tag_list


def get_hash_tags(sentence, seed=0, max_outputs=1):
    # method for adding hashtags to sentence
    random.seed(seed)
    hashtag_list = extract_hashtags(sentence)
    transformation_list = []
    for _ in range(max_outputs):
        selected_hastag = random.sample(hashtag_list, random.randint(1, len(hashtag_list)))
        if bool(random.getrandbits(1)):
            transformation_list.append(sentence + " " + " ".join(selected_hastag))
        else:
            transformation_list.append(sentence + "".join(selected_hastag))
    return transformation_list


class HashtagGeneration(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING
    ]
    languages = ["en"]

    def __init__(self, seed=0, max_outputs=2):
        super().__init__(seed)
        self.max_outputs=max_outputs

    def generate(self, sentence: str):
        transformed_sentences = get_hash_tags(sentence, seed=self.seed, max_outputs=self.max_outputs)
        return transformed_sentences


if __name__ == "__main__":
    import json
    from TestRunner import convert_to_snake_case

    tf = HashtagGeneration()
    test_cases = []
    input_sent = ["I love domino's pizza .",
                  "Many people like T20 cricket these days .",
                  "Attention is all you need .",
                  "Natural Language Processing research is awesome."]

    for i,sentence in enumerate(input_sent):
        transformed_sentence = tf.generate(sentence)
        test_cases.append({
                    "class": tf.name(),
                    "inputs": {"sentence": sentence},
                    "outputs": [],}
            )
        for trans_sentence in transformed_sentence:
            #print(trans_sentence)
            test_cases[i]["outputs"].append({"sentence":trans_sentence})
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))