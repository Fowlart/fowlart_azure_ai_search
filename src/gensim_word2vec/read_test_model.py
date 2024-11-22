import gensim

if __name__ == "__main__":

    trained_model = gensim.models.Word2Vec.load(r"C:\Users"
                                            r"\Artur.Semikov"
                                            r"\PycharmProjects"
                                            r"\FowlartAiSearch\resources\gensim-models\main-model.txt").wv

    for index, word in enumerate(trained_model.index_to_key):
        if index == 10:
            break
        print(f"word #{index}/{len(trained_model.index_to_key)} is {word}")