from searching.Biofetcher import Biofetcher
from mappping.Mapping import Mapping
from characterizing.Characterization import Characterization
from clustering.Clustering import Clustering

if __name__=='__main__':
    biofetcher = Biofetcher()

    mapping =  Mapping()
    mapping.processDnaSequences(biofetcher.listOfCells)

    characterization = Characterization()
    characterization.characterize(mapping.signals)

    cluster = Clustering(characterization.features)