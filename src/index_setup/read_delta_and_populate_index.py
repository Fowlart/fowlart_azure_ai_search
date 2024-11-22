import numpy
import polars as pl
from azure.search.documents.indexes._search_index_client import SearchClient
from src.utils.common_utils import get_search_client, key_phrase_extraction, get_search_index_client
from utils.common_utils import authenticate_text_analytics_client, analyze_text, get_tokens
import gensim
import gensim.downloader as api
import numpy as np
from src.utils.common_utils import bcolors as c


def _update_to_index(data: list[dict], searchClient: SearchClient):

    for doc in data:
        print(doc)

    upload_results = searchClient.upload_documents(data)

    for result in upload_results:
        print(result)


if __name__ == "__main__":

    df = (pl.read_delta(source=r'C:\Users\Artur.Semikov'
                               r'\PycharmProjects\FowlartAiSearch'
                               r'\resources\733d79e5-b388-4186-94de-146127ae7a61'))

    print(df.collect_schema())


    jsons: list[dict] = (df
                         .head(100)
                         .select("review_id","review_rating","review_text")
                         .filter(pl.col("review_text").str.len_chars()>100)
                         .rename({"review_id":"id",
                                  "review_rating":"ReviewRating",
                                  "review_text":"ReviewText"})
                         .cast({"ReviewRating":pl.Int32})
                         .to_dicts())

    print(f"Number of reviews: {len(jsons)}")

    text_analytics_client = authenticate_text_analytics_client()

    search_client = get_search_client("fowlart_product_review_hybrid")



    trained_model = gensim.models.Word2Vec.load(r"C:\Users"
                                                r"\Artur.Semikov"
                                                r"\PycharmProjects"
                                                r"\FowlartAiSearch\resources\gensim-models\main-model.txt").wv


    trained_model = api.load('word2vec-google-news-300')

    search_index_client = get_search_index_client()

    # will mutate the original jsons
    for x in jsons:

        key_phrases = key_phrase_extraction(x["ReviewText"],text_analytics_client)

        x["KeyPhrases"]= key_phrases

        # Average of Word2Vec vectors : You can just take the average of all the word vectors in a sentence.
        # This average vector will represent your sentence vector.

        review_tokens = get_tokens(x["ReviewText"],analyzer_name="en.microsoft",
                             index_name="fowlart_product_review_hybrid",
                             client=search_index_client)

        sentence_vector_list: list[numpy.ndarray] = []

        for token in review_tokens:
            try:
                sentence_vector_list.append(trained_model[token])
            except KeyError:
             print(c.WARNING)
             print(f"The token `{token}` does not appear in this model")
             print(c.ENDC)

        average_vector: np.ndarray = np.mean(sentence_vector_list, axis=0)

        print(f"Created vector for review with the shape {average_vector.shape}")

        x["ReviewTextVector"] = average_vector.tolist()

    print(jsons)

    _update_to_index(jsons,search_client)