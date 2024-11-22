import polars as pl
from src.utils.common_utils import get_tokens, get_search_index_client


class ReviewsCorpus:

    """An iterator that yields sentences (lists of str)."""

    def __init__(self,
            number_of_records: int,
            minimal_review_length: int
            ):

        self.number_of_records = number_of_records
        self.minimal_review_length = minimal_review_length

        df = (pl.read_delta(source=r'C:\Users\Artur.Semikov'
                                   r'\PycharmProjects\FowlartAiSearch'
                                   r'\resources\733d79e5-b388-4186-94de-146127ae7a61'))

        jsons: list[dict] = (df
        .head(number_of_records)
        .select("review_text")
        .filter(pl.col("review_text").str.len_chars() > minimal_review_length)
        .to_dicts())

        print(f"Retrieved number of customer reviews to processing: {len(jsons)}")

        self.reviews_dict = jsons

    def __iter__(self):

        for element in self.reviews_dict:
            text = element["review_text"]
            print(f"Tokenizing: {text} ")
            result = get_tokens(text=text,
                             analyzer_name="en.microsoft",
                             index_name="fowlart_product_review_hybrid",
                             client=get_search_index_client())
            print(f"Result is: {result}")

            yield result