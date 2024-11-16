import polars as pl
from src.utils.common_utils import get_search_client

if __name__ == "__main__":

    df = (pl.read_delta(source=r'C:\Users\Artur.Semikov'
                               r'\PycharmProjects\FowlartAiSearch\resources\733d79e5-b388-4186-94de-146127ae7a61'))

    print(df.collect_schema())

    jsons: list[dict] = (df
                         .head(100)
                         .select("review_id","review_rating","review_text")
                         .rename({"review_id":"id",
                                  "review_rating":"ReviewRating",
                                  "review_text":"ReviewText"})
                         .cast({"ReviewRating":pl.Int32})
                         .to_dicts())

    for doc in jsons:
        print(doc)

    client = get_search_client("fowlart_product_review_hybrid")

    upload_results = client.upload_documents(jsons)

    for result in upload_results:
        print(result)