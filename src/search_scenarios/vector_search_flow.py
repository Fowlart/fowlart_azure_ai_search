from utils.common_utils import get_search_client, get_search_index_client, extract_key_phrases, bcolors
from search_queries.search_queries import vector_search
from gensim_word2vec import gensim_util as gu
from utils.common_utils import get_text_analytics_client


if __name__=="__main__":

    prompt = """Scotch tape for small repair"""

    search_client = get_search_client()

    search_index_client = get_search_index_client()

    text_analytics_client = get_text_analytics_client()

    key_phrases = extract_key_phrases(prompt,text_analytics_client)

    key_phrases_prompt = " ".join(key_phrases)

    print(f"\n{bcolors.BOLD}Searching vectors for prompt: {key_phrases_prompt}\n{bcolors.ENDC}")

    vector = gu.get_vector_from_sentence(
        text=key_phrases_prompt,
        search_index_client= search_index_client)

    vector_search(client=search_client,
                  vector=vector,
                  exhaustive_search=True,
                  k_nearest_neighbors=4)


