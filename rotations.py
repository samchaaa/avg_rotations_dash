import numpy as np
import pandas as pd
from settings import Settings


def get_sign(data):

    # Get sign of each bar (-1, 0, 1)
    data['sign'] = np.sign(data['close'] - data['open'])

    # Group together (including 0's at end of group)
    prev = data['sign'][0]
    g = 0
    for i, s in zip(data.index, data['sign']):
        if s == 1:
            if prev == 1:
                # continue up group
                # print(i, s, 'yes', g)
                data.loc[i, 'g'] = g
            else:
                # new up group
                # iterate group
                g += 1
                # print(i, s, 'new', g)
                data.loc[i, 'g'] = g
        if s == -1:
            if prev == -1:
                # continue down group
                # print(i, s, 'yes', g)
                data.loc[i, 'g'] = g
            else:
                # new down group
                # iterate group
                g += 1
                # print(i, s, 'new', g)
                data.loc[i, 'g'] = g
        if s == 0:
            # add to last group
            # print(i, s, 'add to last', g)
            data.loc[i, 'g'] = g
        prev = s
    return data


def get_rotations(data):

    r = []
    for x in range(int(max(data['g']))):
        # if g == x or x+1, find min/max
        # if g sign is +, find the +/- rot (high)
        # if g sign is -, find -/+ rot (low)

        if data.loc[data['g'] == x, 'sign'].iloc[0] > 0:
            h = data.loc[(data['g'] == x) | (data['g'] == x+1), 'high']
            i = h.idxmax()
            h = h.max()
            # data.loc[i, 'r'] = h
            r.append([i, h])
        if data.loc[data['g'] == x, 'sign'].iloc[0] < 0:
            l = data.loc[(data['g'] == x) | (data['g'] == x+1), 'low']
            i = l.idxmin()
            l = l.min()
            # data.loc[i, 'r'] = l
            r.append([i, l])

    return pd.DataFrame(r)


def final(inst, r):

    r = r.rename(columns={0: 'datetime', 1: 'price'})
    r['diff'] = r['price'].diff()
    # "Absolute difference"... movement in absolute distance.
    r['abs_diff'] = abs(r['diff'])

    # dependent on scaling
    if any(map(lambda x: x in inst.lower(), ['jpy'])):
        point = 100
    elif any(map(lambda x: x in inst.lower(), ['btcusd', 'usa500idxusd', 'usatechidxusd'])):
        point = 1
    else:
        point = 10000

    r[['diff', 'abs_diff']] = r[['diff', 'abs_diff']] * point

    # Rolling average of absolute movement.
    r['abs_diff_rolling'] = r['abs_diff'].rolling(Settings.ROTATIONS_AVG).mean()

    return r


