from searching.Biofetcher import Biofetcher

import pickle

if __name__=='__main__':
    biofetcher = Biofetcher()

    print('Creating db...')

    nameFile = str(biofetcher.organismTypes)

    with open('dbFile.dictionary', 'wb') as dbFile_dictionary:
        pickle.dump(biofetcher.listOfCells, dbFile_dictionary)