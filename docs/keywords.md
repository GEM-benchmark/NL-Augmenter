  # NL-Augmenter Keywords

Every transformation should have keywords that identify the type of transformation that is being written. The following list can be used as reference.
- the type of linguistic change that the transformation is attempting eg. morphological, lexical, syntactic, word-order, discourse, noise etc.
- the type of algorithm that is written eg. rule-based, model-based, api-based, external-knowledge-based, transformer-based, parser-based, etc.
- the naturalness of the generation eg. natural-sounding, natural-looking, unnatural, etc.
- the potential accuracy & precision of the generation eg. high-precision, high-coverage, etc.
- the text-specific modality being covered (if applicable) eg. visual, aural, written, etc.
- the skills required to differentiate between the input and the output of the transformation (if applicable) eg. causal-reasoning, visual-reasoning, social-reasoning, humor, figurative-language, grammar, world-knowledge, etc. 
- other transformation specific keywords

Some of the categories can be subjective and they are meant to be used as best estimated. It is okay to include multiple of each type. Example, many transformer based generators might fit into most of the linguistic categories.  If your transformation is best described by keywords not yet included in the list below, please add the additional keywords to this file as part of your pull request.

Keyword | Description
------- | -----------
**Type of Linguistic Change** |
  `morphological` | character level or inflectional/morphological changes
  `lexical` | the transformation substitutes different words or phrases
  `syntactic` | the transformation changes the syntax of the input (eg. active to passive)
  `word-order` | if the order of the words or phrases is changed (eg. topicalisation, changing the order of semantic roles)
  `discourse` | operating on or generating units of language longer than a sentence (eg. paragraph, multiple utterances in a dialog setting, etc)
  `noise` | The generation adds random noise which would perturb the examples (eg. removing punctuations, changing case, repeating words/characters)
**Type of algorithm** |
  `rule-based` | if the implementation uses a heuristic or rules based approach
  `model-based` | if the implementation uses a machine learning model
  `api-based` | if the implementation uses an external api or tool
  `external-knowledge-based` | if the implementation uses a corpora, a separate knowledge base, etc.
  `transformer-based` | if the implementation uses a transformer based model (eg. BERT, T5)
  `parser-based` | if the implementation uses any syntactic (dependency, constituency, etc) or shallow semantic parser or other semantic parsers (eg. semantic role labelling)
  `tokenizer` | if the implementation uses a tokenizer
  `chunker` | if the implementation uses a chunker
  `discourse-segmenter` | if the implementation uses a discourse segmenter
**The naturalness of the generation** |
  `unnatural-sounding` | if the generations might not sound natural eg. if synthesized to speech, would they not sound natural as their source sentences. Eg, adding noun definitions might make the sentence factually correct but people might not use the same language while speaking.  
  `unnatural-looking` | generations in written format which might not look natural to a reader. homophonic translations, filler words
**The potential accuracy & precision of the generation** | 
  `high-precision` | The transformation generates what it intends to generate
  `low-precision` | The transformation sometimes does not generate what it intends to generate (eg. often changes meaning)
  `low-coverage` | The transformation might not return an output for all types of inputs but only a handful of inputs
  `high-coverage` | The transformation can return an output for almost all types of inputs
  `high-generations` | The transformation generates a lot of (possibly diverse) outputs for a single input (eg beam search or substitutions with large number of alternate choices)
  `low-generations` | The transformation generates few outputs for a single input (substitution with lesser number of alternate choices)
**The text-specific modality being addressed (if applicable)** |
  `visual` | The outputs are visually similar to the inputs (eg. Leet letters)
  `aural` | The outputs sound similar to the inputs (eg. homophones)
  `written` | The transformation makes font changes, or changes which would look different in different written formats
**The skills required to differentiate between the input and the output of the transformation (if applicable)** |
  `causal-reasoning` | ability to reason about cause and effect
  `visual-reasoning` | ability to reason by the appearance of the text
  `social-reasoning` | ability to understand and reason about human social interactions
  `figurative-language` | ability to understand figures of speech
  `world-knowledge` | ability to understand world knowledge
  
