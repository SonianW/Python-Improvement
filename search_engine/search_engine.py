# %%%%% import
import re

# %%%%% class
class SearchEngineBase(object):
    def __init__(self):
        pass

    def add_corpus(self, file_path):
        with open(file_path, "r") as f:
            text = f.read()
        self.process_corpus(file_path, text)

    def process_corpus(self, id, text):
        raise Exception("process_corpus not implemented.")

    def search(self, query):
        raise Exception("search not implemented")


class SimpleEngine(SearchEngineBase):
    def __init__(self):
        super(SimpleEngine, self).__init__()
        self.__id_to_texts = {}

    def process_corpus(self, id, text):
        self.__id_to_texts[id] = text

    def search(self, query):
        results = []
        for id, text in self.__id_to_texts.items():
            if query in text:
                results.append(id)
        return results


class BOWEngine(SearchEngineBase):
    def __init__(self):
        super(BOWEngine, self).__init__()
        self.__id_to_words = {}

    def process_corpus(self, id, text):
        self.__id_to_words[id] = self.parse_text_to_words(text)

    def search(self, query):
        query_words = self.parse_text_to_words(query)
        results = []
        for id, words in self.__id_to_words.items():
            if self.query_match(query_words, words):
                results.append(id)
        return results

    @staticmethod
    def query_match(query_words, words):
        for word in query_words:
            if not word in words:
                return False
        return True

    @staticmethod
    def parse_text_to_words(text):
        text = re.sub(r"[^\w]", " ", text)
        text = text.lower()
        word_list = text.split(" ")
        word_list = filter(None, word_list)
        return set(word_list)

class BOWInvertedIndexEngine(SearchEngineBase):
    def __init__(self):
        super(BOWInvertedIndexEngine, self).__init__()
        self.inverted_index = {}
    
    def process_corpus(self, id, text):
        words = self.parse_text_to_words(text)
        for word in words:
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word].append(id)

    def search(self, query):
        query_words = list(self.parse_text_to_words(query))
        query_words_index = list()
        for query_word in query_words:
            query_words_index.append(0)

        for query_word in query_words:
            if query_word not in self.inverted_index:
                return []
        
        result = []
        while True:
            current_ids = []

            for idx, query_word in enumerate(query_words):
                current_index = query_words_index[idx]
                current_inverted_list = self.inverted_index[query_word]
            
                if current_index >= len(current_inverted_list):
                    return result

                current_ids.append(current_inverted_list[current_index])

            if all(x == current_ids[0] for x in current_ids):
                result.append(current_ids[0])
                query_words_index = [x + 1 for x in query_words_index]
                continue

            min_val = min(current_ids)
            min_val_pos = current_ids.index(min_val)
            query_words_index[min_val_pos] += 1

    @staticmethod
    def parse_text_to_words(text):
        text = re.sub(r"[^\w]", " ", text)
        text = text.lower()
        word_list = text.split(" ")
        word_list = filter(None, word_list)
        return set(word_list)

# %%%%% test code
def main(search_engine):
    for file_path in [
        "./corpus/1.txt",
        "./corpus/2.txt",
        "./corpus/3.txt",
        "./corpus/4.txt",
        "./corpus/5.txt",
    ]:
        search_engine.add_corpus(file_path)

    while True:
        query = input()
        results = search_engine.search(query)
        print("found {} result(s):".format(len(results)))
        for result in results:
            print(result)


search_engine = BOWInvertedIndexEngine()
main(search_engine)
