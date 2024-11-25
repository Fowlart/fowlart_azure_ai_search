from search_queries import search_by_key_phrases

from src.utils.common_utils import get_search_client, get_text_analytics_client, extract_key_phrases

if __name__=="__main__":

    prompt = """
    What is the recommendation for the teacher?
    """

    search_client = get_search_client()

    text_analytic_client = get_text_analytics_client()

    search_by_key_phrases(search_client, extract_key_phrases(prompt, text_analytic_client))
