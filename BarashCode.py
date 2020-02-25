import matplotlib.pyplot as plt
import numpy as np
import math
plt.rcParams.update({'font.size': 5})

#SELECT CUTS HERE

eventType_limit =       [0,1,2,3]	# Events 						[0,1,2,3]
Channel_limit =         [0,1,2]		# Channels 						[0,1,2]
NJets_limit =           [0,7]		# Number of Jets 				[0,7]
Met_limit =             [0,200]		# Missing Transverse Momentum 	[0,200]
Mll_limit =             [0,200]		# Dilepton Mass  				[0,200]
LepDeltaPhi_limit =     [0,180]		# Lepton Angle 					[0,180]
METLLDeltaPhi_limit =   [0,180] 	# Lepton-MET Angle 				[0,180]
SumLepPt_limit =        [0,200]		# Lepton Transverse Momentum 	[0,200]
BTags_limit =           [0,1]		# BTags included? 				[0,1]

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

nEvents = 0
nSignal = 0

eventType_list = [ [],[],[],[] ]
Channel_list = [ [],[],[],[] ]
NJets_list = [ [],[],[],[] ]
Met_list = [ [],[],[],[] ]
Mll_list = [ [],[],[],[] ]
LepDeltaPhi_list = [ [],[],[],[] ]
METLLDeltaPhi_list = [ [],[],[],[] ]
SumLepPt_list = [ [],[],[],[] ]
BTags_list = [ [],[],[],[] ]
weight_list = [ [],[],[],[] ]

for line in open("outreach.csv"):
    try:
        current = Event(line)
        if  (current.Channel in Channel_limit) and (NJets_limit[0] <= current.NJets <= NJets_limit[1]) and (Met_limit[0] <= current.MET <= Met_limit[1]) and (Mll_limit[0] <= current.Mll <= Mll_limit[1]) and (LepDeltaPhi_limit[0] <= current.LepDeltaPhi*(180/3.14) <= LepDeltaPhi_limit[1]) and (METLLDeltaPhi_limit[0] <= current.METLLDeltaPhi*(180/3.14) <= METLLDeltaPhi_limit[1]) and (SumLepPt_limit[0] <= current.SumLepPt <= SumLepPt_limit[1]) and (current.BTags in BTags_limit):
            eventType_list[current.eventType].append(current.eventType)
            Channel_list[current.eventType].append(current.Channel)
            NJets_list[current.eventType].append(current.NJets)
            Met_list[current.eventType].append(current.MET)
            Mll_list[current.eventType].append(current.Mll)
            LepDeltaPhi_list[current.eventType].append(abs(current.LepDeltaPhi)*(180/3.14))
            METLLDeltaPhi_list[current.eventType].append(abs(current.METLLDeltaPhi)*(180/3.14))
            SumLepPt_list[current.eventType].append(current.SumLepPt)
            BTags_list[current.eventType].append(current.BTags)
            if current.eventType == 0: nSignal += 1
            nEvents += 1
    except Exception:
        continue

def plot():
    fig, axes = plt.subplots(nrows=3, ncols=3)
    ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8 = axes.flatten()
    colors = ['#2671ab', 'orange', '#4b9c35', '#d93333']
    ax0.hist([Channel_list[0],Channel_list[1],Channel_list[2],Channel_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins = 3, range=[0,2])
    ax0.set_title('EE         MM         EM')
    ax1.hist([NJets_list[0],NJets_list[1],NJets_list[2],NJets_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins = [0,1,2,3,4,5,6,7],range=[0,7])
    ax1.set_title('Number of Jets')
    ax2.hist([Met_list[0],Met_list[1],Met_list[2],Met_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins=[j for j in range(0,200,10)], range=[0, 200])
    ax2.set_title('Missing Transverse Momentum')
    ax3.hist([Mll_list[0],Mll_list[1],Mll_list[2],Mll_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins=[j for j in range(0,200,10)], range=[0,200])
    ax3.set_title('Reconstructed Dilepton Mass')
    ax4.hist([LepDeltaPhi_list[0],LepDeltaPhi_list[1],LepDeltaPhi_list[2],LepDeltaPhi_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins=[j for j in range(0,181,10)],range=[0,180])
    ax4.set_title('Opening Angle Between Leptons')
    ax5.hist([METLLDeltaPhi_list[0],METLLDeltaPhi_list[1],METLLDeltaPhi_list[2],METLLDeltaPhi_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins=[j for j in range(0,181,10)], range=[0,180])
    ax5.set_title('Opening Angle Between MET and Leptons')
    ax6.hist([SumLepPt_list[0],SumLepPt_list[1],SumLepPt_list[2],SumLepPt_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins=[j for j in range(0,200,10)],range=[0,200])
    ax6.set_title('Total Lepton Transverse Momentum')
    ax7.hist([BTags_list[0],BTags_list[1],BTags_list[2],BTags_list[3]] ,color=colors, rwidth=0.8, stacked = True, bins = 2,range=[0,1])
    ax7.set_title('(No)      B-Tag     (Yes)')
    ax8.hist([eventType_list[0],eventType_list[1],eventType_list[2],eventType_list[3]], color=colors, bins = 4, rwidth=0.80,orientation='horizontal',stacked=True, range=[0, 3])
    ax8.set_title('Significance: {}' .format( round(nSignal/math.sqrt(nEvents - nSignal),3)))
    #plt.tight_layout()
    plt.subplots_adjust(hspace = 0.5, wspace=0.7)
    plt.savefig('examplePic.png', dpi = 3000)
    plt.show()
	
plot()
print('File updated.')
