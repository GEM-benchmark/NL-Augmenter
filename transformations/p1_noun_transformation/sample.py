from transformations.p1_noun_transformation import AddNounDefinition

tf = AddNounDefinition()
sentence = "Andrew finally returned the French book to Chris that I bought last week".lower()
print(tf.generate(sentence))
