


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

    def insert(self, nom, vc, vg, va, vt, sen):
        s = Signal()
        s.name = nom
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
        self.name = ''
        self.sig = []