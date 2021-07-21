from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Multilingual Back Translation.
    Translate a sentence to a pivot language and then back to the source lagnuage generating paraphrases.
    Can be used to do "Direct Trranslation" from a source language to itself.
"""


class MultilingualBackTranslation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ['af' ,'am' ,'ar' ,'ast' ,'az' ,'ba' ,'be' ,'bg' ,'bn' ,'br' ,'bs' ,'ca' ,'ceb' ,'cs' ,'cy' ,'da' ,'de' ,'el' ,'en' ,'es' ,'et' ,'fa' ,'ff' ,'fi' ,'fr' ,'fy' ,'ga' ,'gd', 'gl' ,'gu' ,'ha' ,'he' ,'hi' ,'hr' ,'ht' ,'hu' ,'hy' ,'id' ,'ig' ,'ilo' ,'is' ,'it' ,'ja' ,'jv' ,'ka' ,'kk' ,'km' ,'kn' ,'ko' ,'lb' ,'lg' ,'ln' ,'lo' ,'lt' ,'lv' ,'mg' ,'mk' ,'ml' ,'mn' ,'mr' ,'ms' ,'my' ,'ne' ,'nl' ,'no' ,'ns' ,'oc' ,'or' ,'pa' ,'pl' ,'ps' ,'pt' ,'ro' ,'ru' ,'sd' ,'si' ,'sk' ,'sl' ,'so' ,'sq' ,'sr' ,'ss' ,'su' ,'sv' ,'sw' ,'ta' ,'th' ,'tl' ,'tn' ,'tr' ,'uk' ,'ur' ,'uz' ,'vi' ,'wo' ,'xh' ,'yi' ,'yo' ,'zh' ,'zu']
    heavy = True

    def __init__(self, seed=0, max_outputs=1, src_lang:str='en', pivot_lang:str='zh'):
        super().__init__(seed, max_outputs=max_outputs)
        self.model = M2M100ForConditionalGeneration.from_pretrained('facebook/m2m100_418M')
        self.tokenizer = M2M100Tokenizer.from_pretrained('facebook/m2m100_418M')
        self.src_lang = src_lang
        self.pivot_lang = pivot_lang

    def generate(self, sentence: str):

        # Source to Pivot
        self.tokenizer.src_lang = self.src_lang
        encoded_source_sentence = self.tokenizer(sentence, return_tensors="pt")
        generated_pivot_tokens = self.model.generate(**encoded_source_sentence, forced_bos_token_id=self.tokenizer.get_lang_id(self.pivot_lang))
        pivot_sentence = self.tokenizer.batch_decode(generated_pivot_tokens, skip_special_tokens=True)
    
        #Pivot to Source
        if self.pivot_lang != self.src_lang:
            self.tokenizer.src_lang = self.pivot_lang
            encoded_pivot_sentence = self.tokenizer(pivot_sentence, return_tensors="pt")
            generated_source_tokens = self.model.generate(**encoded_pivot_sentence, forced_bos_token_id=self.tokenizer.get_lang_id(self.src_lang))
            source_sentence = self.tokenizer.batch_decode(generated_source_tokens, skip_special_tokens=True)
        else:
            source_sentence = pivot_sentence
    
        return source_sentence

"""
# Sample code to demonstrate usage. Can also assist in adding test cases.
# You don't need to keep this code in your transformation.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = MultilingualBackTranslation()
    test_cases = []
    for sentence in ["The policy of this president ruined our country.",
                     "Next week I will have my birthday party.",
                     "Being honest should be one of our most important character traits.",
                     "My graduation ceremony will be next week.",
                     "What is important is that everyone understands."]:
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence}, "outputs": [{"sentence": o} for o in tf.generate(sentence)]}
        )
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))
"""
