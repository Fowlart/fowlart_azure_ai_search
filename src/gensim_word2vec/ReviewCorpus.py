import polars as pl
from src.utils.common_utils import get_tokens, get_search_index_client


class ReviewsCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __iter__(self):

        df = (pl.read_delta(source=r'C:\Users\Artur.Semikov'
                                   r'\PycharmProjects\FowlartAiSearch'
                                   r'\resources\733d79e5-b388-4186-94de-146127ae7a61'))

        jsons: list[dict] = (df
                             .head(300)
                             .select("review_text")
                             .filter(pl.col("review_text").str.len_chars() > 100)
                             .to_dicts())


        for element in jsons:
            text = element["review_text"]
            print(f"Tokenizing: {text} ")
            result = get_tokens(text=text,
                             analyzer_name="en.microsoft",
                             index_name="fowlart_product_review_hybrid",
                             client=get_search_index_client())
            print(f"Result is: {result}")

            yield result