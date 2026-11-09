import json, sys, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from common import *
refs = {1: down(load(1)), 2: down(load(2))}
out = {}
for i in range(1, NPAGES + 1):
    r = refs[1 if i % 2 else 2]; t = down(load(i))
    W = r.shape[1] // 2
    res = []
    for sl in (slice(0, W), slice(W, None)):
        dy, dx, c = phase_shift(r[:, sl], t[:, sl])
        res.append((dy, dx, round(c, 3)))
    out[i] = res
    print(i, res)
json.dump(out, open(D + 'work/shifts.json', 'w'))
