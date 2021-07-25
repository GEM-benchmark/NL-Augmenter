from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType
import language_tool_python


class TextContainsGrammarError(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ['ar', 'ast', 'ast-ES', 'be', 'be-BY', 'br', 'br-FR', 'ca', 'ca-ES',
                 'ca-ES-valencia', 'da', 'da-DK', 'de', 'de-AT', 'de-CH', 'de-DE',
                 'de-DE-x-simple-language', 'el', 'el-GR', 'en', 'en-AU', 'en-CA',
                 'en-GB', 'en-NZ', 'en-US', 'en-ZA', 'eo', 'es', 'es-AR', 'fa',
                 'fr', 'ga', 'ga-IE', 'gl', 'gl-ES', 'it', 'ja', 'ja-JP', 'km',
                 'km-KH', 'nl', 'nl-BE', 'pl', 'pl-PL', 'pt', 'pt-AO', 'pt-BR',
                 'pt-MZ', 'pt-PT', 'ro', 'ro-RO', 'ru', 'ru-RU', 'sk', 'sk-SK',
                 'sl', 'sl-SI', 'sv', 'ta', 'ta-IN', 'tl', 'tl-PH', 'uk', 'uk-UA',
                 'zh', 'zh-CN']

    def __init__(self, lang='en-US'):
        super().__init__()
        self.lang = lang
        self.tool = language_tool_python.LanguageTool(lang)

    def filter(self, sentence: str = None) -> bool:
        matches = self.tool.check(sentence)
        return bool(matches)
