import random
import string
import spacy

from typing import List

from initialize import spacy_nlp

from trdg.generators import GeneratorFromStrings

from tesserocr import PyTessBaseAPI, PSM, OEM

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

from transformations.ocr_perturbation.example import generate_test_cases


"""
This transformation renders input text as an image (optionally augmented with 
geometric distortions and/or pixel-level noise) and recognizes the rendered text
using the Tesseract 4 OCR engine. It returns the recognized text as the result.
"""

tess_lang = {
    "en": "eng", # English
    "fr": "fra", # French
    "es": "spa", # Spanish
    "de": "deu", # German
}

trdg_lang = {
    "en": "en", # English
    "fr": "fr", # French
    "es": "es", # Spanish
    "de": "de", # German
}

class RenderingParams(object):
    def __init__(self, background_type=2, distortion_type=0,
        distortion_orientation=0, blur=0):
        """
        :param background_type: 0=noisy, 1=clean, 2=texture, 3=color_texture
        :param distortion_type: 0=none, 1=sin, 2=cos, 3=random
        :param distortion_orientation: 0=vertical, 1=horizontal, 2=both
        :param blur: blur radius
        """
        self.background_type = background_type
        self.distorsion_type = distortion_type
        self.distortion_orientation = distortion_orientation
        self.blur = blur


class OcrPerturbation(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en", "fr", "es", "de"]
    keywords = [
        "lexical",
        "morphological",
        "discourse",
        "api-based",
        "tokenizer-required",
        "unnatural-sounding",
        "high-precision",
        "high-coverage",
        "high-generations",
    ]

    def __init__(
        self, seed=0, max_outputs=1, language="en", params=RenderingParams()):
        """
        Instatiates an OcrPerturbation object
        
        :param seed: random seed
        :param max_outputs: maximum number of generated results
        :param language: one of ['en', 'fr', 'es', 'de']
        :param custom_params: image rendering parameters
        """
        assert language in self.languages
        
        super().__init__(seed, max_outputs=max_outputs)
        self.language = language
        self.params = params
        self.nlp = self._get_spacy_model()


    def generate(self, sentence: str) -> List[str]:

        random.seed(self.seed)

        perturbed_sentences = []        
        
        with PyTessBaseAPI(lang=tess_lang[self.language], psm=PSM.RAW_LINE, 
            oem=OEM.LSTM_ONLY) as ocr:
            
            for idx in range(self.max_outputs):
            
                perturbed_sentence = ""
                
                doc = self.nlp(sentence)
                assert doc.has_annotation("SENT_START")
                
                for sent in doc.sents:

                    image_generator = self._get_image_generator(sent.text)
                    img, lbl = image_generator.next()

                    import os
                    fonts = image_generator.fonts
                    gen_cnt = image_generator.generated_count
                    font_names = [os.path.split(font)[1] for font in fonts]

                    print(gen_cnt, fonts[(gen_cnt - 1) % len(fonts)], font_names)

                    ocr.SetImage(img)

                    try:
                        recognized_text = ocr.GetUTF8Text()
                        recognized_text = recognized_text.strip().replace("\n", "").replace("\t", "")
                    except RuntimeError:
                        recognized_text = sent.text
                    
                    perturbed_sentence += " " + recognized_text

                perturbed_sentences.append(perturbed_sentence.strip())
                    
        return perturbed_sentences                
        
    def _get_image_generator(self, sentence):
        gen = GeneratorFromStrings(
                [sentence],
                language=trdg_lang[self.language],
                size=32,
                skewing_angle=0,
                random_skew=False,
                blur=self.params.blur, 
                random_blur=False,
                is_handwritten=False,
                background_type=self.params.background_type, 
                distorsion_type=self.params.distorsion_type, 
                alignment=1, 
                text_color="#282828",
                distorsion_orientation=self.params.distortion_orientation,
                orientation=0, 
                space_width=1,
                character_spacing=0,
                margins=(2,2,2,2)
            )

        # shuffle fonts
        random.shuffle(gen.fonts)

        return gen
            
    def _get_spacy_model(self):
        if self.language == 'en':
            return spacy_nlp if spacy_nlp else spacy.load("en_core_web_sm")
        elif self.language == 'fr':
            return spacy.load("fr_core_news_sm")
        elif self.language == 'es':
            return spacy.load("es_core_news_sm")
        elif self.language == 'de':
            return spacy.load("de_core_news_sm")
        else:
            return None

"""
# Sample code to demonstrate usage. Can also assist in adding test cases.

if __name__ == '__main__':

    tf = OcrPerturbation(max_outputs=1)
    
    generate_test_cases(tf, print_result=True)

    # generate 'test.json'
    #generate_test_cases(tf, output_filename="test.json")
"""
