import json, os, sys, statistics as st
# 通用計分程式：考試相關設定都在工作資料夾的 exam_config.py 與 roster.py
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.environ.get('MOCK_BASE', '.'), 'work')
sys.path.insert(0, HERE); sys.path.insert(0, WORK)
from exam_config import *
import roster as _r
SHEET_SEAT, NAMES = _r.SHEET_SEAT, _r.NAMES
NO_SHEET = getattr(_r, 'NO_SHEET', sorted(set(NAMES) - set(SHEET_SEAT)))
STUDENT_ID = getattr(_r, 'STUDENT_ID', {})   # 學號可省略
ROSTER = [(s, NAMES[s]) for s in SHEET_SEAT]
B = '未作答'
WQ = {}
for q in FULL:
    ns = {}; exec(open(os.path.join(WORK, 'written', f'w{q}.py'), encoding='utf-8').read(), ns); WQ[q] = ns['W']
    assert set(WQ[q]) == set(SHEET_SEAT), q
    assert all(0 <= v[0] <= FULL[q] for v in WQ[q].values()), q
W = {i: {q: WQ[q][seat] for q in FULL} for i, seat in enumerate(SHEET_SEAT)}
MC = json.load(open(os.path.join(WORK, 'mc.json')))
MULTI = {q for q, k in KEY.items() if len(k) > 1}
PTS = {q: 2 for q in KEY}; PTS.update(FULL)
QS = sorted(PTS)
assert sum(PTS.values()) == TOTAL_FULL, sum(PTS.values())
for sb in SUBJECTS: assert sum(PTS[q] for q in QS if SUBJ[q] == sb) == SUBJ_FULL, sb
assert sorted(q for _, _, qs in UNITS for q in qs) == QS
def to_level(x):
    if x <= 0: return 0
    for lv in range(1, 15):
        if x <= GRADE_UB[lv]: return lv
    return 15
def score_mc(q, ans):
    key = KEY[q]
    if q in MULTI:
        if not ans: return 0.0
        n = NOPT[q]; L = 'ABCDEF'[:n]
        k = sum(1 for c in L if (c in key) != (c in ans)) + sum(1 for c in ans if c not in L)
        return round(max(0.0, 2 * (n - 2 * k) / n), 2)
    return 2.0 if ans == key else 0.0
STUDENTS = []
for s in range(len(ROSTER)):
    ans = MC[str(s)]
    item = {}
    for q in QS:
        if q in KEY:
            a = ans.get(str(q), '')
            item[q] = {'ans': a or '—', 'pts': score_mc(q, a), 'full': 2}
        else:
            p, c = W[s][q]
            item[q] = {'ans': c, 'pts': float(p), 'full': FULL[q]}
    tot = round(sum(v['pts'] for v in item.values()), 2)
    p1 = round(sum(item[q]['pts'] for q in P1_QS), 2)
    p2 = round(tot - p1, 2)
    wr = round(sum(item[q]['pts'] for q in FULL), 1)
    subj = {sb: round(sum(item[q]['pts'] for q in QS if SUBJ[q] == sb), 2) for sb in SUBJECTS}
    units = [(sb, nm, qs, round(sum(item[q]['pts'] for q in qs), 2), sum(PTS[q] for q in qs)) for sb, nm, qs in UNITS]
    blanks = [q for q in QS if (q in KEY and item[q]['ans'] == '—') or (q in FULL and W[s][q][1].startswith(B))]
    multi_partial = [q for q in MULTI if 0 < item[q]['pts'] < 2]
    seat, name = ROSTER[s]
    STUDENTS.append(dict(idx=s, seat=seat, name=name, item=item, total=tot, p1=p1, p2=p2, written=wr,
                         subj=subj, units=units, blanks=blanks, multi_partial=multi_partial, level=to_level(tot)))
tots = sorted((x['total'] for x in STUDENTS), reverse=True)
for x in STUDENTS:
    x['rank'] = 1 + sum(t > x['total'] + 1e-9 for t in tots)
CLASS = {
 'n': len(STUDENTS), 'avg': round(st.mean(tots), 1), 'median': round(st.median(tots), 1), 'max': max(tots), 'min': min(tots), 'sd': round(st.stdev(tots), 1),
 'subj': {sb: round(st.mean(x['subj'][sb] for x in STUDENTS), 1) for sb in SUBJECTS},
 'q': {q: round(st.mean(x['item'][q]['pts'] for x in STUDENTS) / PTS[q], 3) for q in QS},
 'unit': {nm: round(st.mean(u[3] / u[4] for x in STUDENTS for u in x['units'] if u[1] == nm), 3) for _, nm, _ in UNITS},
 'p1': round(st.mean(x['p1'] for x in STUDENTS), 1), 'p2': round(st.mean(x['p2'] for x in STUDENTS), 1),
 'written': round(st.mean(x['written'] for x in STUDENTS), 1),
 'levels': sorted(x['level'] for x in STUDENTS),
}
CLASS['level_avg'] = round(st.mean(CLASS['levels']), 1)
if __name__ == '__main__':
    for x in sorted(STUDENTS, key=lambda x: x['rank']):
        print(x['rank'], x['seat'], x['name'], x['total'], x['level'], x['p1'], x['p2'], x['written'], x['subj'], 'blank', len(x['blanks']))
    print(CLASS['avg'], CLASS['median'], CLASS['max'], CLASS['min'], CLASS['sd'], CLASS['subj'], CLASS['p1'], CLASS['p2'], CLASS['written'], CLASS['level_avg'])
    print(sorted(CLASS['unit'].items(), key=lambda kv: kv[1]))
    print(sorted(CLASS['q'].items(), key=lambda kv: kv[1])[:18])
    print('levels', CLASS['levels'])
