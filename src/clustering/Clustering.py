from sklearn.cluster import Birch
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import preprocessing
from sklearn import datasets
from matplotlib import style

import numpy as np
import yaml
import matplotlib.pyplot as plt

style.use('ggplot') or plt.style.use('ggplot')

X, y = datasets.load_iris(return_X_y=True)

from sklearn.decomposition import PCA

class Clustering:

    listGoalStandar = []
    def tranformGoldStandar(self):

        for group in (self.philogenticList):
            if group == 'A7':
                self.listGoalStandar.append(0)
            elif group == 'A9':
                self.listGoalStandar.append(1)
            else:
                self.listGoalStandar.append(2)

    def kmeansImplementation(self, featuredOrganismn):
        list = []
        for i in featuredOrganismn:
            list.append(i.feat)

        X_normalized = self.normalizeVector(list)
        X_r = self.generatePCA(X_normalized)

        km = KMeans(n_clusters=3, n_init=10, max_iter=300,
               init='k-means++', algorithm='auto')
        km.fit(X_r)
        self.generateTable(km.labels_)

    def dbScanImplementation(self, featuredOrganismn):
        list = []
        for i in featuredOrganismn:
            print(len(i.feat))
            list.append(i.feat)

        X_normalized = self.normalizeVector(list)

        clustering = DBSCAN(eps=0.4, min_samples=2).fit_predict(X_normalized)

        print(clustering)

    def birchImplementation(self, featuredOrganismn):
        list = []
        for i in featuredOrganismn:
            list.append(i.feat)


        brc = Birch(n_clusters=3).fit(list)
        labels = brc.predict(list)

        labels_predict = labels.tolist()

        print(labels_predict)

        self.generateTable(labels_predict)

    def generateTable(self, clusterList):
        fig, ax = plt.subplots(1, 1)

        data = []
        for index in range(len(clusterList)):

            data.append([self.randIndexList[index], clusterList[index], self.philogenticList[index]])

        column_labels = ["VPH Type", "Cluster label Result", "Philogentic Group"]

        ax.axis('tight')
        ax.axis('off')

        ax.table(cellText=data, colLabels=column_labels, loc="center")

        plt.show()

    def normalizeVector(self, list):
        X_train = np.array(list)
        X_normalized = preprocessing.normalize(X_train, norm='l2')

        return X_normalized

    def plotPca3D(self, X_r):
        x_Axis = []
        y_Axis = []
        z_Axis = []

        for e in X_r:
            x_Axis.append(e[0])
            y_Axis.append(e[1])
            z_Axis.append(e[2])

        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(projection='3d')
        ax.scatter(x_Axis, y_Axis, z_Axis)
        ax.view_init(elev=20., azim=-35)

        for index in range(len(X_r)):
            ax.text(x_Axis[index],  y_Axis[index], z_Axis[index], str(self.randIndexList[index]), fontsize=6,
                    horizontalalignment="right",
                    verticalalignment="top")

        plt.show()


    def plotPca2D(self, X_r):
        x_Axis = []
        y_Axis = []

        for e in X_r:
            x_Axis.append(e[0])
            y_Axis.append(e[1])

        plt.scatter(x_Axis, y_Axis)

        for index in range(len(X_r)):
            plt.annotate(str(self.randIndexList[index]),
                         (x_Axis[index],  y_Axis[index]))
        plt.show()

    def generatePCA(self, X_normalized):
        pca = PCA(n_components=3)
        X_r = pca.fit(X_normalized).transform(X_normalized)

        print(pca.explained_variance_ratio_)

        return X_r

    def clusterSwitch(self, featuredOrganismn):
        yaml_file = open('../resources/config.yaml')
        self.yaml_content = yaml.safe_load(yaml_file)

        clusterOpc = self.yaml_content['flow']['clustering']

        if clusterOpc == 'BIRCH':
            self.birchImplementation(featuredOrganismn)
            # RANDINDEX
            # Adjusted randix
        elif clusterOpc == 'KMEANS':
            self.kmeansImplementation(featuredOrganismn)
            #SILHOUTE
            #RANDINDEX
        elif clusterOpc == 'DBSCAN':
            self.dbScanImplementation(featuredOrganismn)
            # SILHOUTE
            # RANDINDEX
        else:
            print("Option of clustering not found")

    def __init__(self, featuredOrganismn, randIndexList, philogenticList):
        self.randIndexList = randIndexList
        self.philogenticList = philogenticList
        self.tranformGoldStandar()
        self.clusterSwitch(featuredOrganismn)