from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    AutoModelForSequenceClassification,
)
import torch
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType

"""
code and model from: https://github.com/PrithivirajDamodaran/Styleformer
"""


class Adequacy:
    def __init__(self, model_tag="prithivida/parrot_adequacy_on_BART"):
        self.nli_model = AutoModelForSequenceClassification.from_pretrained(model_tag)
        self.tokenizer = AutoTokenizer.from_pretrained(model_tag)

    def filter(self, input_phrase, para_phrases, adequacy_threshold, device="cpu"):
        top_adequacy_phrases = []
        for para_phrase in para_phrases:
            x = self.tokenizer.encode(
                input_phrase,
                para_phrase,
                return_tensors="pt",
                truncation_strategy="only_first",
            )
            self.nli_model = self.nli_model.to(device)
            logits = self.nli_model(x.to(device))[0]
            # we throw away "neutral" (dim 1) and take the probability of "entailment" (2) as the adequacy score
            entail_contradiction_logits = logits[:, [0, 2]]
            probs = entail_contradiction_logits.softmax(dim=1)
            prob_label_is_true = probs[:, 1]
            adequacy_score = prob_label_is_true[0].item()
            if adequacy_score >= adequacy_threshold:
                top_adequacy_phrases.append(para_phrase)
        return top_adequacy_phrases

    def score(self, input_phrase, para_phrases, adequacy_threshold, device="cpu"):
        adequacy_scores = {}
        for para_phrase in para_phrases:
            x = self.tokenizer.encode(
                input_phrase,
                para_phrase,
                return_tensors="pt",
                truncation_strategy="only_first",
            )
            self.nli_model = self.nli_model.to(device)
            logits = self.nli_model(x.to(device))[0]
            # we throw away "neutral" (dim 1) and take the probability of "entailment" (2) as the adequacy score
            entail_contradiction_logits = logits[:, [0, 2]]
            probs = entail_contradiction_logits.softmax(dim=1)
            prob_label_is_true = probs[:, 1]
            adequacy_score = prob_label_is_true[0].item()
            if adequacy_score >= adequacy_threshold:
                adequacy_scores[para_phrase] = adequacy_score
        return adequacy_scores


adequacy = Adequacy()


class Formal2Casual(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = True

    def __init__(self, num_beams=5, max_length=32, quality_filter=0.95, device=None):
        super().__init__()
        if self.verbose:
            print("Starting to load Casual to Formal Model...\n")
        m_name = "prithivida/formal_to_informal_styletransfer"
        self.tokenizer = AutoTokenizer.from_pretrained(m_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(m_name)
        if self.verbose:
            print("Completed loading Casual to Formal Model.\n")
        self.adequacy = adequacy
        self.max_output = num_beams
        self.num_beams = num_beams
        self.max_length = max_length
        self.quality_filter = quality_filter
        self.device = device
        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def generate(self, sentence: str):
        ctf_prefix = "transfer Formal to Casual: "
        src_sentence = sentence
        sentence = ctf_prefix + sentence
        input_ids = self.tokenizer.encode(sentence, return_tensors="pt")
        model = self.model.to(self.device)
        input_ids = input_ids.to(self.device)

        preds = model.generate(
            input_ids,
            num_beams=self.num_beams,
            max_length=self.max_length,
            early_stopping=True,
            num_return_sequences=self.max_output,
        )

        gen_sentences = set()
        for pred in preds:
            gen_sentences.add(
                self.tokenizer.decode(pred, skip_special_tokens=True).strip()
            )

        adequacy_scored_phrases = self.adequacy.score(
            src_sentence, list(gen_sentences), self.quality_filter, self.device
        )
        ranked_sentences = sorted(
            adequacy_scored_phrases.items(), key=lambda x: x[1], reverse=True
        )
        if len(ranked_sentences) > 0:
            return [ranked_sentences[0][0]]
        else:
            print("No transfer found!")
            return [sentence]


class Casual2Formal(SentenceOperation):
    tasks = [TaskType.TEXT_CLASSIFICATION, TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    heavy = True

    def __init__(self, num_beams=5, max_length=32, quality_filter=0.95, device=None):
        super().__init__()
        if self.verbose:
            print("Starting to load Casual to Formal Model...\n")
        m_name = "prithivida/informal_to_formal_styletransfer"
        self.tokenizer = AutoTokenizer.from_pretrained(m_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(m_name)
        if self.verbose:
            print("Completed loading Casual to Formal Model.\n")
        self.adequacy = adequacy
        self.max_output = num_beams
        self.num_beams = num_beams
        self.max_length = max_length
        self.quality_filter = quality_filter
        self.device = device
        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def generate(self, sentence: str):
        ctf_prefix = "transfer Casual to Formal: "
        src_sentence = sentence
        sentence = ctf_prefix + sentence
        input_ids = self.tokenizer.encode(sentence, return_tensors="pt")
        model = self.model.to(self.device)
        input_ids = input_ids.to(self.device)

        preds = model.generate(
            input_ids,
            num_beams=self.num_beams,
            max_length=self.max_length,
            early_stopping=True,
            num_return_sequences=self.max_output,
        )

        gen_sentences = set()
        for pred in preds:
            gen_sentences.add(
                self.tokenizer.decode(pred, skip_special_tokens=True).strip()
            )

        adequacy_scored_phrases = self.adequacy.score(
            src_sentence, list(gen_sentences), self.quality_filter, self.device
        )
        ranked_sentences = sorted(
            adequacy_scored_phrases.items(), key=lambda x: x[1], reverse=True
        )
        if len(ranked_sentences) > 0:
            return [ranked_sentences[0][0]]
        else:
            return [sentence]
