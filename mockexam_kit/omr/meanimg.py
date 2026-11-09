# 所有答案卷對位後的平均影像 mean_F.png / mean_K.png（格框與劃記都清楚，給 autogrid.py 量格子用）
import json, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from PIL import Image
SH = json.load(open(D + 'work/shifts.json'))
for side, pages in (('F', range(1, NPAGES + 1, 2)), ('K', range(2, NPAGES + 1, 2))):
    acc=None
    for i in pages:
        a = load_u8(i).astype(np.float32)
        h = SH[str(i)]; out=np.empty_like(a); W = a.shape[1] // 2
        for k, (x0, x1) in enumerate(((0, W), (W, a.shape[1]))):
            dy, dx = -h[k][0] * 4, -h[k][1] * 4
            out[:, x0:x1] = np.roll(np.roll(a[:, x0:x1], -dy, axis=0), -dx, axis=1)
        acc = out if acc is None else acc+out
    Image.fromarray((acc/len(pages)).astype(np.uint8)).save(D+f'work/mean_{side}.png')
