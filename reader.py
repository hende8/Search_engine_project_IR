import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()
    def get_all_path_of_parquet(self):
        pathes =[]
        for filename in os.listdir(self.corpus_path):
            if filename.endswith(".parquet"):
                pathes.append([self.corpus_path+"\\",filename])
            elif os.path.isdir(self.corpus_path + '\\' + filename):
                for filenameParquet in os.listdir(self.corpus_path + '\\' + filename):
                    if filenameParquet.endswith(".parquet"):
                        temp_folder_path = self.corpus_path
                        self.corpus_path = self.corpus_path + '\\' + filename
                        pathes.append([self.corpus_path ,filenameParquet])
                        self.corpus_path = temp_folder_path
            else:
                continue
        return pathes
    def get_documents(self,path,filename):
        full_path = os.path.join(path, filename)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()