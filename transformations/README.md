### The List of Transformations

This directory contains transformations that are part of the Natural Language Augmenter (NL-Augmenter). Each subdirectory contains a single transformation (or a filter for a contrast set). A summary table of these transformation follows.

| Transformation                             | Description                                                                       
| ------- | -----------                          
| [back_translation](back_translation)              | Converts an English sentence to German and back to English                
| [butter_fingers_perturbation](butter_fingers_perturbation)     | Adds noise to all types of text sources (sentence, paragraph, etc.) proportional to noise emanating from keyboard typos making common spelling errors.  
| [change_person_named_entities](change_person_named_entities)        | Changes person named entities: Alex travels to the city everyday! --> Jacob travels to the city everyday! 
| [change_two_way_ne](change_two_way_ne)                   | Changes the named entity in the source sentence and reflects the same change in the target sentence. Benefits Machine Translation tasks.
| [longer_names_ner](longer_names_ner)        | Elongates person names: Russel Peters is a comedian. --> Russel J. M. Peters is a comedian.  
| [without_punctuation](punctuation)        | Hello Sam, how are you? --> hello sam how are you
| [replace_numerical_values](replace_numerical_values)        | Changes numerical values. Jason's 3 sisters want to move back to India --> Jason's 6 sisters want to move back to India
| [redundant_context_for_qa](redundant_context_for_qa)        | Duplicates the context in a QA setting. (context, question, short-answer) --> (context+context, question, short-answer)
