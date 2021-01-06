import os
import pandas as pd
import json
from collections import Counter
from indexer import Indexer

class GlobalMethod:

    def __init__(self):
        self.inverted_index=None
        self.postingDic=None
        self.matrix=pd.DataFrame()
        # self.path=path


    def execute_global_method_and_generate_matrix(self,inverted_index,postingDic):
        self.inverted_index=inverted_index
        self.postingDic=postingDic
        path = os.path.dirname(os.path.abspath(__file__))
        file =path+'\\Global_method_matrix.json'
        if os.path.isfile(file) :
            return self.load_json_to_df()
        average_freq = int(self.calculate_average_of_frequency()*20)
        print(average_freq)
        columns = []
        dic_of_designated_terms ={}
        for term in self.inverted_index.keys():
            num_of_freq = int(self.inverted_index[term][0])
            if num_of_freq > average_freq:
                # dict_of_term = Indexer.get_details_about_term_in_inverted_index(term=term,inverted_index=self.inverted_index)
                # details_dic_in_inverted_index=Indexer.get_values_in_posting_file_of_dictionary_term(term=term,pointer=dict_of_term['pt'],path=self.path)
                details_dic_in_inverted_index=self.postingDic[term]
                columns.append(term)
                dic_of_designated_terms[term]= {}
                dic_of_designated_terms[term]= details_dic_in_inverted_index
        df = pd.DataFrame(index=columns, columns=columns)
        for column in columns:
            for row in columns:
                df[row][column]=-1
        for column in columns:
            dic_with_tweet_id_col = dic_of_designated_terms[column]
            temp_list_tweet_id_row = []
            for row in columns:
                if df[row][column]!=-1:continue
                dic_with_tweet_id_row = dic_of_designated_terms[row]
                dic_temp ={}
                # keys_1=dic_with_tweet_id_row.keys()
                keys_1=[]
                for key in dic_with_tweet_id_row:
                    keys_1.append(key[0])
                # keys_2=dic_with_tweet_id_col.keys()
                keys_2=[]
                for key in dic_with_tweet_id_col:
                    keys_2.append(key[0])

                keys_dic_temp=[]
                mutual_list=[]
                for tweet in keys_1:
                    temp_list_tweet_id_row.append(tweet)
                    # dic_temp[tweet]=1
                    keys_dic_temp.append(tweet)


                # keys_dic_temp = dic_temp.keys()
                # for key in keys_dic_temp:

                for tweet in keys_2:
                    if tweet in keys_dic_temp:
                        mutual_list.append(tweet)
                temp_list_tweet_id_row.clear()
                temp_list_tweet_id_row=list()
                sigma = 0
                for item in mutual_list:
                    item = str(item)
                    column = str(column)
                    row = str(row)
                    try:
                        first=0
                        second=0
                        for tuple in dic_of_designated_terms[row]:
                            if item ==tuple[0]:
                                first=tuple[1]
                                break
                        for tuple in dic_of_designated_terms[column]:
                            if item ==tuple[0]:
                                second=tuple[1]
                                break
                        sigma += int(first) * int(second)
                    except:
                        print("error")
                        continue
                freq_row = int(self.inverted_index[row][0])**2
                freq_col= int(self.inverted_index[column][0])**2
                val = self.calculate_frequency_and_normalize(c_i_j=int(sigma),
                                                             c_i_i=int(freq_row),
                                                             c_j_j=int(freq_col))
                df[row][column] = val
                df[column][row] = val

        df.to_json('Global_method_matrix.json')
        print(df)
    def calculate_frequency_and_normalize(self, c_i_j, c_i_i, c_j_j):
        down = (c_i_i) + (c_j_j) - c_i_j
        return c_i_j / down
    def calculate_average_of_frequency(self):
        keys = self.inverted_index.keys()
        sum=0
        number_of_terms=len(keys)
        for key in keys :
            sum+=int(self.inverted_index[key][0])
        return int(sum/number_of_terms)
    def load_json_to_df(self):
        path = os.path.dirname(os.path.abspath(__file__))
        file =path+'\\Global_method_matrix.json'
        with open(file) as train_file:
            data = json.load(train_file)
            self.matrix = pd.DataFrame.from_dict(data, orient='columns')
        return self.matrix
    def expand_query(self,term):
        dic={}
        columns = self.matrix.columns
        for column in self.matrix.columns:
            if term==column:
                for row in self.matrix.columns:
                    if row==column:
                        continue
                    dic[row]=self.matrix[column][row]
                sorted_d = sorted((value, key) for (key, value) in dic.items())
                sorted_d.reverse()
                words =""
                index =0
                for word in sorted_d[0:1]:
                    if index==0:
                        words=str(word[1])
                    else:
                        words +=" "+str(word[1])
                    index+=1
                return words.split(" ")
        return []

