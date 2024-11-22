from src.gensim_word2vec.ReviewCorpus import ReviewsCorpus
import gensim.models

if __name__=="__main__":

    my_corp = ReviewsCorpus(number_of_records=1000,minimal_review_length=100)

    model = gensim.models.Word2Vec(
        sentences=my_corp,
        vector_size=1000)

    model_path = r"C:\Users\Artur.Semikov\PycharmProjects\FowlartAiSearch\resources\gensim-models\main-model-l.txt"

    model.save(model_path)

    print(f"Training finalized! Model was saved at {model_path}")