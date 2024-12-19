from analyze_text.text_preprocessor import  TextPreprocessor
from  index_setup.index_creator import BaseIndexCreator
from index_setup.index_populator import BaseIndexPopulator

def run():

    preprocessor = TextPreprocessor()

    index_creator = BaseIndexCreator()

    index_populator = BaseIndexPopulator(
        index_name=index_creator.get_base_index_name(),
        path_to_content_root=preprocessor.path_to_text_bucket
    )

    preprocessor.preprocess_files()

    index_creator.create_index()

    index_populator.populate_index()

if __name__=="__main__":

    run()