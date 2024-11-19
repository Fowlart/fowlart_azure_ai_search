from search_queries import search_by_key_phrases
from src.analyze_text.extract_key_phrases import key_phrase_extraction
from src.utils.common_utils import analyze_text, get_search_client

if __name__=="__main__":

    prompt = """
    What is the recommendation for the teacher?
    """

    search_client = get_search_client("fowlart_product_review_hybrid")

    search_by_key_phrases(get_search_client("fowlart_product_review_hybrid"), key_phrase_extraction(prompt))
