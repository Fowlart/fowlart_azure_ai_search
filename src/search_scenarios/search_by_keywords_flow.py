from search_queries import search_by_key_phrases

from src.utils.common_utils import get_search_client, authenticate_text_analytics_client, key_phrase_extraction

if __name__=="__main__":

    prompt = """
    What is the recommendation for the teacher?
    """

    search_client = get_search_client("fowlart_product_review_hybrid")

    text_analytic_client = authenticate_text_analytics_client()

    search_by_key_phrases(search_client, key_phrase_extraction(prompt,text_analytic_client))
