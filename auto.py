import numpy as np
from scipy.optimize import minimize
from event import Event
import random
import time


def read_file(data):
    with open('outreach.csv') as f:
        for line in f:
            try:
                current = Event(line)
            except Exception:
                continue

            weight = current.weight
            line = [float(x) if float(x) != int(float(x)) else int(float(x)) for x in line.split(',')]
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


def random_points():
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


num_starting_points = 10
start = False
starting_points = []
for i in range(num_starting_points):
    while not start:
        r = random_points()
        new_data, sig = multiple_cuts(data, r)

        if sig > 0.3 and sig != np.inf:
            start = True

            starting_points.append((r, sig))


def increment(r, n):
    if n % 2 == 0:
        r[n // 2][0] += 1
    else:
        r[n // 2][1] -= 1
    return r


# stop = False
# turns = 0
# while not stop:
#     turns += 1
#
#     r = increment(r, 12)
#     #print(r)
#     new_data, new_sig = multiple_cuts(data, r)
#     if new_sig < sig:
#         stop = True
#         print(sig)
#         print(turns)
#         print(r)
#     else:
#         sig = new_sig

# for i in range(2, 14):
#     stop = False
#     turns = 0
#     while not stop:
#         turns += 1
#
#         r = increment(r, i)
#         # print(r)
#         new_data, new_sig = multiple_cuts(data, r)
#         if new_sig < sig:
#             stop = True
#             print(sig)
#             print(turns)
#             print(r)
#         else:
#             sig = new_sig

ranges = [[0, 8],
          [0, 200],
          [0, 200],
          [0, 3.2],
          [0, 3.2],
          [0, 200]]

increments = [1, 1, 1, 0.01, 0.01, 1]


def make_rand_vector(dims, scale):
    vec = [random.gauss(0, 1) for i in range(dims)]
    mag = sum(x ** 2 for x in vec) ** 0.5
    return [(x * scale) / mag for x in vec]


def denormalize(v, ranges):
    temp_ranges = [ranges[i // 2][1] for i in range(2 * len(ranges))]
    for i in range(len(v)):
        v[i] *= temp_ranges[i]
    return v


def rand(r, ranges):
    v = []
    for i in range(len(r)):
        vi = random.choice([-1, 1]) * increments[i]
        vj = random.choice([-1, 1]) * increments[i]
        if r[i][0] == ranges[i][0]:
            vi = random.choice([0, 1]) * increments[i]
        if r[i][1] == ranges[i][1]:
            vj = random.choice([-1, 0]) * increments[i]
        v.append(vi)
        v.append(vj)
    return v


def apply_vec(r, v):
    r = np.array(r).flatten()
    for i in range(len(v)):
        r[i] += v[i]
    temp = []
    for i in range(0, len(r), 2):
        temp.append([r[i], r[i + 1]])
    return temp


def crop_vec(r):
    r.pop(0)
    r.pop()
    return r


def recrop_vec(r):
    r.insert(0, [2, 3])
    r.insert(len(r), [0, 1])
    return r


def rand_one_change(r, ranges):
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

ending_points = []
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
