from azure.search.documents.indexes import SearchIndexClient
from utils.common_utils import get_tokens, bcolors as c
import gensim
import numpy as np


def get_vector_from_sentence(text: str,
                             search_index_client: SearchIndexClient) -> list[float]:


    tokens = get_tokens(text,
                               analyzer_name="en.microsoft",
                               index_name="fowlart_product_review_hybrid",
                               client=search_index_client)

    trained_model = gensim.models.Word2Vec.load(r"C:\Users"
                                                r"\Artur.Semikov"
                                                r"\PycharmProjects"
                                                r"\FowlartAiSearch"
                                                r"\resources"
                                                r"\gensim-models"
                                                r"\main-model-l.txt").wv

    sentence_vector_list: list[np.ndarray] = []

    for token in tokens:
        try:
            vector = trained_model[token]
            sentence_vector_list.append(vector)
            print(f"Token `{token}` was vectorized to array with the shape {vector.shape}")
        except KeyError:
            print(c.WARNING)
            print(f"The token `{token}` does not appear in this model")
            print(c.ENDC)

    if len(sentence_vector_list) == 0:
        raise Exception(f"The current model could not vectorize any word from the prompt: `{text}`")

    average_vector: np.ndarray = np.mean(sentence_vector_list, axis=0)

    result = average_vector.tolist()

    return result