from search_queries import all_terms_are_present, semantic_search, filter_by_field, simple_search
from src.utils.common_utils import analyze_text, get_search_client

if __name__=="__main__":

    prompt = """
    What is the best products according to users?
    """

    search_client = get_search_client("fowlart_product_review_hybrid")

    analyze_text(text=prompt,
                 analyzer_name="funny_standard_lucene",
                 index_name="fowlart_product_review_hybrid")

    # simple_search(search_client, prompt)

    # how to achieve this? prompt => analyzed_prompt
    analyzed_prompt = "best products"

    semantic_search(get_search_client("fowlart_product_review_hybrid"), prompt)

    # all_terms_are_present(get_search_client("fowlart_product_review_hybrid"), analyzed_prompt.split(" "))

    # filter_by_field(client=search_client, filter="ReviewRating eq 5", query="best")