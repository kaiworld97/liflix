import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def make_movie_data():
    df = pd.read_table('movie_data.csv', sep=',')
    model = Doc2Vec.load("Doc2Vec.model")

    def genre_compare(index, n):
        a = df.loc[iii, 'movie_genre']
        b = df.loc[index, 'movie_genre']
        if len(a) == 1:
            if n == 0 and len(set(b) - set(a)) == 0:
                similar_list.append(df.loc[index, 'movie_title'])
            elif n != 0 and len(set(b) - set(a)) == n and a[0] in b:
                similar_list.append(df.loc[index, 'movie_title'])
        elif len(set(b) - set(a)) == n:
            similar_list.append(df.loc[index, 'movie_title'])

    iii = 0
    inferred_doc_vec = model.infer_vector(df['token'][iii])

    most_similar_docs = model.docvecs.most_similar([inferred_doc_vec], topn=30)
    print(df.loc[iii, 'movie_genre'])

    similar_list = []
    n = 0
    while len(similar_list) < 10:
        print('hi')
        print(similar_list)
        for index, similarity in most_similar_docs:
            genre_compare(index, n)
            if len(similar_list) == 10:
                break
        print(similar_list)
        print(n)

        n += 1
    print(similar_list)
    print(n)
    print(df)
    return



make_movie_data()