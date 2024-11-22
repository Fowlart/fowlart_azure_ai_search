from src.gensim_word2vec.ReviewCorpus import ReviewsCorpus
import gensim.models

if __name__=="__main__":

    my_corp = ReviewsCorpus()

    model = gensim.models.Word2Vec(
        sentences=my_corp,
        vector_size=100,
        workers=10)

    model_path = r"C:\Users\Artur.Semikov\PycharmProjects\FowlartAiSearch\resources\gensim-models\main-model.txt"

    model.save(model_path)

    print(f"Training finalized! Model was saved at {model_path}")