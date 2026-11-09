import numpy as np, json
from PIL import Image
import os; D=os.environ.get('MOCK_BASE','.').rstrip('/')+'/'
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import page_path, NPAGES
def small(i, rot=0):
    im = Image.open(page_path(i))
    if rot: im = im.rotate(180)
    return 1 - np.asarray(im.reduce(10), dtype=np.float32) / 255.
R = {'F': small(1, 1), 'K': small(2, 1)}
def score(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))
res = []
for i in range(1, NPAGES + 1):
    cand = []
    for rot in (0, 1):
        a = small(i, rot)
        for side in 'FK':
            cand.append((score(a, R[side]), side, rot))
    cand.sort(reverse=True)
    res.append((i,) + cand[0] + (round(cand[0][0]-cand[1][0],3),))
for r in res: print(r)
json.dump(res, open(D+'work/orient.json', 'w'))
