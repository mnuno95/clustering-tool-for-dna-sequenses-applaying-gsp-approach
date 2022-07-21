from mappping.Mapping import Mapping
from characterizing.Characterization import Characterization
from clustering.Clustering import Clustering

import pickle

if __name__=='__main__':

    dnaDb = None

    with open('dbFile.dictionary', 'rb') as config_dictionary_file:
        dnaDb = pickle.load(config_dictionary_file)

    mapping = Mapping()
    mapping.processDnaSequences(dnaDb)

    characterization = Characterization()
    characterization.characterize(mapping.signals)

    cluster = Clustering(characterization.features, mapping.randIndexList, mapping.philogeneticType)