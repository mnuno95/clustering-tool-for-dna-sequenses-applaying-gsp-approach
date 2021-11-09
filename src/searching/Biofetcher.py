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

        organismTypes = self.yaml_content['query']['type']

        for type in organismTypes:
            self.getOrganismListFromNCBIDataBase(type)


    '''
         this function do the API call to NCBI based on the configuration and retrieves an id list of the organism.
    '''
    def getOrganismListFromNCBIDataBase(self, type):

        ncbiQueryPath = f'({self.organism} type {type} [Organism]) AND genome[All Fields] AND("{self.queryPubDateStart}"[Publication Date]: "{self.queryPubDateEnd}"[Publication Date])'

        apiCall = Entrez.esearch(db=self.ncbiDatabaseQuery, term=ncbiQueryPath, retmax=self.queryMaxResult, idtype="acc", sort="relevance")
        response = Entrez.read(apiCall)

        self.organismIdResultList.append(response['IdList'])

    '''
        This function gets a list ob the Object cell which has the information of all the needed regions of the organism
    '''
    def getOrganismFromNCBIDataBase(self):

        genomicRegions = {}
        organismTypes = self.yaml_content['query']['type']

        for region in self.yaml_content['query']['regions']:
            genomicRegions[region] = []


        index = 0
        for organismIdList in self.organismIdResultList:

            cell = OrganismnCell(organismTypes[index], copy.deepcopy(genomicRegions))

            for organismId in organismIdList:
                self.getEntrezObject(organismId, cell)

            self.listOfCells.append(cell)
            index = index + 1



    def getEntrezObject(self, organismId, cell):

        with Entrez.efetch(db=self.ncbiDatabaseQuery, rettype="gb", retmode="text", id=organismId) as handle:
            seq_record = SeqIO.read(handle, "gb")

            for feature in seq_record.features:
                if feature.type == "CDS":

                    if 'gene' in feature.qualifiers:

                        genomicRegion = str(feature.qualifiers["gene"][0])

                        if genomicRegion in self.yaml_content['query']['regions']:
                            dnaRegion = feature.location.extract(seq_record).seq

                            cell.genomicRegions[genomicRegion].append(str(dnaRegion))


    def __init__(self):
        self.getSettings()
        self.findOrganismIds()
        self.getOrganismFromNCBIDataBase()
