import polars as pl
from azure.search.documents.indexes._search_index_client import SearchClient
from src.utils.common_utils import get_search_client, key_phrase_extraction
from utils.common_utils import authenticate_text_analytics_client


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

    for x in jsons:
        x["KeyPhrases"]=key_phrase_extraction(x["ReviewText"],text_analytics_client)
        _update_to_index([x],search_client)