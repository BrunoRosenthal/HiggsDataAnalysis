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


def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def adjust(d):
    n = []
    for arr in d:
        n.append(reject_outliers(np.array(arr), 2))
    return n


nEvents = 0
data = [
        {
        "type": 'Channel',
        "num_bins": 3,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        },
        {
        "type": 'NJets',
        "num_bins": 11,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        },
        {
        "type": 'MET',
        "num_bins": 21,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        },
        {
        "type": 'Mll',
        "num_bins": 21,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": [],
        },
        {
        "type": 'LepDeltaPhi',
        "num_bins": 20,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        },
        {
        "type": 'METLLDeltaPhi',
        "num_bins": 21,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        },
        {
        "type": 'SumLepPt',
        "num_bins": 20,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        },
        {
        "type": 'BTags',
        "num_bins": 2,
        "custom_axis": ['no', 'yes'],
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        },
        {
        "type": 'weight',
        "num_bins": 20,
        "H \u2192 WW": [],
        "WW": [],
        "ttbar": [],
        "Z": []
        }
]



for line in open("outreach.csv"):
    try:
        current = Event(line)
        for i in range(len(data)):
            data[i][current.typeName()].append(getattr(current, data[i]['type']))
    except Exception:
        continue
    if nEvents % 10000 == 0:
        pass
        #print("Event %i: %s" % (nEvents, current))
    nEvents += 1

print("\nnEvents=%i\n" % nEvents)

for i in range(len(data)):
    if data[i]['type'] != 'BTags':
        continue
    d = [y for x, y in data[i].items() if x not in ['type', 'num_bins', 'custom_axis']]
    d = adjust(d)
    try:
        cust = data[i]['custom_axis']
        plt.hist(d, bins=data[i]['num_bins'], stacked=True, color=['blue','orange','green','red'], label=["H \u2192 WW", "WW", "ttbar", "Z"], rwidth=0.7)
        plt.xticks([0.25, 0.75], cust)
    except:
        plt.hist(d, bins=data[i]['num_bins'], stacked=True, color=['blue','orange','green','red'], label=["H \u2192 WW", "WW", "ttbar", "Z"], rwidth=0.7)       
    
    plt.xlabel(data[i]['type'])
    plt.legend(loc='best')
    plt.show()


