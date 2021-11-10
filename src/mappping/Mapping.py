import threading
import yaml



class Mapping:
    signals = list()
    aux = list()
    option = ''

    def parallelism(self, sequences, first, last, lst):
        for i in range(first, last):
                v = Voss()
                for j in sequences[i]:
                    v.transform(j)
                else:
                    v.insert(v.c, v.g, v.a, v.t, lst)

    def transform(self, sequences):
        del self.signals[:]
        del self.aux[:]
        tam = len(sequences)
        mtam = int(tam / 2)

        t1 = threading.Thread(target=self.parallelism, args=(sequences, 0, mtam, self.signals))
        t2 = threading.Thread(target=self.parallelism, args=(sequences, mtam, tam, self.aux))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.signals.extend(self.aux)


    def processDnaSequences(self, sequences):

        dnaSequences = []
        yaml_file = open('../resources/config.yaml')
        yaml_content = yaml.safe_load(yaml_file)
        region = yaml_content['query']['regions'][0]

        for cell in sequences:
            for dna in cell.genomicRegions[region]:
                dnaSequences.append(dna)

        self.transform(dnaSequences)


class Voss:
    voss_c = {'C': 1, 'G': 0, 'A': 0, 'T': 0}
    voss_g = {'C': 0, 'G': 1, 'A': 0, 'T': 0}
    voss_a = {'C': 0, 'G': 0, 'A': 1, 'T': 0}
    voss_t = {'C': 0, 'G': 0, 'A': 0, 'T': 1}

    def __init__(self):
        self.c = []
        self.g = []
        self.a = []
        self.t = []

    def insert(self, vc, vg, va, vt, sen):
        s = Signal()
        s.sig.append(vc)
        s.sig.append(vg)
        s.sig.append(va)
        s.sig.append(vt)
        sen.append(s)

    def transform(self, base):
        self.c.append(self.voss_c[base])
        self.g.append(self.voss_g[base])
        self.a.append(self.voss_a[base])
        self.t.append(self.voss_t[base])

class Signal:
    def __init__(self):
        self.sig = []