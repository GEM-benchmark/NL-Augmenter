# 1. get the subjects + objects
# 2. infer if the word is masculine or feminine (if it is not a proper noun)
# 3. get the word2vec for it, add the Man vector, 
#    # use tensorflow, pytorch, or keras?
#       Ideas for how to infer existing gender
#   1. translate to a romance language, and take the gender of that
#   2. add man, add woman, see if either of them don't change.
# taken from https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py

if __name__ == "__main__":
    wv, nlp = load()
    text = ("When Sebastian Thrun started working on self-driving cars at "
            "Google in 2007, few people outside of the company took him "
            "seriously. I can tell you very senior CEOs of major American "
            "car companies would shake my hand and turn away because I wasn’t "
            "worth talking to,” said Thrun, in an interview with Recode earlier "
            "this week.")
    
    doc = nlp(text)
    
    for sent in doc.sents:
        print(sent)
        gender_benders = generate_sentences(str(sent), wv, nlp)
        for gender_bender in gender_benders:
            print("\t" + gender_bender)
