
class OrganismnCell:
    def __init__(self, type):
        self.type = type
        self.dna = ''
        self.insertionRegionOrder = []

    def setDna(self, dna):
        self.dna = dna

    def pushRegionOrder(self, region):
        self.insertionRegionOrder.append(region)