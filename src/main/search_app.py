from utils.common_utils import get_query_key, get_html_template_folder_path, get_test_index_name
from flask import Flask
from analyze_text.text_preprocessor import  TextPreprocessor
from  index_setup.index_creator import BaseIndexCreator
from index_setup.index_populator import BaseIndexPopulator


app = Flask(__name__, template_folder=get_html_template_folder_path())

def prepare_index() -> str:
    # todo: use the dependency injection framework, to fetch singleton object, and avoid instantiation
    index_creator = BaseIndexCreator()
    index_name = index_creator.get_base_index_name()
    return index_name

@app.route("/")
def hello_world():

    file = open(f"{get_html_template_folder_path()}\\AzSearch.html", "r")

    content: str = str(file.read())

    content = (content
               .replace("{{{queryKey}}}",get_query_key())

               .replace("{{{indexName}}}",prepare_index()))

    print(content)

    return content

