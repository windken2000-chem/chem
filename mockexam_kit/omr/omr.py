import json, sys, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from common import *
from PIL import Image
C = json.load(open(D+'work/centers.json')); SH = json.load(open(D+'work/shifts.json'))
# 可選：work/omr_link.json＝{"題號": "參考題號"}，該題不自行對位、直接沿用同一面相鄰題的位移（題號字母印得淡、對位不穩時用）
QMAX = int(os.environ.get('MOCK_GRID_QMAX', '36'))
LINK = json.load(open(D+'work/omr_link.json')) if os.path.exists(D+'work/omr_link.json') else {}
REF = {s: 1 - np.asarray(Image.open(D+f'work/med_{s}.png'), dtype=np.float32)/255. for s in 'FK'}
def search(ref, tgt, y0, y1, x0, x1, gy, gx, R=14):
    rw = ref[y0:y1, x0:x1]; rw = rw - rw.mean()
    best = (-1e9, gy, gx)
    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            tw = tgt[y0+gy+dy:y1+gy+dy, x0+gx+dx:x1+gx+dx]
            s = float((rw*(tw - tw.mean())).sum())
            if s > best[0]: best = (s, gy+dy, gx+dx)
    return best[1], best[2]
def process(i):
    side = 'F' if i % 2 else 'K'
    ref = REF[side]; tgt = load(i)
    out = {}
    order = sorted(C[side], key=lambda q: q in LINK)
    for q in order:
        cs = C[side][q]
        xs = [c[0] for c in cs]; yc = cs[0][1]
        half = SH[str(i)][0] if xs[0] < 2482 else SH[str(i)][1]
        gy, gx = -half[0]*4, -half[1]*4
        if q in ('39', '47'):
            y0, y1, x0, x1 = int(yc-30), int(yc+30), int(xs[0]-40), int(xs[-1]+150)
        else:
            y0, y1, x0, x1 = int(yc-44), int(yc-8), int(xs[0]-40), int(xs[-1]+40)
        if q in LINK and LINK[q] in out: dy, dx = out[LINK[q]]['d']
        else: dy, dx = search(ref, tgt, y0, y1, x0, x1, gy, gx)
        f = []
        for cx, cy in cs:
            yy, xx = int(round(cy+dy)), int(round(cx+dx))
            if q in ('39', '47'): v = tgt[yy-16:yy+17, xx-16:xx+17].mean()
            else: v = tgt[yy-5:yy+6, xx-16:xx+17].mean()
            f.append(round(float(v), 3))
        out[q] = {'d': (dy, dx), 'f': f}
    # 對位異常修正（只用在格子密集的選擇題區，列距約 60 px；題號由環境變數 MOCK_GRID_QMAX 指定，預設 36）：
    # 與上下鄰近 4 題位移中位數差 > 8 px 者（多半是對到隔壁列的字母）改用鄰近題位移重新取樣
    fixed = {}
    for q, cs in C[side].items():
        if q in ('39', '47') or side != 'F' or int(q) > QMAX: continue
        half = cs[0][0] < 2482; yc = cs[0][1]
        nb = sorted((abs(C[side][k][0][1] - yc), k) for k in C[side] if k != q and k not in ('39', '47') and int(k) <= QMAX and (C[side][k][0][0] < 2482) == half)[:4]
        if len(nb) < 2: continue
        my = float(np.median([out[k]['d'][0] for _, k in nb])); mx = float(np.median([out[k]['d'][1] for _, k in nb]))
        dy, dx = out[q]['d']
        if abs(dy - my) > 8 or abs(dx - mx) > 8:
            dy, dx = int(round(my)), int(round(mx)); f = []
            for cx, cy in cs:
                yy, xx = int(round(cy+dy)), int(round(cx+dx))
                f.append(round(float(tgt[yy-5:yy+6, xx-16:xx+17].mean()), 3))
            fixed[q] = {'d': (dy, dx), 'f': f, 'fixed': True}
    out.update(fixed)
    return out
if __name__ == '__main__':
    from multiprocessing import Pool
    with Pool(8) as p: res = p.map(process, range(1, NPAGES + 1))
    json.dump({str(i+1): r for i, r in enumerate(res)}, open(D+'work/omr.json', 'w'))
    print('done')
