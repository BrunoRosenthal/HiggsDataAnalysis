import matplotlib.pyplot as plt
import numpy as np
from event import Event

class Data:

    def __init__(self):
        self.initial_data = []
        self.data = []
        
        self.nEvents = 0
        self.nSignal = 0
        self.tWeight = 0
        self.tSignalWeight = 0
        self.sig = 0
        self.init_sig = 0
        
        self.colors = ['#2671ab', 'orange', '#4b9c35', '#d93333']
        self.labels = ['H \u2192 WW', 'WW', 'ttbar', 'Z']
        self.bins = [3, range(8), range(0, 200, 10), range(0, 200, 10), np.linspace(0, 3.2, 20), np.linspace(0, 3.2, 20), range(0, 200, 10), 2, 4]
        self.titles = ['EE                  MM                  EM',
                      'Number of Jets',
                      'Missing Transverse Momentum',
                      'Reconstructed Dilepton Mass',
                      'Opening Angle Between Leptons',
                      'Opening Angle Between MET and Leptons',
                      'Total Lepton Transverse Momentum',
                      'No          B-Tag         Yes',
                      'Number of Predicted Events']
        self.ranges = [[0, 2],
                        [0, 7],
                        [0, 200],
                        [0, 200],
                        [0, 3.2],
                        [0, 3.2],
                        [0, 200],
                        [0, 1],
                        [0, 3]]
        self.types = [
                    'Channel',
                    'NJets',
                    'MET',
                    'Mll',
                    'LepDeltaPhi',
                    'METLLDeltaPhi',
                    'SumLepPt',
                    'BTags',
                    'weight']
        
        
    def read_data(self):
        with open('outreach.csv') as f:
            for line in f:
                try:
                    current = Event(line)
                except Exception:
                    continue
                
                weight = current.weight
                line = [float(x) if float(x)!= int(float(x)) else int(float(x)) for x in line.split(',')]
                self.initial_data.append(line)

                self.nEvents += 1
                self.tWeight += weight
                
                if current.isSignal():
                    self.tSignalWeight += weight
                    self.nSignal += 1
                    
        self.data = self.initial_data[:]
        self.init_sig = self.tSignalWeight / np.sqrt(self.tWeight - self.tSignalWeight)
        self.sig = self.init_sig
                    
                    

    def split_data(self, num):
        data_section = [[], [], [], []]
        weight_section = [[], [], [], []]
        for line in self.data:
            data_section[line[0]].append(line[num])
            weight_section[line[0]].append(line[-1])

        return data_section, weight_section


    def create_hist(self):
        self.fig, self.axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 8))
        self.flattened_axes = self.axes.flatten()

        for num, ax, bin_size, title, range_size in zip(range(1, 10), self.flattened_axes, self.bins, self.titles, self.ranges):
            if num == 9:
                data_section, weight_section = self.split_data(0)
                plt.gca().invert_yaxis()
                ax.get_yaxis().set_visible(False)
                
                heights, bins, patches = ax.hist(data_section, bins=bin_size, stacked=True, color=self.colors, label=self.labels, rwidth=0.8, range=range_size, weights=weight_section, orientation='horizontal')


                heights = heights[3]
                num_z = int(round(heights[3]))
                num_ttbar = int(round(heights[2]))
                num_ww = int(round(heights[1]))
                num_hww = int(round(heights[0]))

                plt.text(0.05, 0.11, 'Z ({})'.format(num_z), fontsize=10, transform = ax.transAxes)
                plt.text(0.05, 0.34, 'ttbar ({})'.format(num_ttbar), fontsize=10, transform = ax.transAxes)
                plt.text(0.05, 0.58, 'WW ({})'.format(num_ww), fontsize=10, transform = ax.transAxes)
                plt.text(0.05, 0.83, 'HWW ({}) Significance: {}'.format(num_hww, round(self.sig, 3)), fontsize=10, transform = ax.transAxes)
            else:
                if num == 8:
                    ax.get_xaxis().set_visible(False)
                data_section, weight_section = self.split_data(num)
                ax.hist(data_section, bins=bin_size, stacked=True, color=self.colors, label=self.labels, rwidth=0.8, range=range_size, weights=weight_section)
            ax.set_title(title)
            
        plt.subplots_adjust(hspace=0.5, wspace=0.3)
        plt.show()


    def calc_sig(self):
        tWeight = 0
        tSignalWeight = 0
        for line in self.data:
            tWeight += line[-1]
            if line[0] == 0:
                tSignalWeight += line[-1]
        self.sig = tSignalWeight / np.sqrt(tWeight - tSignalWeight)


    def cut(self, var, start, stop):
        if start <= stop:
            self.data = [x for x in self.data if ((x[var] >= start) and (x[var] <= stop))]
        else:
            self.data = [x for x in self.data if ((x[var] >= stop) and (x[var] <= start))]
        self.calc_sig()






plt.rcParams.update({'font.size': 7})
d = Data()
d.read_data()
#d.create_hist()
#d.cut(8, 0, 0)
#d.cut(1, 2, 2)
#d.cut(7, 50, 200)
d.create_hist()


    
