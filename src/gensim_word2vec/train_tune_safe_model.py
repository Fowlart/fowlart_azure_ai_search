from src.gensim_word2vec.ReviewCorpus import ReviewsCorpus
import gensim.models

from utils.common_utils import get_path_to_gensim_model

if __name__=="__main__":

    my_corp = ReviewsCorpus(number_of_records=1000,minimal_review_length=100)

    model = gensim.models.Word2Vec(
        sentences=my_corp,
        vector_size=300)

    model.save(get_path_to_gensim_model())

    print(f"Training finalized! Model was saved at {get_path_to_gensim_model()}")