from nltk.corpus import wordnet

class WordNet:
    def __init__(self):
        pass

    def expand_query(self,term):
        #synonyms = []
        antonyms = []
        words_to_add = []
        syns = wordnet.synsets(term)
        for syn in syns:
            for l in syn.lemmas():
                words_to_add.append(l.name())
        return words_to_add
