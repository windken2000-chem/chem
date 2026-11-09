# 自動量測格子座標（版面不同時用，取代手動 measure.py/centers.py）
# 用法：在 work 資料夾執行 python3 autogrid.py rows.json
#   rows.json：{"F": {"1": [y概略, x0, x1], ...}, "K": {...}}（y 為格子中心的概略值，±25 px 內即可）
#   需要 mean_F.png / mean_K.png（meanimg.py 產生：所有答案卷對位後的平均影像，格框與劃記都清楚）
# 輸出 centers.json：每題 6 格 (x, y) 中心
import json, sys, numpy as np
from PIL import Image
ROWS = json.load(open(sys.argv[1]))
NOPT = 6
def runs(line, x0, lo=30, hi=70):
    out = []; s = None
    for i, v in enumerate(list(line) + [False]):
        if v and s is None: s = i
        if not v and s is not None:
            if lo <= i - s <= hi: out.append(x0 + (s + i - 1) / 2)
            s = None
    return out
C = {'F': {}, 'K': {}}
for side in 'FK':
    m = np.asarray(Image.open(f'mean_{side}.png')) < 225
    for q, (y0, x0, x1) in ROWS.get(side, {}).items():
        best = None
        for yt in range(int(y0) - 25, int(y0) + 10):
            for hgt in range(11, 18):
                a = runs(m[yt, x0:x1], x0); b = runs(m[yt + hgt, x0:x1], x0)
                sc = len(a) + len(b)
                if best is None or sc > best[0]: best = (sc, yt, hgt, a + b)
        sc, yt, hgt, xs = best
        xs = sorted(xs)
        # 依格距分群→各格中心
        grp = []
        for x in xs:
            if grp and x - grp[-1][-1] < 25: grp[-1].append(x)
            else: grp.append([x])
        cen = [float(np.mean(g)) for g in grp]
        C[side][q] = {'yc': yt + hgt / 2, 'cen': cen, 'score': sc}
# 全域格距：以各列相鄰中心差的中位數
d = [b - a for s in C for v in C[s].values() for a, b in zip(v['cen'], v['cen'][1:]) if 70 < b - a < 130]
SP = float(np.median(d)); print('SP', SP, 'n', len(d))
OUT = {'F': {}, 'K': {}}
for side in 'FK':
    for q, v in C[side].items():
        x0 = ROWS[side][q][1]
        # 估 A 格：每個中心回推 A=c-SP*j，取眾數附近中位數
        ests = []
        for c in v['cen']:
            j = round((c - v['cen'][0]) / SP)
            ests.append(c - SP * j)
        a0 = float(np.median(ests))
        OUT[side][q] = [(round(a0 + SP * j, 1), round(v['yc'], 1)) for j in range(NOPT)]
        print(side, q, 'y', v['yc'], 'n', len(v['cen']), 'A', round(a0, 1), 'score', v['score'])
json.dump(OUT, open('centers.json', 'w'))
