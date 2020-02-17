import matplotlib.pyplot as plt
import numpy as np


class Event:
    def storeVariables(self, args):
        self.eventType = int(args[0])
        self.Channel = int(args[1])
        self.NJets = int(args[2])
        self.MET = float(args[3])
        self.Mll = float(args[4])
        self.LepDeltaPhi = float(args[5])
        self.METLLDeltaPhi = float(args[6])
        self.SumLepPt = float(args[7])
        self.BTags = int(args[8])
        self.weight = float(args[9])

    def __init__(self, inputLine):
        #        print(line.rstrip().split(","))
        self.storeVariables(line.rstrip().split(","))

    def __repr__(self):
        return " ".join(
            ["Event type Channel NJets MET Mll LepDeltaPhi METLLDeltaPhi SumLepPt BTags Weight", str(self.eventType),
             str(self.Channel), str(self.NJets),
             str(self.MET), str(self.Mll), str(self.LepDeltaPhi), str(self.METLLDeltaPhi), str(self.SumLepPt),
             str(self.BTags), str(self.weight)])

    def typeName(self):
        if self.eventType == 0:
            return "H \u2192 WW"
        if self.eventType == 1:
            return "WW"
        if self.eventType == 2:
            return "ttbar"
        if self.eventType == 3:
            return "Z"
        if self.eventType == 4:
            return "data"
        # raise Exception,"Unexpected type value"

    def isSignal(self):
        return self.eventType == 0

    def isBackground(self):
        return self.eventType >= 1 and self.eventType <= 3

    def isData(self):
        return self.eventType == 4


def split_data(data, n):
    total = [[], [], [], []]
    for i in data:
        total[i[0]].append(i[n])
    return total


def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * (np.std(data) + 0.0001)]


def adjust(d):
    n = []
    for arr in d:
        n.append(reject_outliers(np.array(arr), 2))
    return n


def cut(data, type_data, a, b):
    return [x for x in data if ((x[type_data] >= a) and (x[type_data] <= b))]


def c():
    d = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    for x in data:
        d[x[2]] += 1
    return d


nEvents = 0
types = [
    'Channel',
    'NJets',
    'MET',
    'Mll',
    'LepDeltaPhi',
    'METLLDeltaPhi',
    'SumLepPt',
    'BTags',
    'weight'
]

data = []

for line in open("outreach.csv"):
    try:
        current = Event(line)
    except Exception:
        continue
    nEvents += 1
    line = [float(x) if int(float(x)) != float(x) else int(float(x)) for x in line.split(',')]
    data.append(line)

data1 = cut(data, 3, 0, 60)

def graph(data):
    for i, j in zip(types, range(1, 10)):
        d = split_data(data, j)
        d = adjust(np.array(d))
        if i == 2:
            plt.bar(d)
        else:
            plt.hist(d, bins=20, stacked=True, color=['blue', 'orange', 'green', 'red'], label=["H \u2192 WW", "WW", "ttbar", "Z"], rwidth=0.7)
        plt.xlabel(i)
        plt.legend(loc='best')
        plt.show()

graph(data1)