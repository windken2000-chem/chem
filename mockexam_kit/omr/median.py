import json, sys, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from common import *
from PIL import Image
SH = json.load(open(D + 'work/shifts.json'))
for side, pages in (('F', range(1, NPAGES + 1, 2)), ('K', range(2, NPAGES + 1, 2))):
    stack = []
    for i in list(pages)[:17]:
        a = load_u8(i)
        h = SH[str(i)]
        out = np.full_like(a, 255)
        W = a.shape[1] // 2
        for k, (x0, x1) in enumerate(((0, W), (W, a.shape[1]))):
            dy, dx = -h[k][0] * 4, -h[k][1] * 4   # tgt ~ ref rolled; tgt pos = ref - d
            sub = a[:, x0:x1]
            sub = np.roll(np.roll(sub, -dy, axis=0), -dx, axis=1)
            out[:, x0:x1] = sub
        stack.append(out)
    med = np.median(np.stack(stack), axis=0).astype(np.uint8)
    Image.fromarray(med).save(D + f'work/med_{side}.png')
    print(side, med.shape)
