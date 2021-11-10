from sklearn.cluster import Birch

class Clustering:

    def birchImplementation(self, featuredOrganismn):
        list = []
        for  i in featuredOrganismn:
            list.append(i.feat)

        brc = Birch(n_clusters=3).fit(list)
        labels = brc.predict(list)

        print(labels)

    def __init__(self, featuredOrganismn):
        self.birchImplementation(featuredOrganismn)
