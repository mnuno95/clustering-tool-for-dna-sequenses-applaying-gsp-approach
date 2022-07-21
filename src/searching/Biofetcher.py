from Bio import Entrez
from Bio import SeqIO
from datetime import datetime
from .OrganismnCell import OrganismnCell

import yaml
import copy

class Biofetcher:

    yaml_content = None
    ncbiDatabaseQuery = ''
    queryPubDateStart = ''
    queryPubDateEnd = ''
    queryMaxResult = 1
    organism = ''
    organismIdResultList = []
    listOfCells = []
    randIndexList = []
    philogenticList = []
    regionSize = 0

    '''
        this function gets the query configuration from the yaml file 
    '''
    def getSettings(self):
        yaml_file = open('../resources/config.yaml')
        self.yaml_content = yaml.safe_load(yaml_file)

        Entrez.email = self.yaml_content['api']['mail']
        Entrez.api_key = self.yaml_content['api']['key']

        self.ncbiDatabaseQuery = self.yaml_content['query']['database']
        self.queryMaxResult = self.yaml_content['query']['max_result']
        self.queryPubDateStart = self.yaml_content['query']['initDate']
        self.queryPubDateEnd = datetime.today().strftime('%Y/%m/%d')
        self.organism = self.yaml_content['query']['organism']

    '''
        this function looks for the organism id that the user requires from NCBI data base
    '''
    def findOrganismIds(self):

        self.organismTypes = self.yaml_content['query']['type']

        for type in self.organismTypes:
            self.getOrganismListFromNCBIDataBase(type)


    '''
         this function do the API call to NCBI based on the configuration and retrieves an id list of the organism.
    '''
    def getOrganismListFromNCBIDataBase(self, type):

        ncbiQueryPath = f'({self.organism} type {type} [Organism]) AND genome[All Fields] AND("{self.queryPubDateStart}"[Publication Date]: "{self.queryPubDateEnd}"[Publication Date])'

        apiCall = Entrez.esearch(db=self.ncbiDatabaseQuery, term=ncbiQueryPath, retmax=(self.queryMaxResult * 3), idtype="acc", sort="relevance")
        response = Entrez.read(apiCall)

        self.organismIdResultList.append(response['IdList'])

    '''
        This function gets a list ob the Object cell which has the information of all the needed regions of the organism
    '''
    def getOrganismFromNCBIDataBase(self):

        organismTypes = self.yaml_content['query']['type']

        index = 0
        for organismIdList in self.organismIdResultList:

            for organismId in organismIdList:
                cell = OrganismnCell(organismTypes[index])
                self.getEntrezObject(organismId, cell)
                self.listOfCells.append(cell)
            index+=1


    def getEntrezObject(self, organismId, cell):

        self.regionsSet = set(self.yaml_content['query']['regions'])
        with Entrez.efetch(db=self.ncbiDatabaseQuery, rettype="gb", retmode="text", id=organismId) as handle:
            seq_record = SeqIO.read(handle, "gb")

            dnaResult = ''
            for feature in seq_record.features:
                if feature.type == "CDS":
                    if 'gene' in feature.qualifiers:
                        genomicRegion = str(feature.qualifiers["gene"][0])

                        if genomicRegion in self.regionsSet:
                            dnaRegion = feature.location.extract(seq_record).seq
                            dnaResult += str(dnaRegion)
                            cell.pushRegionOrder(genomicRegion)

            cell.setDna(dnaResult)

    def __init__(self):
        self.getSettings()
        self.findOrganismIds()
        self.getOrganismFromNCBIDataBase()
