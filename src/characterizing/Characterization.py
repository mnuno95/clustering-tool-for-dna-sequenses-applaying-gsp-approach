from spectrum import nextpow2
from numpy.fft import fft
import time

class Characterization:
    features = list()
    option = ''

    def characterize(self, signals):
        del self.features[:]

        ft = FastFourierTransform()
        ft.transform(signals, self.features)

        time.sleep(2)
        print ('Features: ', len(self.features))


class FastFourierTransform():
    maxlength = 0
    ff_t = []

    def insert(self, fftran, fts):
        f = Feature()
        f.feat = fftran
        fts.append(f)

    def transform(self, signals, features):
        for i in signals:
            for j in i.sig:
                if self.maxlength < len(j):
                    self.maxlength = len(j)

        nfft = pow(2, nextpow2(self.maxlength))

        for i in signals:
            for j in i.sig:
                f = abs(fft(j, nfft))

                self.ff_t = []

                for k in range(int(nfft / 2) + 1):
                    self.ff_t.append(f[k])
            else:
                self.insert(self.ff_t, features)

class Feature():
    def __init__(self):
        self.feat = []