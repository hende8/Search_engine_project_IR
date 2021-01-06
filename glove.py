import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

embeddings_dict = {}


class Glove:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self):

        print("initiate glove ")
        self.embeddings_dict={}
        with open("glove.twitter.27B.25d.txt", 'r', encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], "float32")
                self.embeddings_dict[word] = vector

        # f.close()

    def find_closest_embeddings(self,embedding):
        print("finding closest words")

        #return sorted(embeddings_dict.keys(),key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding))
        distance_dic = {}
        shape_embedding = embedding.shape[0]
        for word in self.embeddings_dict:
            if shape_embedding != self.embeddings_dict[word].shape[0]:
                continue
            distance_dic[word] = spatial.distance.euclidean(self.embeddings_dict[word], embedding)
        sorted_dict = {k: v for k, v in sorted(distance_dic.items(), key=lambda item: item[1])}

        i = 0
        list_result = []
        for word in sorted_dict.keys():
            if i > 0: break
            if np.array_equal(self.embeddings_dict[word],embedding): continue
            list_result.append(word)
            i += 1
        return list_result

    def expand_query(self,term):
        embedded = self.embeddings_dict.get(term)
        if term not in self.embeddings_dict:
            return []
        return self.find_closest_embeddings(embedded)
