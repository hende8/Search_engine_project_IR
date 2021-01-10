from datetime import datetime

import search_engine_best
from reader import ReadFile
import PySimpleGUI as sg


from configuration import ConfigClass


sg.ChangeLookAndFeel('Black')


class GUI:
    ''' Create a GUI object '''

    def __init__(self):
        self.layout: list = [
            [sg.Text('Any thoughts?', size=(11, 1)),
             sg.Input(size=(40, 1), focus=True, key="TERM")],
            [sg.Button('Search', size=(10, 1), bind_return_key=True, key="_SEARCH_")],
            [sg.Output(size=(100, 30), key = '_output_')]]

        self.window: object = sg.Window('DBM Search Engine', self.layout, element_justification='left')

    def clear(self):
        self.window.FindElement('_output_').Update('')

class Search_Engine:
    ''' Create a search engine object '''

    def __init__(self):
        self.file_index = []  # directory listing returned by os.walk()
        self.results = []  # search results returned from search method

    def search(self, query):
        ''' Search for the term based on the type in the index; the types of search
            include: contains, startswith, endswith; save the results to file '''
        self.results.clear()
        self.matches = 0
        self.records = 0
        relevant_res, tweet_id = search_engine_best.SearchEngine.search(query)
        # save results to file
        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')


def main():
    ''' The main loop for the program '''
    config = ConfigClass()
    se = search_engine_best.SearchEngine(config=config)
    r = ReadFile(corpus_path=config.get__corpusPath())
    # parquet_file_path =r.get_all_path_of_parquet()[0][0]+r.get_all_path_of_parquet()[0][1]
    # se.build_index_from_parquet(parquet_file_path)
    se.load_index('idx_bench')
    g = GUI()

    # s.load_existing_index()  # load if exists, otherwise return empty list

    while True:
        event, values = g.window.read()

        if event is None:
            break

        if event == '_SEARCH_':
            g.clear()
            query = values['TERM']
            start = datetime.now()
            relevant, tweets_id = se.search(query)
            end = datetime.now()
            total_time = (end - start).total_seconds()
            # print the results to output element
            index = 0
            for tweet_id in tweets_id:
                if index < 25:
                    print("%s. tweet id: %s"%(index+1,tweet_id))
                index += 1

            print()
            print("About %s tweets (%s seconds)"%(relevant, total_time))

if __name__ == '__main__':
    main()
