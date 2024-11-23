from utils.common_utils import get_search_client, get_search_index_client
from search_queries.search_queries import vector_search
from gensim_word2vec import gensim_util as gu


if __name__=="__main__":

    prompt = """DIY bookmarks"""

    search_client = get_search_client("fowlart_product_review_hybrid")

    search_index_client = get_search_index_client()

    vector = gu.get_vector_from_sentence(text=prompt, search_index_client= search_index_client)

    vector_search(client=search_client, vector=vector)




