import os

from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models.keyedvectors import KeyedVectors


# embeddings_dict = {}


class Glove:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.

    def __init__(self):
        path_server =  '../../../../glove.twitter.27B.25d.txt'
        glove_input_file = 'glove.twitter.27B.25d.txt'
        word2vec_output_file = 'glove.twitter.27B.25d.txt.word2vec'
        if os.path.isfile('glove.twitter.27B.25d.txt.word2vec') is False:
            glove2word2vec(path_server, word2vec_output_file)
            #
        self._model = KeyedVectors.load_word2vec_format('glove.twitter.27B.25d.txt.word2vec', binary=False)

    def expand_query(self, term):
        try:
            words = self._model.most_similar(term)
            list_word = []
            for word in words:
                list_word.append(word[0])
            return list_word
        except:
            return []
