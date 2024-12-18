from utils.common_utils import get_query_key, get_html_template_folder_path, get_test_index_name
from flask import Flask


app = Flask(__name__, template_folder=get_html_template_folder_path())

@app.route("/")
def hello_world():

    file = open(f"{get_html_template_folder_path()}\\AzSearch.html", "r")

    content: str = str(file.read())

    content = (content
               .replace("{{{queryKey}}}",get_query_key())
               .replace("{{{indexName}}}",get_test_index_name()))

    print(content)

    return content

