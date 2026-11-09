import json, numpy as np
# 每頁自動門檻：bg＝所有格子塗黑度中位數，mk＝明顯劃記的中位數，thr＝(bg+mk)/2
# 在 work 資料夾執行；勾選框題號（如 39、47）不參與
CHECKBOX = ('39', '47')
O = json.load(open('omr.json')); T = {}
for p in O:
    v = np.array([x for q, d in O[p].items() if q not in CHECKBOX for x in d['f']])
    bg = float(np.percentile(v, 50)); hi = v[v > max(0.12, bg + 0.08)]
    mk = float(np.median(hi)) if len(hi) else 0.3
    T[p] = [round(bg, 3), round(mk, 3), round((bg + mk) / 2, 3)]
json.dump(T, open('thr.json', 'w'))
low = sorted(T.items(), key=lambda kv: kv[1][1])[:5]
print('劃記最淡的 5 頁（需人工核對）:', low)
