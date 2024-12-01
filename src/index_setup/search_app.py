from utils.common_utils import get_query_key

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():

    return f"<p>{get_query_key()}</p>"

