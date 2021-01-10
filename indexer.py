# DO NOT MODIFY CLASS NAME
import math

import utils
import collections
class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.number_of_documents=0

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        self.number_of_documents += 1
        for term in document_dictionary.keys():
            if term==document.tweet_id:continue
            tf = round(document_dictionary[term] / document.doc_length, 4)
            tf_in_doc = document_dictionary[term]
            is_term_upper=False
            try:
                # Update inverted index and posting
                keys= self.inverted_idx.keys()
                if term[0].islower() :
                    if term not in keys:
                        self.inverted_idx[term] = 1
                        self.postingDict[term] = []
                    else:
                        self.inverted_idx[term] += 1
                else:
                    if 'A' <= term[0] <= 'Z':
                        term_upper = term.upper()
                    else:
                        term_upper = term
                    if term_upper in keys:
                        self.inverted_idx[term_upper] += 1
                        is_term_upper=True
                    else:
                        # first occurrence of word with capital letter
                        if term_upper not in keys:
                            self.inverted_idx[term_upper] = 1
                            self.postingDict[term_upper] = []
                            is_term_upper=True
                        else:
                            self.inverted_idx[term_upper] += 1
                            is_term_upper=True

                if is_term_upper:
                    self.postingDict[term_upper].append((document.tweet_id, document_dictionary[term],tf))
                else:
                    self.postingDict[term].append((document.tweet_id, document_dictionary[term],tf))
            except:
                print('problem with the following key {}'.format(term))

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        if ".pkl" in fn:
            fn=fn[:-4]
        origin_dict = utils.load_obj(fn)
        self.postingDict=origin_dict['posting_file']
        self.inverted_idx=origin_dict['inverted_index']
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """

        dict_of_inverted_and_posting={}
        dict_of_inverted_and_posting['inverted_index']=self.inverted_idx
        dict_of_inverted_and_posting['posting_file']=self.postingDict
        utils.save_obj(dict_of_inverted_and_posting,fn)

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.postingDict.keys()

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.postingDict[term] if self._is_term_exist(term) else []
    def sort_inverted_index(self):
        '''
        sorting an inverted index
        :return:
        '''
        self.inverted_idx = collections.OrderedDict(sorted(self.inverted_idx.items()))
    def sort_posting_file(self):
        '''
        sorting an posting file dictionary
        :return:
        '''
        self.postingDict = collections.OrderedDict(sorted(self.postingDict.items()))
    def add_idf_to_dictionary(self):
        '''
        add idf metric to the dictionary
        :return:
        '''
        for word in self.inverted_idx.keys():
            idf = math.log10(self.number_of_documents/int(self.inverted_idx[word]))
            self.inverted_idx[word] = (self.inverted_idx[word],idf)

    def sort_100K_inverted_index(self):
        '''
        sort
        :return: dictionary that limited to 100K words
        '''
        temp_dic = {k: v for k, v in sorted(self.inverted_idx.items(), key=lambda item: item[1], reverse=True)}
        n_items =  {k: temp_dic[k] for k in list(temp_dic)[:100000]}
        return n_items