import gensim.downloader as api
import polars as pl
from utils.common_utils import get_text_analytics_client, extract_key_phrases, get_path_to_example_data
from src.utils.common_utils import bcolors as c

if __name__ =="__main__":

    wv = api.load('word2vec-google-news-300')

    text_analytics_client = get_text_analytics_client()

    jsons: list[dict] = (pl.read_delta(source=get_path_to_example_data())
                         .head(100)
                         .select("review_id", "review_rating", "review_text")
                         .filter(pl.col("review_text").str.len_chars() > 100)
                         .to_dicts())

    for x in jsons:

        keyPhrases = extract_key_phrases(x["review_text"], text_analytics_client)
        print(f"Analyzed key-phrases list: {keyPhrases}")
        for w in keyPhrases:
            print(f"Finding vector for `{w}`")
            try:
             print(wv[w].shape)
            except KeyError:
             print(c.WARNING)
             print(f"The word `{w}` does not appear in this model")
             print(c.ENDC)