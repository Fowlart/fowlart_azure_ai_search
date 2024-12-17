from analyze_text.text_preprocessor import  TextPreprocessor
from  index_setup.index_creator import BaseIndexCreator

def run():
    preprocessor = TextPreprocessor()
    index_creator = BaseIndexCreator()
    preprocessor.preprocess_files()
    index_creator.create_index()

if __name__=="__main__":
    run()