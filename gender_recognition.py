from pylab import *
import numpy as np
from wave import open
from struct import unpack_from
from scipy import *
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


meskiMinMax = [60, 160]
zenskiMinMax = [180, 270]

def HPS(freq, matrix):
    czas = 3  # dlugosc dzwieku w sekundach

    #podział sygnału na mniejsze
    probki = [matrix[i * freq:(i + 1) * freq] for i in range(int(czas))]

    wyniki = []
    for dane in probki:
        if (len(dane) == 0):
            continue
        else:
            okno_czasowe = np.hamming(len(dane))    #pobranie próbek z sygnału
            dane = dane * okno_czasowe
            fourier = abs(fft.fft(dane))/freq   #wyzaczanie transformaty fouriera
            fourier_kopia = np.copy(fourier)

        # mnożenie o to samo widmo próbkowane w dół o 2,3,4
        for i in range(2,5):
            tab = np.copy(fourier[::i])
            fourier_kopia = fourier_kopia[:len(tab)]
            fourier_kopia *= tab

        wyniki.append(fourier_kopia)

    odpowiedz = [0] * len(wyniki[int(len(wyniki)/2)]) #długość środkowej wartości listy wyniki

    for res in wyniki:
        if (len(res) != len(odpowiedz)):
            continue
        else:
            odpowiedz += res

    if (np.sum(odpowiedz[meskiMinMax[0]:meskiMinMax[1]]) > np.sum(odpowiedz[zenskiMinMax[0]:zenskiMinMax[1]])):
        return 'M'
    else:
        return 'K'


def run(arg):
    try:
        plik = open(arg, "r")
        kanaly, _, czestotliwosc, klatki, _, _ = plik.getparams()

        ramki = plik.readframes(klatki * kanaly)
        macierz = unpack_from("%dh" % klatki * kanaly, ramki)

        if (kanaly) == 2:
            kanal1 = np.array(macierz[0::2])
            kanal1 = kanal1/2
            kanal2 = np.array(macierz[1::2])
            kanal2 = kanal2/2
            macierz = kanal1 + kanal2
        else:
            macierz = np.array(macierz)

        print(HPS(czestotliwosc, macierz))
    except:
        print("M")


if __name__ == "__main__":
    run(sys.argv[1])