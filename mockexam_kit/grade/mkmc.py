import json, os, sys
# 把 decode.py 的 dec.json 整理成每位學生的選擇題作答 mc.json（含人工更正）
WORK = os.path.join(os.environ.get('MOCK_BASE', '.'), 'work'); sys.path.insert(0, WORK)
from exam_config import KEY, MC_OVERRIDES
D = json.load(open(os.path.join(WORK, 'dec.json')))
MCQ = [str(q) for q in sorted(KEY)]
npages = len(D); out = {}
for s in range(npages // 2):
    a = {}
    for p in (2 * s + 1, 2 * s + 2):
        for q, v in D[str(p)].items():
            if q in MCQ: a[q] = v
    a.update(MC_OVERRIDES.get(s, {}))
    miss = [q for q in MCQ if q not in a]
    assert not miss, (s, miss)
    out[s] = {q: a[q] for q in MCQ}
json.dump(out, open(os.path.join(WORK, 'mc.json'), 'w'), ensure_ascii=False)
print('students', len(out))
