from analyze_text.text_preprocessor import  TextPreprocessor
from  index_setup.index_creator import BaseIndexCreator
from index_setup.index_populator import BaseIndexPopulator

def run():

    preprocessor = TextPreprocessor()
    index_creator = BaseIndexCreator()
    index_populator = BaseIndexPopulator(index_name=index_creator.get_base_index_name())
    preprocessor.preprocess_files()

    index_creator.create_index()

    print(index_populator.retrieve_files_metadata(root_dir=preprocessor.path_to_text_bucket))

if __name__=="__main__":

    run()