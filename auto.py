import numpy as np
from event import Event
import random
import time



# Importing needed modules

def read_file(data):
    # this function puts the data into a set of arrays
    with open('outreach.csv') as f:
        for line in f:
            try:
                current = Event(line)
            except Exception:
                continue

            line = [float(x) if float(x) != int(float(x)) else int(float(x)) for x in line.split(',')]
            data.append(line)

    return data


def calc_sig(data):
    # this function calculates the significance
    t_weight = 0
    t_signal_weight = 0
    for line in data:
        t_weight += line[-1]
        if line[0] == 0:
            t_signal_weight += line[-1]
    sig = t_signal_weight / np.sqrt(t_weight - t_signal_weight)
    return sig


def cut(data, var, start, stop):
    # this function cuts the data for a single variable
    if start <= stop:
        data = [x for x in data if ((x[var] >= start) and (x[var] < stop))]
    else:
        data = [x for x in data if ((x[var] >= stop) and (x[var] <= start))]
    return data


def multiple_cuts(data, var):
    # this function cuts the data for multiple variables
    for i in range(len(var)):
        data = cut(data, i + 1, var[i][0], var[i][1])
    sig = calc_sig(data)
    return data, sig


data = read_file([])


def random_points():
    # this function generates a random 12 dimensional coordinate
    ranges = [[0, 3],
              [0, 8],
              [0, 200],
              [0, 200],
              [0, 3.2],
              [0, 3.2],
              [0, 200],
              [0, 2]]

    rands = []
    for i, j in ranges:
        if int(j) == j:
            a = random.randint(i, j - 1)
            b = random.randint(a + 1, j)
            a = 0
            b = random.randint(1, j)

        else:
            a = random.random()
            b = random.random()

            a *= b
            a *= j
            b *= j

            a = 0
            b = random.random() * j

        rands.append([a, b])

    rands[0] = [2, 3]
    rands[7] = [0, 1]

    return rands


num_starting_points = 10  # I set the number of random points to use
sig_threshold = 0.35 # I set the minimum significance that will be passed through
starting_points = [] # I create an array to store the random points
for i in range(num_starting_points):
    start = False
    while not start:
        r = random_points()
        new_data, sig = multiple_cuts(data, r)

        if sig > sig_threshold and sig != np.inf:
            start = True

            starting_points.append((r, sig))


def increment(r, n):
    # this function increments a 12 dimensional point
    if n % 2 == 0:
        r[n // 2][0] += 1
    else:
        r[n // 2][1] -= 1
    return r


ranges = [[0, 8],
          [0, 200],
          [0, 200],
          [0, 3.2],
          [0, 3.2],
          [0, 200]]

increments = [1, 1, 1, 0.01, 0.01, 1]


def crop_vec(r):
    # this function removes the first and last element because those aren't supposed to be randomised
    r.pop(0)
    r.pop()
    return r


def recrop_vec(r):
    # this function reinserts the first and last element
    r.insert(0, [2, 3])
    r.insert(len(r), [0, 1])
    return r


def rand_one_change(r, ranges):
    # this function changes 1 coordinate randomly of a 12 dimensional point
    r = np.array(crop_vec(r)).flatten()
    tmp_ranges = np.array(ranges).flatten()
    pos = random.randint(0, len(r) - 1)
    val = random.choice([-1, 1])
    if r[pos] == tmp_ranges[pos]:
        if pos % 2 == 1:
            val = -1
        else:
            val = 1
    val *= increments[pos // 2]
    r[pos] += val
    temp = []
    for i in range(0, len(r), 2):
        temp.append([r[i], r[i + 1]])
    temp = recrop_vec(temp)
    pos = (1 + (pos // 2), pos % 2)
    reversal = (pos, -val)
    return temp, reversal


ending_points = [] # this is the array where the final points will be stored
for r, s in starting_points:
    c = 0
    sig = multiple_cuts(data, r)[1]
    sig_100 = 0
    next_point = False
    while not next_point:
        c += 1
        sig = multiple_cuts(data, r)[1]
        r, reversal = rand_one_change(r, ranges)
        nSig = multiple_cuts(data, r)[1]
        if nSig < sig:
            r[reversal[0][0]][reversal[0][1]] += reversal[1]
        if c % 100 == 0:
            if sig == sig_100:
                ending_points.append((r, sig))
                next_point = True
            sig_100 = sig

print(starting_points)
print(ending_points)
