from search_queries import all_terms_are_present, semantic_search, filter_by_field, simple_search
from src.utils.common_utils import analyze_text, get_search_client
from utils.common_utils import get_test_index_name

if __name__=="__main__":

    prompt = """
    What is the recommendation for the teacher?
    """

    search_client = get_search_client()

    analyze_text(text=prompt,
                 analyzer_name="standard.lucene",
                 index_name=get_test_index_name())

    semantic_search(search_client, prompt)
