import itertools
import random
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
Visual letter perturbation based on image-based character embedding space from https://arxiv.org/pdf/1903.11508v1.pdf.
You can obtain them yourself, too, by repeating this code:

from gensim.models import KeyedVectors as W2Vec
model = W2Vec.load_word2vec_format('vce.normalized')
model.similar_by_key('a', topn=100, restrict_vocab=None)

Then by visual inspection, remove some characters that could be confused by an already existing letter. (manually)
Obviously using the topn=100 or even topn=20 which they do in the paper would be easier to use
But I found the quality of the nearest neighbors was sometimes bad, like replacing v's with y's since they are visually similar
So that is why I selected these manually. Obviously pretty subjective here.

Future improvements: add other typefaces, for example you could all of the ones from this website: https://lingojam.com/CoolTextFonts
For example, ABCDE -> ⒶⒷⒸⒹⒺ

Future improvements: This can be applied to other alphabets e.g. Cyrillic, Greek, Armenian, Georgian, Hangul, etc.
"""

letter_mappings = {
  'a': ['а', 'ạ', 'ȧ', 'ḁ', 'ā', 'ą', 'ä', 'ӓ', 'ã', 'á', 'ẚ', 'â', 'à', 'ả', 'ậ', 'ǎ', 'ă', 'ӑ', 'ȃ', 'ắ', 'ặ', 'ằ', 'ȁ', 'ɑ', 'ầ', 'α', '⍺', 'ẳ', 'å'],
  'b': ['ḅ', 'ḇ', 'þ', 'ϸ', 'ƀ', 'ƅ', 'ɓ', 'ƃ', 'ƥ', 'ᖯ', 'ᑲ', 'ᑿ', 'Ь'],
  'c': ['ᴄ', 'с', 'ⅽ', 'ϲ', 'ċ', 'ç', 'ҫ', 'ć', 'ς', 'ҁ', 'ĉ', 'ƈ', 'ϛ', 'ḉ'],
  'd': ['ⅾ', 'ḍ', 'ḏ', 'ḓ', 'ḑ', 'ɖ', 'đ', 'ժ', '₫', 'ƌ', 'ď', 'ᴅ', 'ɗ', 'ᑯ', 'ð', 'ᕷ', 'ɒ', 'ȡ', 'ᴆ', 'ᑻ'],
  'e': ['е', 'ẹ', 'ė', 'ȩ', 'є', 'ē', 'ę', 'ḛ', 'ë', 'ё', 'ǝ', 'ə', 'ә', 'ẽ', 'ɘ', 'è', 'ḙ', 'ɞ', 'ɐ', 'ѐ', 'ê', 'é', 'ẻ', 'ͼ', 'ε', 'ԑ', 'ɛ', 'ệ', 'ě', 'ĕ', 'ӗ', 'ȇ', 'ȅ', 'ề', 'ℯ', 'ḝ', 'ἐ', 'ἑ', 'ᴇ', 'ḕ'],
  'f': ['ƒ', 'ẜ', 'ḟ', 'ẝ', 'ʄ', 'ϝ'],
  'g': ['ց', 'ɡ', 'ģ', 'ġ', 'ḡ', 'ǵ', 'ĝ', 'ǥ', 'ǧ', 'ğ', 'ɠ'],
  'h': ['հ', 'һ', 'ḥ', 'ẖ', 'ḫ', 'ի', 'ɦ', 'ḩ', 'ɧ', 'ћ', 'ħ', 'Һ', 'ℎ', 'ⱨ'],
  'i': ['і', 'ⅰ', 'ị', 'į', 'ı', 'ו', 'إ', 'ߊ', 'ἰ', 'ľ', 'ⵏ', 'ἱ', '⍳', 'ι', 'ɩ', 'ⵑ', 'ɨ', 'í', '⌊', 'ḭ', 'ᶅ', 'ǃ', 'ί', 'ί', 'î', 'ĩ', '׀', 'ℹ'],
  'j': ['ј', 'ϳ', 'ȷ', 'ɉ', 'ĵ', 'ǰ', 'ز', 'ڗ', 'ۈ', 'ژ', 'ڙ', 'ڒ', 'ڑ', 'ⅉ',],
  'k': ['ķ', 'ḳ', 'ḵ', 'ƙ', 'ᴋ', 'ĸ', 'ҟ', 'κ', 'ⱪ', 'к', 'ҝ', 'ԟ', 'ќ', 'ḱ'],
  'l': ['ⅼ', 'ا', 'ļ', 'ḷ', 'ŀ', 'ḽ', 'ł', 'ⵏ', 'ɭ', 'ᶅ', 'Ɩ', 'ȴ', 'ⱡ', 'լ'],
  'm': ['ⅿ', 'ṃ', 'ṁ', 'ḿ', 'ⴇ', 'ⴊ', 'ⴔ', 'ⴜ'],
  'n': ['ո', 'ņ', 'ṇ', 'ṉ', 'ח', 'ṅ', 'ṋ', 'η', 'ƞ', 'ŋ', 'ɳ', 'п', 'ῃ', 'ה', 'ɲ', 'ñ', 'ռ', 'ǹ', 'һ', 'ń', 'ἠ', 'ἡ', 'ᾐ', 'ᾑ', 'ῆ', 'ᴨ', 'ⴖ', 'ὴ', 'ῇ', 'ň', 'ῂ', 'ή', 'ή', 'ɴ', 'ἢ', 'ἣ', 'ῄ', 'ᴎ', 'ͷ', 'и', 'ᾒ', 'ᾓ', 'ἤ'],
  'o': ['ο', 'օ', 'ᴏ', 'о', 'ọ', 'ȯ', 'ơ', 'σ', 'ǫ', 'ợ', 'ὀ', 'ὁ', 'ō', 'ø', 'ϙ', 'ӧ', 'ö', 'ɵ', 'ѳ', 'ө', 'õ', 'ʊ', 'ວ', 'ǭ', 'ό', 'ό', 'ó', 'ô', 'ὸ', 'ò', 'ỏ', 'ớ', 'ὂ', 'ὃ', '໐', 'ס', 'ộ', 'ǿ', 'ờ', 'ở', 'ǒ', '⌀', 'ອ', 'ŏ'],
  'p': ['р', '⍴', 'ρ', 'ṗ', 'ϸ', 'þ', 'ῤ', 'ῥ', 'ṕ', 'ƥ', 'ƿ', 'ҏ', 'բ', 'ᵽ'],
  'q': ['ԛ', 'ɋ', 'ɖ', 'ϥ', 'զ'],
  'r': ['ŗ', 'ṛ', 'ṟ', 'ṙ', 'г', 'ᴦ', 'ṝ', 'ɽ', 'ɼ', 'ґ', 'ŕ', 'Ւ', 'ѓ', 'ř', 'ȓ', 'Ի'],
  's': ['ѕ', 'ș', 'ṣ', 'ṡ', 'ṩ', 'ʂ', 'ş', 'ś', 'ŝ', 'š', 'ṥ'],
  't': ['ț', 'ṭ', 'ṯ', 'ṱ', 'ţ', 'ƭ', 'ƫ', 'ŧ', 'ť', 'ʈ', 'է', 'Է', 'ե'],
  'u': ['ս', 'ṳ', 'ụ', 'ū', 'ư', 'ṵ', 'ü', 'ự', 'ʋ', 'ų', 'ũ', 'ṷ', 'ú', 'ⴎ', 'μ', 'µ', 'û', 'ù', 'υ', 'ủ', 'ບ', 'ᴜ', 'ʊ', 'ữ', 'կ', 'վ', 'մ', 'ứ', 'џ', 'ǔ', 'ů', 'ŭ', 'ừ', 'ߎ', 'ử', 'ὑ', 'ȗ', 'ὐ', 'ט', 'ȕ', 'ῡ', 'ϋ', 'և', 'ű'],
  'v': ['ⅴ', 'ᴠ', 'ṿ', 'ѵ', 'ү', 'ν', 'ṽ', 'ⱱ', 'ⱴ', 'γ', 'ѷ', 'ע'],
  'w': ['ᴡ', 'ԝ', 'ẉ', 'ẇ', 'ẅ', 'ẁ', 'ŵ', 'ẃ', 'ẘ', 'ⱳ', 'ա', 'ⴍ'],
  'x': ['ⅹ', 'х', 'ẋ', 'ӿ', 'ẍ', 'ҳ', 'ӽ'],
  'y': ['у', 'ỵ', 'ү', 'ẏ', 'ȳ', 'ӯ', 'ÿ', 'ӱ', 'ỹ', 'ƴ', 'ў', 'ý', 'ŷ', 'ỷ', 'ỳ', 'ӳ', 'ẙ'],
  'z': ['ᴢ', 'ẓ', 'ẕ', 'ż', 'ƶ', 'ȥ', 'ʐ', 'ź', 'ẑ', 'ʑ', 'ƨ', 'ž'],
  
  'A': ['Α', 'А', 'Ạ', 'ᾼ', 'Ḁ', 'Ἀ', 'Ἁ', 'ᾈ', 'ᾉ', 'Ȧ', 'Ά', 'Ά', 'Ⱥ', 'Ą', 'Ả', 'ᕕ', 'À', 'Ẵ', 'Ằ', 'Ắ', 'Ᾰ', 'Á', 'Ȃ', 'Ã', 'Ӓ', 'Ä', 'Ẳ', '₳', 'Ȁ', 'Ẫ', 'Â', 'ᕖ', 'Ậ', 'Ᾱ', 'Ā', 'Ǎ', 'Å', 'Å', '4', 'Ӑ', 'Ă', 'Ặ', 'Ầ', 'Ấ', 'Ǡ', 'Ǟ', 'Ẩ', 'Ὰ'],
  'B': ['Β', 'В', 'Ḅ', 'Ḇ', 'Ḃ', '8', 'Ƀ', 'ß', 'β', '฿'],
  'C': ['Ⅽ', 'Ϲ', 'С', 'Ҫ', 'Ç', 'Ҁ', 'ᑕ', 'Ċ', 'ᕦ', 'ᑢ', 'Ϛ', 'ⵛ', 'ⵎ', 'Ȼ', 'ᑖ', 'Ć', 'ᕧ', 'ᑤ', '₵', 'ᕩ'],
  'D': ['Ⅾ', 'ᗞ', 'Ḏ', 'Ḍ', 'Ḓ', 'Ḑ', 'ↁ', 'Ḋ', 'Ð', 'Ɖ', 'Đ', 'Ď', 'Ɒ'],
  'E': ['Ε', 'ⴹ', 'Е', 'Ẹ', 'ⵟ', 'Ȩ', 'Ḛ', 'Ę', 'Ḙ', 'Ė', 'Ɛ', 'Ԑ', 'ℇ', 'Є', 'Ẻ', 'È', 'Ӗ', 'Ĕ', 'Ѐ', 'É', 'Ȇ', 'Ƹ', 'Ḝ', 'Ẽ', '⋿', 'Ё', 'Ë', '∃', 'ⴺ', 'Ǝ', '£', 'Ȅ', 'Ễ', 'Ê', 'Ệ', 'Σ', 'ⵉ'],
  'F': ['Ϝ', 'Ḟ', 'ߓ', 'Ғ'],
  'G': ['Ģ', 'Ǥ', 'Ԍ', 'Ġ', 'Ğ', 'Ǵ', 'Ḡ', 'Ĝ'],
  'H': ['Η', 'Н', 'ᕼ', 'Ḥ', 'Ḫ', 'ῌ', 'Ḣ', 'Ḩ', 'Ӈ', 'Ң', 'Ⱨ', 'Ḧ', 'Ĥ', 'Ȟ', 'Ӊ', 'ℍ'],
  'I': ['Ι', 'Ӏ', 'ⵏ', 'І', 'Ⅰ', 'Ị', 'ߊ', 'ⵑ', 'ا', 'ǃ', 'Į', 'ⅼ', 'ӏ', 'إ','׀', 'Ḭ'],
  'J': ['Ј', 'Ɉ', 'յ', 'Ĵ', 'ȷ'],
  'K': ['Κ', 'K', 'Ķ', 'Ḳ', 'Ḵ', '₭', 'Ƙ', 'Ҝ', 'Ḱ', 'К', 'Ԟ', 'Ҟ', 'Ϗ', 'қ', 'Ǩ', 'ⱪ', 'ҟ', 'Ⱪ', 'ԟ', 'ҝ', 'κ', 'к', 'Ќ', 'ⴿ'],
  'L': ['ᒪ', 'Ⅼ', 'Ļ', 'Լ', 'Ḷ', 'Ḻ', 'Ŀ', 'ᒷ', 'Ľ', 'Ḽ', 'ʟ', 'ւ'],
  'M': ['Ⅿ', 'Μ', 'М', 'Ṃ', 'Ṁ', 'Ϻ', 'Ḿ', 'Ɱ', 'Ӎ', 'ᴍ', 'м'],
  'N': ['Ν', 'Ņ', 'Ṉ', 'Ṇ', 'Ṋ', 'Ṅ', 'Ǹ', 'Ń', 'Ñ', 'Ň', 'Ɲ', 'Ŋ'],
  'O': ['Ο', 'Օ', 'О', 'Ọ', 'Ǫ', 'Ơ', 'Θ', 'Ϙ', 'Ợ', 'Ɵ', 'ϴ', 'Ө', 'Ѳ', 'Ȯ', 'Q', 'Ԛ', 'Ό', 'Ό', 'Ὀ', 'Ò', 'Ŏ', '⊙', 'Ờ', 'Ȏ', 'Ó', 'Ỏ', 'Ȍ', '⊝', 'Õ', 'Ṍ', 'Ṏ', 'Ӧ', 'Ö', '⊘', '⊖', 'Ớ', 'Ở', '⊜', '⊛', 'Ỡ', '⊚', 'ʘ', 'Ǿ', 'Ô', 'Ỗ', 'Ộ', 'Ӫ', '⊗', '⊕', 'Փ', 'Ṑ', 'Ō', 'Ṓ', 'Ǒ', 'Ǭ', 'Ὁ', 'Ø', 'Ѻ'],
  'P': ['Ρ', 'Р', 'Ҏ', 'ᑭ', 'ᕈ', 'Ṗ', 'ᑷ', '₱', 'Ᵽ', 'ᑮ', 'ᑹ', 'Ṕ', 'ᕉ', 'ᒆ'],
  'Q': ['Ԛ', 'ℚ'],
  'R': ['Ŗ', 'Ṛ', 'Ṟ', 'Ɽ', 'Ɍ', 'Ṙ', 'Ŕ', 'Ȓ', 'Ṝ', 'Ȑ', '℞', 'Ř', 'Я'],
  'S': ['Ѕ', 'Ș', 'Ṣ', 'Ş', 'Ṡ', 'Ṩ', '5', 'Ś', 'Ƽ', 'Ŝ', 'Ṥ', 'Ṧ', 'Š', 'Ƨ'],
  'T': ['Т', 'Τ', 'Ț', 'Ṭ', 'Ṯ', 'Ṱ', 'Ţ', 'Ŧ', 'Ʈ', 'Ṫ', 'Ҭ', '₮', 'Ԏ', 'Ƭ', '₸', 'Ť', 'ⴶ', 'ͳ', 'ߠ', '☨', '⊺', '☦'],
  'U': ['Ս', 'ᑌ', 'Ṳ', 'Ụ', 'Ų', 'Ṵ', 'ᑘ', 'Ṷ', 'ⵡ', 'Ư', 'Ự', 'Џ', 'Ա', 'Ù', 'Ʉ', 'ᕟ', 'ᕞ', 'Ŭ', 'Ȗ', 'Ú', 'Ủ', 'Ȕ', 'Ů', 'Ṹ', 'Ũ', 'ᑧ', 'Ü', 'Ǘ', 'Ǜ', 'Ǚ', 'Ừ', 'Ц', 'Ứ', 'Ử', 'Û', '∪', 'Ū', 'Ǔ', 'Մ', '⊎', '⊍', '⊌'],
  'V': ['Ⅴ', 'ᐯ', 'ⴸ', 'Ṿ', 'ᐻ', 'Ѵ', '∨', '⊽', 'Ѷ', '⋎', '℣', 'Ṽ'],
  'W': ['Ԝ', 'Ẉ', 'Ẇ', 'Ẁ', 'Ⱳ', '₩', 'Ẅ', 'Ẃ', 'Ŵ', 'Ɯ'],
  'X': ['Х', 'Χ', 'ⵝ', 'Ⅹ', 'Ӿ', 'ⵅ', 'ⴴ', 'Ẋ', 'ⴳ', 'Ẍ', 'Ӽ', 'Ҳ', '✘', '☓', 'ⴵ'],
  'Y': ['Ү', 'Υ', 'Ỵ', 'Ẏ', 'Ƴ', 'Ỷ', 'Ý', 'Ῠ', 'Ỳ', 'Ɏ', 'Ỹ', 'Ÿ', 'Ϋ', 'Ŷ', 'Ȳ', 'Ῡ', 'ϒ'],
  'Z': ['Ζ', 'Ẓ', 'Ẕ', 'Ƶ', 'Ż', 'Ȥ', 'Ź', 'ƻ', 'Ẑ', 'Ž']
}

# Now, let's generate a dictionary that maps every letter to every other letter in its family.
# That way we aren't stuck with only modifying the standard letters in the Latin alphabet
# But instead we can also visually attack nonstandard letters such as 'Ṃ' or 'ǵ' or 'ℚ'

complete_mappings = {}
for key_letter, letter_family in letter_mappings.items():
    for letter in letter_family:
        complete_mappings[letter] = list(set(letter_family) - {letter} | {key_letter})
    
    # Add back in the original mapping
    complete_mappings[key_letter] = letter_family
    
letter_mappings = complete_mappings


class VisualAttackLetters(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION, TaskType.TEXT_TAGGING]
    languages = ["sq", "hy", "bg", "ca", "hr", "cs", "nl", "en", "et", "fi", "fr", "de", "el", "hu", "is", "it", "la", "lv", "lt", "mk", "no", "pl", "pt", "ro", "ru", "sk", "sl", "es", "sv", "tr", "uk"]
    keywords = ['morphological','external-knowledge-based','visual','high-generations']

    def __init__(self, seed: int = 0, max_outputs: int = 1, perturb_pct: float = 0.50) -> None:
        '''
        In order to generate multiple different perturbations, you should set seed=None
        '''
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.perturb_pct = perturb_pct

    def generate(self, sentence: str) -> List[str]:
        random.seed(self.seed)
        sentence_list = list(sentence)
        perturbed_texts = []
        # Perturb the input sentence max_output times
        for _ in itertools.repeat(None, self.max_outputs):
            for idx, letter in enumerate(sentence_list):
                if letter in letter_mappings and random.random() < self.perturb_pct:
                    sentence_list[idx] = random.choice(letter_mappings[letter]) # Perturb the letter
                    
            perturbed_texts.append(''.join(sentence_list))
            
        return perturbed_texts
