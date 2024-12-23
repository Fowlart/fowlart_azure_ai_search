from src.analyze_text.text_preprocessor import  TextPreprocessor
from  src.index_setup.index_creator import BaseIndexCreator
from src.index_setup.index_populator import BaseIndexPopulator
import nltk

def run():

    preprocessor = TextPreprocessor()

    index_creator = BaseIndexCreator()

    index_populator = BaseIndexPopulator(
        index_name=index_creator.get_base_index_name(),
        path_to_content_root=preprocessor.path_to_text_bucket
    )

    try:
        preprocessor.preprocess_files()
    except (LookupError) as e:
        print("Downloading nltk libs...")
        nltk.download('punkt')
        nltk.download('punkt_tab')
        preprocessor.preprocess_files()

    index_creator.create_index()

    index_populator.populate_index()

if __name__=="__main__":

    run()