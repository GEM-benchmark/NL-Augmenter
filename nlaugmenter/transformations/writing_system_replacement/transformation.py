"""
The code is based on the code from the whitespace_perturbation task, created by Xinyi Wu:
https://github.com/GEM-benchmark/NL-Augmenter/tree/main/transformations/whitespace_perturbation
"""
import string

import numpy as np

from nlaugmenter.interfaces.SentenceOperation import SentenceOperation
from nlaugmenter.tasks.TaskTypes import TaskType

"""
Implements the Replace Writing System transformation
"""


def build_chinese_chars(use_all_codes=False):
    """Returns a string containing many thousands of Chinese, Japanese, Korean (CJK) characters.

    We use the characters to generate novel alphabets and other writing systems.

    If you want to greatly increase the number of available characters, set
    use_all_codes to True.
    But many environments can't render the additional CJK characters correctly yet (as of 24 jul 2021).
    Thus, please enable them only if you're sure that characters are supported
    on your system.
    See also: https://en.wikipedia.org/wiki/List_of_CJK_Unified_Ideographs,_part_1_of_4

    >>> res0 = build_chinese_chars()
    >>> len(res0)
    27540
    >>> res0[:60]
    '一丁丂七丄丅丆万丈三上下丌不与丏丐丑丒专且丕世丗丘丙业丛东丝丞丟丠両丢丣两严並丧丨丩个丫丬中丮丯丰丱串丳临丵丶丷丸丹为主'
    >>> res0[-60:]
    '䵹䵺䵻䵼䵽䵾䵿䶀䶁䶂䶃䶄䶅䶆䶇䶈䶉䶊䶋䶌䶍䶎䶏䶐䶑䶒䶓䶔䶕䶖䶗䶘䶙䶚䶛䶜䶝䶞䶟䶠䶡䶢䶣䶤䶥䶦䶧䶨䶩䶪䶫䶬䶭䶮䶯䶰䶱䶲䶳䶴'
    """
    if use_all_codes:
        cjk_codes = """
        4E00–9FDF
        3400–4DB5
        3000–303F
        20000–2A6DF
        2A700–2B73F
        2B740–2B81F
        2B820–2CEAF
        2CEB0–2EBEF
        30000–3134F
        """
    else:
        cjk_codes = """
        4E00–9FDF
        3400–4DB5
        """

    code_ranges = []
    for line in cjk_codes.split():
        code_points = line.split("–")
        code_ranges.append(tuple(code_points))

    res = ""
    for start_end in code_ranges:
        start, end = start_end
        for i in range(int(start, 16), int(end, 16)):
            res += chr(i)
    return res


def get_char_candidate(chars_to_select_from, rnd_generator, max_chars=3):
    """Returns a string containing 1 or several random Chinese characters.

    >>> test_rnd_generator = np.random.default_rng(seed=42)
    >>> all_chars = build_chinese_chars()
    >>> get_char_candidate(all_chars, test_rnd_generator, max_chars=10)
    '㕣'
    >>> get_char_candidate(all_chars, test_rnd_generator, max_chars=10)
    '紶粕㹾圾餅掬堡'
    """
    char_num = int(rnd_generator.integers(low=1, high=max_chars + 1, size=1))
    indexes = rnd_generator.choice(len(chars_to_select_from), size=char_num)

    res = ""
    for ind in indexes:
        res += chars_to_select_from[ind]
    return res


def select_from_dict(original_dict, allowed_keys):
    """
    >>> select_from_dict({"spam": 1, "eggs": 2, "pizza": 3}, allowed_keys=("pizza", "spam"))
    {'spam': 1, 'pizza': 3}
    >>> select_from_dict({"spam": 1, "eggs": 2, "pizza": 3}, allowed_keys=())
    {'spam': 1, 'eggs': 2, 'pizza': 3}
    """
    if len(allowed_keys) > 0:
        filtered_dict = dict()
        for key, value in original_dict.items():
            if key in allowed_keys:
                filtered_dict[key] = value
    else:
        filtered_dict = original_dict
    return filtered_dict


def dic_value(input_dic, key, default=None):
    """
    Returns the value from the dic. If input_dic is not a dict, or there is no such key, then returns default
    """
    if isinstance(input_dic, dict):
        value = input_dic.get(key, default)
    else:
        value = default
    return value


def split_text_into_random_length_chunks(
    text, rnd_generator, max_chunk_len=4, exclude_white_spaces=True
):
    """Returns a list of strings, each string being a part of the input text.

    The length of each part is selected randomly.

    >>> test_rnd_generator = np.random.default_rng(seed=42)
    >>> split_text_into_random_length_chunks("I love carrots", test_rnd_generator, exclude_white_spaces=True)
    ['I', 'lov', 'e', 'carr', 'o', 'ts']
    """
    chunks = []
    ind = 0
    while ind < len(text):
        syllable_len = int(
            rnd_generator.integers(low=1, high=max_chunk_len + 1, size=1)
        )
        start = ind
        end = ind + syllable_len
        syllable = text[start:end]
        if exclude_white_spaces and " " in syllable:
            if syllable.startswith(" "):
                ind += 1
                continue
            else:
                space_position = syllable.find(" ")
                end = ind + space_position
                syllable = text[start:end]
        chunks.append(syllable)
        ind = end
    return chunks


def replace_chars(
    input_charset,
    available_chars,
    text,
    rnd_generator,
    max_chars=3,
    deletion_probability=0.0,
    replace_white_spaces=False,
    deletion_tag="<del>",
):
    """Returns a new text, created by replacing parts of the input text with random Chinese characters.

    if deletion_probability > 0, it will also randomly omit parts of the text.

    deletion_tag: str: how removed characters are marked in replacement reports

    Also returns a report, demonstrating how the replacement was done.

    >>> test_rnd_gen = np.random.default_rng(seed=42)
    >>> all_chars = build_chinese_chars()
    >>> replace_chars(["I", "love", "potato", "es"], all_chars, "I love potatoes", test_rnd_gen, max_chars=1)
    ('鑪 紶 掬堡', "'I' -> '鑪' , 'love' -> '紶' , 'potato' -> '掬' , 'es' -> '堡'")
    >>> replace_chars(["I", "lo", "ve", "potat", "o", "es"], all_chars, "I love potatoes", test_rnd_gen, max_chars=1)
    ('鬯 㚱菓 痣祊㪣', "'I' -> '鬯' , 'lo' -> '㚱' , 've' -> '菓' , 'potat' -> '痣' , 'o' -> '祊' , 'es' -> '㪣'")
    >>> charset = ["I", "lo", "ve", "potat", "o", "es"]
    >>> replace_chars(charset, all_chars, "I love potatoes", test_rnd_gen, max_chars=1, deletion_probability=0.3)
    ('䆥哝 忆龍緲', "'I' -> '<del>' , 'lo' -> '䆥' , 've' -> '哝' , 'potat' -> '忆' , 'o' -> '龍' , 'es' -> '緲'")
    """

    mapping = dict()
    claimed_chars = set()

    old_new_chars_tuple_list = []
    for old_char in input_charset:
        if old_char in mapping:
            pass  # already mapped
        else:
            if old_char == " " and not replace_white_spaces:
                mapping[old_char] = " "
                claimed_chars.add(" ")
            elif rnd_generator.random() < deletion_probability:
                mapping[old_char] = deletion_tag
            else:
                candidate = get_char_candidate(
                    available_chars, rnd_generator, max_chars=max_chars
                )
                counter = 0
                retries_num = 10
                while candidate in claimed_chars and counter < retries_num:
                    candidate = get_char_candidate(
                        available_chars, rnd_generator, max_chars=max_chars
                    )
                    counter += 1

                if candidate in claimed_chars:
                    """
                    Omitting chars that we've failed to convert.
                    Omitting causes no harm, as
                    one can consider the char as non-writeable in the new writing system
                    """
                    mapping[old_char] = deletion_tag
                else:
                    mapping[old_char] = candidate
                    claimed_chars.add(candidate)
        old_new = (old_char, mapping[old_char])
        old_new_chars_tuple_list.append(old_new)

    """
    We replace the longest chunks first, to avoid situations where
    a short chunk is contained in a long chunk, and thus will be incorrectly
    replaced.
    For example, the input text is "I love potatoes". The chunks in question
    are "e" and "oes". We first replace "oes", and only then "e".
    """
    done_part = ""
    remaining_part = text
    report = ""
    report_separator = " , "
    for mapping_tuple in old_new_chars_tuple_list:
        old_char, new_char = mapping_tuple
        report += f"'{old_char}' -> '{new_char}'{report_separator}"
        if new_char == deletion_tag:
            replacement = ""
        else:
            replacement = new_char

        if remaining_part.startswith(old_char):
            done_part += replacement
            remaining_part = remaining_part[len(old_char) :]
        else:
            evaluated_part = remaining_part
            spaces_punctuation_etc = ""

            cursor_ind = 0
            while not evaluated_part.startswith(old_char) and cursor_ind < len(
                remaining_part
            ):
                cursor_ind += 1
                spaces_punctuation_etc += evaluated_part[0]
                evaluated_part = evaluated_part[1:]
            done_part += spaces_punctuation_etc + replacement
            remaining_part = evaluated_part[len(old_char) :]

    if report.endswith(report_separator):
        report = report[: -len(report_separator)]

    return done_part.strip(), report


def to_alphabet(
    input_text,
    available_chars,
    rnd_generator,
    settings=None,
):
    """Replaces text characters in such a way, as if the text was written in a different alphabet.

    For example:
    "I love carrots" -> "鑪 鬯㚱㪣堡 掬紶菓菓㚱祊痣"

    It is done by replacing each character with a character from a randomly generated alphabet.
    In the example above, "o" is replaced "㚱", and so on.

    >>> test_rnd_generator = np.random.default_rng(seed=42)
    >>> all_chars = build_chinese_chars()
    >>> new_text, _, report = to_alphabet("I love carrots", all_chars, test_rnd_generator); new_text
    '鑪 紶掬堡鬯 㚱菓痣痣掬祊㪣'
    >>> report[:65]
    "'I' -> '鑪' , 'l' -> '紶' , 'o' -> '掬' , 'v' -> '堡' , 'e' -> '鬯' , "
    >>> settings = {"max_alphabet_chars": 2}
    >>> new_text, _, report = to_alphabet("I love carrots", all_chars, test_rnd_generator, settings=settings); new_text
    '覩 㬩毅饜琣䈵拰甥 裌䕟稲焍稲焍饜琣肃寺'
    """
    max_alphabet_chars = dic_value(settings, "max_alphabet_chars", default=1)
    alphabet_chunk_len = dic_value(settings, "alphabet_chunk_len", default=1)
    replace_white_spaces = dic_value(settings, "replace_white_spaces", False)

    input_charset = split_text_into_random_length_chunks(
        input_text,
        rnd_generator,
        max_chunk_len=alphabet_chunk_len,
        exclude_white_spaces=not replace_white_spaces,
    )
    new_text, replacement_report = replace_chars(
        input_charset,
        available_chars,
        input_text,
        rnd_generator,
        max_chars=max_alphabet_chars,
        replace_white_spaces=replace_white_spaces,
    )
    return new_text, input_charset, replacement_report


def to_syllabary(
    input_text,
    available_chars,
    rnd_generator,
    settings=None,
):
    """Replaces text characters in such a way, as if the text was written in a syllabary writing system.

    For example, "I love carrots" could be converted into a fake syllabary system as follows:
    0. Randomly assign syllables: ['I', 'lov', 'e', 'pota', 't', 'oes']
    1. Assign each syllable a random character:
    '蚴 䬔蕆 富憩䗑'

    >>> test_rnd_gen = np.random.default_rng(seed=42)
    >>> all_chars = build_chinese_chars()
    >>> new_text, _,replacement_report = to_syllabary("I love potatoes", all_chars, test_rnd_gen); new_text
    '蚣 䬕蔶 寈憣䗔'
    >>> replacement_report
    "'I' -> '蚣' , 'lov' -> '䬕' , 'e' -> '蔶' , 'pota' -> '寈' , 't' -> '憣' , 'oes' -> '䗔'"
    >>> test_rnd_gen = np.random.default_rng(seed=0)
    >>> test_sentence = "Neuroplasticity is a processing allowing short-term, medium-term, and long-term remodeling..."
    >>> augmented_text, augment_report = add_common_writing_system_augments(test_sentence, test_rnd_gen)
    >>> test_rnd_gen = np.random.default_rng(seed=0)
    >>> new_text, _,_ = to_syllabary(augmented_text, all_chars, test_rnd_gen); new_text
    '鱾偠蠿祡儋蚋鎟羕䵨䡖鏹䁆岈鏹癢潠嗘䚜楣炠鿔砡體鄊礟㛍嚇呌㺦'
    """
    syllabary_chunk_len = dic_value(settings, "syllabary_chunk_len", default=4)
    max_syllabary_chars = dic_value(settings, "max_syllabary_chars", default=1)
    replace_white_spaces = dic_value(settings, "replace_white_spaces", False)

    charset = split_text_into_random_length_chunks(
        input_text,
        rnd_generator,
        max_chunk_len=syllabary_chunk_len,
        exclude_white_spaces=True,
    )
    new_text, replacement_report = replace_chars(
        charset,
        available_chars,
        input_text,
        rnd_generator,
        max_chars=max_syllabary_chars,
        replace_white_spaces=replace_white_spaces,
    )
    return new_text, charset, replacement_report


def to_logographic(
    input_text,
    available_chars,
    rnd_generator,
    settings=None,
):
    """Replaces text characters in such a way, as if the text was written in a logographic writing system.

    For example, "I love carrots" could be converted into a fake logographic system as follows:
    0. Split the text into words: ['I', 'love', 'carrots']
    1. Assign each word a random character:
    '蚴 䬔 䗑'

    >>> test_rnd_gen = np.random.default_rng(seed=111)
    >>> potatoes = "I love potatoes. potatoes are tasty"
    >>> all_chars = build_chinese_chars()
    >>> settings = {"max_logographic_chars": 1, "remove_white_spaces": False}
    >>> new_text, _, report = to_logographic(potatoes, all_chars, test_rnd_gen, settings=settings); new_text
    '鯘 怶 㸊. 㸊 㒴 翕'
    >>> report
    "'I' -> '鯘' , 'love' -> '怶' , 'potatoes' -> '㸊' , 'potatoes' -> '㸊' , 'are' -> '㒴' , 'tasty' -> '翕'"
    >>> settings = {"max_logographic_chars": 1, "remove_white_spaces": True}
    >>> new_text, _, report = to_logographic(potatoes, all_chars, test_rnd_gen, settings=settings); new_text
    '䩘纀牤.牤䌡竀'
    >>> settings = {"max_logographic_chars": 3, "remove_white_spaces": False}
    >>> new_text, _, report = to_logographic(potatoes, all_chars, test_rnd_gen, settings=settings); new_text
    '滛譴 腥噠 藔. 藔 缽蕃 氦検瘍'
    >>> settings = {"max_word_len": 50, "max_logographic_chars": 1}
    >>> to_logographic("Supercalifragilisticexpialidocious", all_chars, test_rnd_gen, settings=settings)
    ('昀莫', ['Superc', 'alifragilisticexpialidocious'], "'Superc' -> '昀' , 'alifragilisticexpialidocious' -> '莫'")
    """
    max_word_len = dic_value(settings, "max_word_len", default=10)
    replace_white_spaces = dic_value(settings, "replace_white_spaces", False)
    remove_white_spaces = dic_value(settings, "remove_white_spaces", True)
    max_logographic_chars = dic_value(settings, "max_logographic_chars", 3)

    if " " in input_text:
        cleaned = remove_punctuation(input_text)
        words = cleaned.split(" ")
        charset = words
        new_text, replacement_report = replace_chars(
            charset,
            available_chars,
            input_text,
            rnd_generator,
            max_chars=max_logographic_chars,
            replace_white_spaces=replace_white_spaces,
        )
        if remove_white_spaces:
            new_text = remove_spaces(new_text)
    else:
        charset = split_text_into_random_length_chunks(
            input_text, rnd_generator, max_chunk_len=max_word_len
        )
        new_text, replacement_report = replace_chars(
            charset,
            available_chars,
            input_text,
            rnd_generator,
            max_chars=max_logographic_chars,
            replace_white_spaces=replace_white_spaces,
        )
    return new_text, charset, replacement_report


def to_partial_phonemic(
    input_text,
    available_chars,
    rnd_generator,
    settings=None,
):
    """Replaces text characters in such a way, as if the text was written in a partial phonemic writing system.

    For example, "I love cats" could be converted into a fake partial phonemic system as follows:
    0. Split the text into small random parts: ['I', 'lo', 've', 'ca', 'ts']
    1. Remove a random selection of the parts: ['lo', 've', 'ca']
    1. Assign each remaining part a random character:
    '蚴 䬔 䗑'

    vowel_ratio determines how many parts will be removed, simulating the omission of vowels
    in partial phonemic writing systems.

    >>> test_rnd_generator = np.random.default_rng(seed=42)
    >>> all_chars = build_chinese_chars()
    >>> settings = {"vowel_ratio": 0.3}
    >>> new_text, _, report = to_partial_phonemic("I love cats", all_chars, test_rnd_generator, settings=settings); new_text
    '堡 鬯㚱 憣䗔袭'
    >>> report
    "'I' -> '堡' , 'lo' -> '鬯' , 'v' -> '<del>' , 'e' -> '㚱' , 'c' -> '憣' , 'at' -> '䗔' , 's' -> '袭'"
    >>> new_text, _, report = to_partial_phonemic("I love cats", all_chars, test_rnd_generator, settings=settings); new_text
    '忆 龍緲䈵 莍'
    >>> report
    "'I' -> '忆' , 'l' -> '龍' , 'o' -> '緲' , 've' -> '䈵' , 'c' -> '<del>' , 'at' -> '莍' , 's' -> '<del>'"
    """
    vowel_ratio = dic_value(settings, "vowel_ratio", default=0.4)
    phonemic_chunk_len = dic_value(settings, "phonemic_chunk_len", default=2)
    max_phonemic_chars = dic_value(settings, "max_phonemic_chars", default=1)
    replace_white_spaces = dic_value(settings, "replace_white_spaces", False)

    input_charset = split_text_into_random_length_chunks(
        input_text,
        rnd_generator,
        max_chunk_len=phonemic_chunk_len,
        exclude_white_spaces=True,
    )
    new_text, replacement_report = replace_chars(
        input_charset,
        available_chars,
        input_text,
        rnd_generator,
        deletion_probability=vowel_ratio,
        max_chars=max_phonemic_chars,
        replace_white_spaces=replace_white_spaces,
    )
    return new_text, input_charset, replacement_report


def reverse_writing_direction(
    input_text, main_rnd_generator=None, settings=None
):
    """Simulates a reversal of writing direction, by returning input_text in a reverse order.

    main_rnd_generator argument is listed only for compatibility purposes.

    >>> reverse_writing_direction("I love carrots")
    'storrac evol I'
    """
    chars_list = list(input_text)
    chars_list.reverse()
    return "".join(chars_list)


def remove_punctuation(input_text, main_rnd_generator=None, settings=None):
    """Removes punctuation.

    main_rnd_generator argument is listed only for compatibility purposes.

    >>> remove_punctuation("I love carrots, and potatoes!")
    'I love carrots and potatoes'
    """
    translation_table = str.maketrans("", "", string.punctuation)
    return input_text.translate(translation_table)


def remove_spaces(input_text, main_rnd_generator=None, settings=None):
    """Removes spaces.

    main_rnd_generator argument is listed only for compatibility purposes.

    >>> remove_spaces("I love carrots")
    'Ilovecarrots'
    """
    return input_text.replace(" ", "")


def rearrange_spaces(input_text, rnd_generator, settings=None):
    """Removes spaces, and then adds some in random positions.

    >>> test_rnd_generator = np.random.default_rng(seed=42)
    >>> rearrange_spaces("I love carrots, and potatoes!", test_rnd_generator)
    'Ilove carr ots,and po tatoes!'
    >>> rearrange_spaces("I love carrots, and potatoes!", test_rnd_generator)
    'I lo v ecarrot s ,a ndpotatoe s! '
    """

    spaces_frequency = dic_value(settings, "spaces_frequency", 0.3)

    without_spaces = remove_spaces(input_text)
    res = ""
    for char in without_spaces:
        if rnd_generator.random() < spaces_frequency:
            res += char + " "
        else:
            res += char
    return res


def replace_writing_system(
    input_text,
    available_chars,
    rnd_generator,
    target_systems=(),
    settings=None,
):
    """Randomly selects a writing system, and modifies the input text as if it was written in the said system.

    >>> test_rnd_generator = np.random.default_rng(seed=12)
    >>> all_chars = build_chinese_chars()
    >>> new_text, system_name,_,_ = replace_writing_system("I love potatoes", all_chars, test_rnd_generator); new_text, system_name
    ('阠㚶乍 渓绌敿', 'partial_phonemic')
    >>> new_text,system_name,_,_ = replace_writing_system("I love potatoes", all_chars, test_rnd_generator); new_text, system_name
    ('䃓 熵鏘 㚐料', 'syllabary')
    >>> new_text,system_name,_,_ = replace_writing_system("I love potatoes", all_chars, test_rnd_generator); new_text, system_name
    ('驿掩㑇㕶誨', 'logographic')
    >>> new_text,system_name,_,_ = replace_writing_system("I love potatoes", all_chars, test_rnd_generator); new_text, system_name
    ('之 笓䒉㘔䆇 躓䒉蝲討蝲䒉䆇䁣', 'alphabet')
    """
    all_writing_systems = {
        "alphabet": to_alphabet,
        "syllabary": to_syllabary,
        "partial_phonemic": to_partial_phonemic,
        "logographic": to_logographic,
    }

    writing_systems = select_from_dict(all_writing_systems, target_systems)

    ind = int(rnd_generator.integers(low=0, high=len(writing_systems), size=1))
    system_name = list(writing_systems)[ind]

    new_text, charset, replacement_report = writing_systems[system_name](
        input_text,
        available_chars,
        rnd_generator,
        settings=settings,
    )
    return new_text, system_name, charset, replacement_report


def add_common_writing_system_augments(
    input_text,
    rnd_generator,
    target_augments=(),
    settings=None,
):
    """Randomly selects 0 or several augmentations, and applies them the the input text.

    For example, it could reverse the writing direction.

    >>> test_rnd_generator = np.random.default_rng(seed=42)
    >>> add_common_writing_system_augments("I love carrots, and potatoes!", test_rnd_generator)
    ('Ilovecarrotsandpotatoes', ['remove_punctuation', 'remove_spaces'])
    >>> add_common_writing_system_augments("I love carrots, and potatoes!", test_rnd_generator)
    ('I love carrots an dpotatoe s', ['remove_punctuation', 'rearrange_spaces'])
    >>> add_common_writing_system_augments("I love carrots, and potatoes!", test_rnd_generator)
    ('Ilovecarrots,andpotatoes!', ['remove_spaces'])
    >>> add_common_writing_system_augments("I love carrots, and potatoes!", test_rnd_generator)
    ('seota t op dnastorra ce v o lI', ['reverse_writing_direction', 'remove_punctuation', 'remove_spaces', 'rearrange_spaces'])
    """
    all_augments = {
        "reverse_writing_direction": reverse_writing_direction,
        "remove_punctuation": remove_punctuation,
        "remove_spaces": remove_spaces,
        "rearrange_spaces": rearrange_spaces,
    }

    augments = select_from_dict(all_augments, target_augments)

    indexes = rnd_generator.integers(
        low=0, high=2, size=len(augments)
    ).tolist()
    augments_to_use = []
    augments_list = list(augments)
    for i in range(len(indexes)):
        ind = indexes[i]
        if ind == 1:
            augments_to_use.append(augments_list[i])

    for augment_name in augments_to_use:
        input_text = augments[augment_name](
            input_text, rnd_generator, settings
        )

    return input_text, augments_to_use


class WritingSystemReplacement(SentenceOperation):
    """
    >>> test_obj = WritingSystemReplacement(seed=5, target_systems=("alphabet"), target_augments=None)
    >>> test_obj.generate(sentence="he we i")
    ['偯㤋 䮁㤋 反']
    >>> test_obj.replace_white_spaces = True  # to replace white space with another char
    >>> test_obj.generate(sentence="he we i")
    ['偯㤋䮁反㤋䮁尙']
    """

    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
    ]

    languages = "All"
    keywords = [
        "noise",
        "morphological",
        "lexical",
        "syntactic",
        "rule-based",
        "unnaturally-written",
        "possible-meaning-alteration",
        "high-coverage",
    ]

    def __init__(
        self,
        seed=0,
        max_outputs=1,
        use_all_codes=False,
        target_systems=(),
        target_augments=(),
        replace_white_spaces=False,
        remove_white_spaces=True,
        vowel_ratio=0.4,
        max_word_len=10,
        max_logographic_chars=3,
        max_alphabet_chars=1,
        max_phonemic_chars=1,
        max_syllabary_chars=1,
        alphabet_chunk_len=1,
        syllabary_chunk_len=4,
        phonemic_chunk_len=2,
        spaces_frequency=0.3,
    ):
        """
        Arguments:
            use_all_codes: bool: Set to True if you want to greatly increase the number of available characters.
                But many environments can't render the additional CJK characters correctly yet (as of 24 jul 2021).
                Thus, please enable them only if you're sure that characters are supported on your system.
                See also: https://en.wikipedia.org/wiki/List_of_CJK_Unified_Ideographs,_part_1_of_4

            target_systems: tuple: E.g. ("alphabet", "syllabary") . Only the systems listed in this tuple will be used.
                if empty, any of the supported target systems will be used.
                For the list of all supported systems, search for the all_writing_systems variable in this very module.

            target_augments: tuple: E.g. ("reverse_writing_direction", "remove_punctuation") .
                Only the augments listed in this tuple will be used.
                if empty, any of the supported augments will be used.
                For the list of all supported augments, search for the all_augments variable in this very module.

            replace_white_spaces: bool: if True, spaces will be treated same way as all other input chars.

            remove_white_spaces: bool: If True, spaces will be removed.

            vowel_ratio: float: Defines how many input chars will be considered as vowels,
                and thus will be deleted if converted to a partial phonemic writing system.
                Makes sens to set it to some value between 0 and 0.6. If higher - too many chars will be deleted to
                preserve any meaning.

            max_word_len: int: Defines how long are the words in the input text, for the purpose of replacing each word
                with logographic chars. Will be ignored if the input text is split into words by spaces.

            max_logographic_chars: int: Defines how many logographic chars will be used
                to replace each input word, at most.

            max_alphabet_chars: int: Defines how many alphabet chars will be used
                to replace each input char, at most.

            max_phonemic_chars: int: Defines how many phonemic chars will be used
                to replace each input "phoneme", at most.

            max_syllabary_chars: int: Defines how many syllabary chars will be used
                to replace each input "syllable", at most.

            alphabet_chunk_len: int: If set to 1, _each_ input char will be treated as an alphabet letter, to be replaced
                with a char from the a new alphabet.
                If bigger than 1, _several_ input chars will be replaced with a char.

            syllabary_chunk_len: int: same as alphabet_chunk_len, but for syllabary target systems

            phonemic_chunk_len: int: same as alphabet_chunk_len, but for partial phonemic target systems

            spaces_frequency: float: Defines how many spaced will be randomly added in rearrange_spaces augment.
                Can be any number between 0 (no new spaces added) and 1 (add a space after each char)

        """
        self.use_all_codes = use_all_codes
        self.target_systems = target_systems
        self.target_augments = target_augments
        self.replace_white_spaces = replace_white_spaces
        self.remove_white_spaces = remove_white_spaces
        self.vowel_ratio = vowel_ratio
        self.max_word_len = max_word_len
        self.max_logographic_chars = max_logographic_chars
        self.max_alphabet_chars = max_alphabet_chars
        self.max_phonemic_chars = max_phonemic_chars
        self.max_syllabary_chars = max_syllabary_chars
        self.alphabet_chunk_len = alphabet_chunk_len
        self.syllabary_chunk_len = syllabary_chunk_len
        self.phonemic_chunk_len = phonemic_chunk_len
        self.spaces_frequency = spaces_frequency
        super().__init__(seed, max_outputs=max_outputs)

    def generate(self, sentence: str):
        """Returns a list of generated strings. Each string is generated as if the input sentence was written in a
        some randomly selected writing system.

        """
        writing_systems_settings = {
            "replace_white_spaces": self.replace_white_spaces,
            "remove_white_spaces": self.remove_white_spaces,
            "vowel_ratio": self.vowel_ratio,
            "max_word_len": self.max_word_len,
            "max_logographic_chars": self.max_logographic_chars,
            "max_alphabet_chars": self.max_alphabet_chars,
            "max_phonemic_chars": self.max_phonemic_chars,
            "max_syllabary_chars": self.max_syllabary_chars,
            "alphabet_chunk_len": self.alphabet_chunk_len,
            "syllabary_chunk_len": self.syllabary_chunk_len,
            "phonemic_chunk_len": self.phonemic_chunk_len,
            "spaces_frequency": self.spaces_frequency,
        }

        rnd_generator = np.random.default_rng(seed=self.seed)
        perturbed_texts = []
        for _ in range(self.max_outputs):
            if self.target_augments is None:
                augmented_text = sentence
                augment_report = "Not augmenting, as per the target_augments"
            else:
                (
                    augmented_text,
                    augment_report,
                ) = add_common_writing_system_augments(
                    sentence,
                    rnd_generator,
                    target_augments=self.target_augments,
                    settings=writing_systems_settings,
                )

            (
                text_of_new_writing_system,
                system_name,
                _,
                replacement_report,
            ) = replace_writing_system(
                augmented_text,
                build_chinese_chars(use_all_codes=self.use_all_codes),
                rnd_generator,
                settings=writing_systems_settings,
                target_systems=self.target_systems,
            )
            perturbed_texts.append(text_of_new_writing_system)

            # print(augment_report, system_name, replacement_report)
        return perturbed_texts
