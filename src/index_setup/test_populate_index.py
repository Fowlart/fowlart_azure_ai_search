import numpy
import polars as pl
from azure.search.documents.indexes._search_index_client import SearchClient
from src.utils.common_utils import get_search_client, extract_key_phrases, get_search_index_client, \
    get_path_to_gensim_model, get_path_to_example_data
from utils.common_utils import get_text_analytics_client, analyze_text, get_tokens, get_index_name
import gensim
import numpy as np
from src.utils.common_utils import bcolors as c


def _update_to_index(data: list[dict], s_client: SearchClient):

    for doc in data:
        print(doc)

    upload_results = s_client.upload_documents(data)

    for result in upload_results:
        print(result)

def populate_index() -> None:

    df = (pl.read_delta(source=get_path_to_example_data()))

    print(df.collect_schema())


    jsons: list[dict] = (df
                         .head(100)
                         .select("review_id","review_rating","review_text","product_title")
                         .filter(pl.col("review_text").str.len_chars()>100)
                         .rename({"review_id":"id",
                                  "product_title": "ProductTitle",
                                  "review_rating":"ReviewRating",
                                  "review_text":"ReviewText"})
                         .cast({"ReviewRating":pl.Int32})
                         .to_dicts())

    print(f"Number of reviews: {len(jsons)}")

    text_analytics_client = get_text_analytics_client()

    search_client = get_search_client()


    trained_model = gensim.models.Word2Vec.load(get_path_to_gensim_model()).wv

    # todo: decide, what model is more effective
    # trained_model = api.load('word2vec-google-news-300')

    search_index_client = get_search_index_client()

    # will mutate the original jsons
    for x in jsons:

        key_phrases = extract_key_phrases(x["ReviewText"], text_analytics_client)

        x["KeyPhrases"]= key_phrases

        review_tokens = get_tokens(x["ReviewText"],
                             analyzer_name="en.microsoft",
                             index_name=get_index_name(),
                             client=search_index_client)

        sentence_vector_list: list[numpy.ndarray] = []

        for token in review_tokens:
            try:
                sentence_vector_list.append(trained_model[token])
            except KeyError:
             print(c.WARNING)
             print(f"The token `{token}` does not appear in this model")
             print(c.ENDC)

        # Average of Word2Vec vectors :
        # You can just take the average
        # of all the word vectors in a sentence.
        # This average vector will represent your sentence vector.
        average_vector: np.ndarray = np.mean(sentence_vector_list, axis=0)

        print(f"Created vector for review with the shape {average_vector.shape}")

        x["ReviewTextVector"] = average_vector.tolist()

    print(jsons)

    _update_to_index(jsons,search_client)