from ranker import Ranker
import numpy as np
import utils

# DO NOT MODIFY CLASS NAME
from spell_checker import SpellCChecker


class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model
        self.spell_checker = SpellCChecker()


    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        query_as_list, entities = self._parser.parse_sentence(query)
        entities = entities.keys()
        query_as_list.extend(entities)
        query_expand = []

        keys = self._indexer.inverted_idx.keys()

        query_expand = []
        if self._model.__class__.__name__ == 'GlobalMethod':
            self._model.execute_global_method_and_generate_matrix(inverted_index=self._indexer.inverted_idx,
                                                         postingDic=self._indexer.postingDict)

        for word in query_as_list:
            temp_words = self._model.expand_query(word)
            for inner_word in temp_words:
                if inner_word in keys and inner_word not in query_expand:
                    query_expand.append(str(inner_word))

        for term in query_as_list:
            if term in keys and term not in query_expand:
                query_expand.append(str(term))
            elif term.upper() in keys and term not in query_expand:
                query_expand.append(str(term.upper()))
            elif term.lower() in keys and term not in query_expand:
                query_expand.append(str(term.lower()))

        relevant_docs = self._relevant_docs_from_posting(query_expand)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs)
        n_relevant = len(ranked_doc_ids)
        return n_relevant, ranked_doc_ids

    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        index = 0
        dict_tweet_tfidf = {}
        for term in query_as_list:
            dic_tweets = self._indexer.get_term_posting_list(term)
            list_terms = []
            for tweet in dic_tweets:

                try:
                    tf_idf = float(tweet[2]) * float(self._indexer.inverted_idx[term][1])
                except:
                    continue
                if tweet[0] not in dict_tweet_tfidf.keys():
                    dict_term_tfidf = {}
                    for term_inner in query_as_list:
                        dict_term_tfidf[term_inner] = float(0)

                    list_terms.append(dict_term_tfidf)
                    list_terms[0][term] = tf_idf
                    dict_tweet_tfidf[tweet[0]] = list_terms

                    dict_tweet_tfidf[tweet[0]] = list(list_terms)

                else:
                    exist_list = dict_tweet_tfidf[tweet[0]]
                    for dict_list in exist_list:
                        dict_list[term] += tf_idf
                list_terms.clear()

            index += 1
            # dic_tweets.clear()
        dict_query = {}
        for term in query_as_list:
            if term not in dict_query.keys():
                dict_query[term] = 1
            else:
                dict_query[term] += 1

        numpy_array_query = np.array(list(dict_query.values()))
        index = 0
        relevant_docs = {}
        keys = list(dict_tweet_tfidf.keys())
        for list_values in dict_tweet_tfidf.values():
            numpy_array_doc = np.array(list(list_values[0].values()))
            multiply_vectors = np.dot(numpy_array_query, numpy_array_doc)
            relevant_docs[keys[index]] = multiply_vectors
            index += 1
        return relevant_docs
