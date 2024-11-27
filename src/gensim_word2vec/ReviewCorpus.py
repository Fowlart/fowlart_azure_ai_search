import polars as pl
from src.utils.common_utils import get_tokens, get_search_index_client, get_path_to_example_data
from src.utils.common_utils import  analyze_text, get_tokens, get_search_index_client, get_index_name


class ReviewsCorpus:

    """An iterator that yields sentences (lists of str)."""

    def __init__(self,
            number_of_records: int,
            minimal_review_length: int
            ):

        self.number_of_records = number_of_records
        self.minimal_review_length = minimal_review_length

        df = (pl.read_delta(source=get_path_to_example_data()))

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
                             index_name=get_index_name(),
                             client=get_search_index_client())
            print(f"Result is: {result}")

            yield result