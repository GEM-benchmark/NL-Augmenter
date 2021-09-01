from transformers import BartForConditionalGeneration, BartTokenizer


class reapModel(object):
    def __init__(self, model_path, max_outputs):
        self.reap = BartForConditionalGeneration.from_pretrained(model_path)
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
        self.max_outputs = max_outputs

        self.reap.to("cuda")

    def generate(self, inputs):
        encoding = self.tokenizer.batch_encode_plus(
            inputs, return_tensors="pt"
        )
        input_ids, attention_masks = (
            encoding["input_ids"],
            encoding["attention_mask"],
        )

        input_args = {
            "input_ids": input_ids.to("cuda"),
            "attention_mask": attention_masks.to("cuda"),
            "num_beams": 6,
            "length_penalty": 2,
            "no_repeat_ngram_size": 3,
            "max_length": 100,
            "min_length": 5,
            "decoder_start_token_id": self.tokenizer.bos_token_id,
            "num_return_sequences": 1,
            "return_dict_in_generate": True,
            "output_scores": True,
        }

        generation_output = self.reap.generate(**input_args)

        generations = [
            self.tokenizer.decode(
                generation_output.sequences[i],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )
            for i in range(generation_output.sequences.shape[0])
        ]
        generations = [g.strip() for g in generations]

        return generations

    def get_transformations(self, sentence, reorderings):
        sentence_text = sentence.sent.lower()
        reapified_inputs = self.reapify_inputs(sentence_text, reorderings)
        outputs = self.generate(reapified_inputs)
        return outputs

    @staticmethod
    def get_rearragement(line, order):
        assert len(line) == len(order), "input file error"

        line_rearraged = [None] * len(line)
        for idx, o in enumerate(order):
            line_rearraged[o] = line[idx]

        line_rearraged = " ".join(line_rearraged)
        return line_rearraged

    @staticmethod
    def reapify_inputs(sentence_text, reorderings):
        reapified_inputs = []
        sentence_tokens = sentence_text.split(" ")
        for r in reorderings:
            order = r[2]
            rearranged_input = reapModel.get_rearragement(
                sentence_tokens, order
            )
            reapified_inputs.append(
                f"{sentence_text} <SEP> {rearranged_input}"
            )
        return reapified_inputs
