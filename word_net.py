import nltk
from nltk.corpus import wordnet
import os
import pandas as pd
import json



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
                # if l.antonyms():
                #     antonyms.append(l.antonyms[0].name())
        return words_to_add
