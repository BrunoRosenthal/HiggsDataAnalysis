import numpy as np
from scipy.optimize import minimize
from event import Event

def read_file(data):
    with open('outreach.csv') as f:
        for line in f:
            try:
                current = Event(line)
            except Exception:
                continue

            weight = current.weight
            line = [float(x) if float(x)!= int(float(x)) else int(float(x)) for x in line.split(',')]
            data.append(line)

    return data


def calc_sig(data):
    tWeight = 0
    tSignalWeight = 0
    for line in data:
        tWeight += line[-1]
        if line[0] == 0:
            tSignalWeight += line[-1]
    sig = tSignalWeight / np.sqrt(tWeight - tSignalWeight)
    return sig


def cut(data, var, start, stop):
    if start <= stop:
        data = [x for x in data if ((x[var] >= start) and (x[var] < stop))]
    else:
        data = [x for x in data if ((x[var] >= stop) and (x[var] <= start))]
    return data


def multiple_cuts(data, var):
    for i in range(len(var)):
        data = cut(data, i + 1, var[i][0], var[i][1])
    sig = calc_sig(data)
    return data, sig

def objective(x, data):
    v = np.split(x, 8)
    data, sig = multiple_cuts(data, v)
    return -sig
    


data = read_file([])

v = [[2, 3],
     [0, 2],
     [30, 60],
     [15, 55],
     [0.38, 1.46],
     [2.68, 3.20],
     [50, 70],
     [0, 1]]

init = [2.0, 3.0, 0.0, 6.0, 0.0, 80.0, 10.0, 55.0, 0.0, 3.2, 0.0, 3.2, 0.0, 200.0, 0.0, 1.0]

bnd = [(0.0, 3.0), (0.0, 3.0), (0.0, 8.0), (0.0, 8.0), (0.0, 200.0), (0.0, 200.0), (0.0, 200.0), (0.0, 200.0), (0.0, 3.2), (0.0, 3.2), (0.0, 3.2), (0.0, 3.2), (0.0, 200.0), (0.0, 200.0), (0.0, 2.0), (0.0, 2.0)]

sol = minimize(objective, init, args=(data), method='SLSQP', bounds=bnd)
print(sol)
