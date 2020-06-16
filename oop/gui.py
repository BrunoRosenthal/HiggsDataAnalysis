import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui(tk.Frame):
    def __init__(self, master, fig, flattened_axes, **kw):
        super().__init__(master, **kw)
        self.master = master
        master.title('Histograms')
        master.resizable(0, 0)
        self.fig = fig
        self.flattened_axes = flattened_axes
        self.lines = []
        self.sliders = []

        self.resolutions = [1, 1, 1, 1, 0.01, 0.01, 1, 1]

    def show_hist(self):
        self.line = FigureCanvasTkAgg(self.fig, self.master)
        self.line.get_tk_widget().grid(column=0, row=3, columnspan=8)

    def update_lines(self):
        for i in range(len(self.lines)):
            self.lines[i].remove()
        self.lines.clear()

        for i in range(len(self.sliders)):
            for j in range(2):
                val = self.sliders[i][j].get()
                l = self.flattened_axes[i].axvline(x=val, color='black')
                self.lines.append(l)

    def update_lines_first(self, event):
        self.update_lines()

        self.fig.canvas.draw_idle()

    def create_sliders(self, ranges):
        for i in range(8):
            t = []
            for j in range(2):
                s = tk.Scale(self.master, from_=ranges[i][0], to=ranges[i][1], resolution=self.resolutions[i], orient='horizontal', command=self.update_lines_first)
                s.set(ranges[i][j])
                t.append(s)
            self.sliders.append(t)

        for i in range(len(self.sliders)):
            for j in range(2):
                self.sliders[i][j].grid(row=j, column=i)

    def get_vals(self):
        self.vals = []
        for i in range(len(self.sliders)):
            graph_slider = []
            for j in range(2):
                val = self.sliders[i][j].get()
                graph_slider.append(val)
            self.vals.append(graph_slider)

    def submit(self, data):
        self.get_vals()
        data.multiple_cuts(self.vals)

    def create_button(self, data):
        self.confirm_button = tk.Button(self.master, text='Enter Cuts', command=lambda: self.submit(data))
        self.confirm_button.grid(row=2, column=4)

    def update_hist(self):
        self.update_lines()
        self.fig.canvas.draw_idle()

    def reset_cuts(self, data):
        data.data = data.initial_data
        for i in range(len(data.flattened_axes)):
            data.flattened_axes[i].clear()
        data.create_hist()
        for i in range(len(self.sliders)):
            for j in range(2):
                self.sliders[i][j].grid(row=j, column=i)

        self.update_hist()

    def create_reset_button(self, data):
        self.reset_button = tk.Button(self.master, text='Reset Cuts', command=lambda: self.reset_cuts(data))
        self.reset_button.grid(row=2, column=3)
