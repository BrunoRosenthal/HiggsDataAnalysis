import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from event import Event
from gui import Gui

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

        self.fig, self.axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 8))
        self.flattened_axes = self.axes.flatten()

       
        self.colors = ['#2671ab', 'orange', '#4b9c35', '#d93333']
        self.labels = ['H \u2192 WW', 'WW', 'ttbar', 'Z']
        self.bins = [range(4), range(9), range(0, 200, 10), range(0, 200, 10), np.linspace(0, 3.2, 20), np.linspace(0, 3.2, 20), range(0, 200, 10), range(3), range(5)]
        self.titles = ['EE                  MM                  EM',
                      'Number of Jets',
                      'Missing Transverse Momentum',
                      'Reconstructed Dilepton Mass',
                      'Opening Angle Between Leptons',
                      'Opening Angle Between MET and Leptons',
                      'Total Lepton Transverse Momentum',
                      'No          B-Tag         Yes',
                      'Number of Predicted Events']
        self.ranges = [[0, 3],
                        [0, 8],
                        [0, 200],
                        [0, 200],
                        [0, 3.2],
                        [0, 3.2],
                        [0, 200],
                        [0, 2],
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

        self.tick_marks = [range(2), range(8), range(0, 200, 20), range(0, 200, 20), np.linspace(0, 3.2, 9), np.linspace(0, 3.2, 9), range(0, 200, 20), range(2), ' ']

        self.slider_starting = [[-0.5, 2.5],
                                [-0.5, 7.5],
                                [-5, 185],
                                [-5, 185],
                                [-0.16, 3.2],
                                [-0.16, 3.2],
                                [-5, 185],
                                [-0.5, 1.5]]
       
       
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
       
        for num, ax, bin_size, title, range_size, mark in zip(range(1, 10), self.flattened_axes, self.bins, self.titles, self.ranges, self.tick_marks):
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
                
                ax.set_xticks(mark)
                
            ax.set_title(title)
           
        plt.subplots_adjust(hspace=0.5, wspace=0.3)
        #plt.show()


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
            self.data = [x for x in self.data if ((x[var] >= start) and (x[var] < stop))]
        else:
            self.data = [x for x in self.data if ((x[var] >= stop) and (x[var] <= start))]
        self.calc_sig()


    def multiple_cuts(self, vals):
        for i in range(len(vals)):
            if vals[i][0] != self.ranges[i][0] or vals[i][1] != self.ranges[i][1]:
                self.cut(i + 1, vals[i][0], vals[i][1])
        for i in range(len(self.flattened_axes)):
            self.flattened_axes[i].clear()
        self.create_hist()
        run_update()
       
       
def run_update():
    g.update_hist()



plt.rcParams.update({'font.size': 7})
d = Data()
d.read_data()
d.create_hist()
root = tk.Tk()
g = Gui(root, d.fig, d.flattened_axes)
g.show_hist()
g.create_sliders(d.ranges)
g.create_button(d)
g.create_reset_button(d)
root.mainloop()
