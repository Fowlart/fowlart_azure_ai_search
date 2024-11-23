import gensim

if __name__ == "__main__":

    trained_model = gensim.models.Word2Vec.load(r"C:\Users"
                                            r"\Artur.Semikov"
                                            r"\PycharmProjects"
                                            r"\FowlartAiSearch"
                                                r"\resources"
                                                r"\gensim-models"
                                                r"\main-model-l.txt").wv

    for index, word in enumerate(trained_model.index_to_key):
        if index == 100:
            break
        print(f"word #{index}/{len(trained_model.index_to_key)}: {word}")

    print(trained_model["colour"])

    #sims = trained_model.most_similar('ultrasound', topn=10)

    #print(sims)