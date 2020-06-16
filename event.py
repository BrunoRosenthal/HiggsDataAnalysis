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

    def __init__(self, line):
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
        return 1 <= self.eventType <= 3

    def isData(self):
        return self.eventType == 4
