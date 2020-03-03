import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 5})

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
        total[int(i[0])].append(i[n])
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


totalWeight = 0
eventsWeight = 0
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
    weight = current.weight
    broken_line = line.split(',')
    line = [float(broken_line[x]) * weight if x > 0 else int(float(broken_line[x])) for x in range(len(broken_line))]
    #line = [float(x) * weight if  0 else int(float(x)) for x in line.split(',')]
    totalWeight += weight  # check meaning of weight, sum of total weight!= 1
    if line[0] == 0:
        eventsWeight += weight
    data.append(line)

#data1 = cut(data, 3, 0, 60)

def graph(data):
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10,7))
    Daxes = axes.flatten()
    colors = ['#2671ab', 'orange', '#4b9c35', '#d93333']
    labels = ["H \u2192 WW", "WW", "ttbar", "Z"]
    bins = [3,
            [0, 1, 2, 3, 4, 5, 6, 7],
            list(range(0, 200, 10)),
            list(range(0, 200, 10)),
            np.linspace(0, 3.2, 20),
            np.linspace(0, 3.2, 20),
            list(range(0, 200, 10)),
            2,
            4]
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


    titles = ['EE         MM         EM',
              'Number of Jets',
              'Missing Transverse Momentum',
              'Reconstructed Dilepton Mass',
              'Opening Angle Between Leptons',
              'Opening Angle Between MET and Leptons',
              'Total Lepton Transverse Momentum',
              '(No)      B-Tag     (Yes)',
              'Template'
              ]
    rangeB = [
        [0, 2],
        [0, 7],
        [0, 200],
        [0, 200],
        [0, 3.2],
        [0, 3.2],
        [0, 200],
        [0, 1],
        [0, 3]
    ]
    

    for typeA, nums, ax, b, title, r in zip(types, range(1, 10), Daxes, bins, titles, rangeB):
        d = split_data(data, nums)
        #d = adjust(np.array(d))
        ax.hist(d, bins=b, stacked=True, color=colors, label=labels, rwidth=0.8, range=r)
        ax.set_title(title)
    plt.subplots_adjust(hspace = 0.5, wspace=0.7)
    plt.show()

graph(data)

#sig = totalWeight/np.sqrt(eventsWeight - totalWeight)
