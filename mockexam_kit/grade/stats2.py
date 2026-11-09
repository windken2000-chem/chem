import json, statistics as st
from collections import Counter
import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'score.py'),encoding='utf-8').read().split("if __name__ == '__main__':")[0])
# 各科非選擇題題號取自 exam_config.WR；沒有就依 SUBJ 自動分組
try: WR
except NameError: WR = {sb: [q for q in FULL if SUBJ[q] == sb] for sb in SUBJECTS}
for sb in SUBJECTS:
    mcq=[q for q in KEY if SUBJ[q]==sb]; wq=WR[sb]
    mcr=st.mean(sum(x['item'][q]['pts'] for q in mcq) for x in STUDENTS)/(2*len(mcq))
    wr=st.mean(sum(x['item'][q]['pts'] for q in wq) for x in STUDENTS)/sum(FULL[q] for q in wq) if wq else 0
    vals=[x['subj'][sb] for x in STUDENTS]; hi=SUBJ_FULL*0.75; lo=SUBJ_FULL*0.5
    print(sb,'MC',round(mcr,3),'W',round(wr,3),f'bands >={hi:g}',sum(v>=hi for v in vals),'mid',sum(lo<=v<hi for v in vals),f'<{lo:g}',sum(v<lo for v in vals))
mc_all=st.mean(sum(x['item'][q]['pts'] for q in KEY) for x in STUDENTS)/(2*len(KEY))
print('MC all',round(mc_all,3),'W all',round(CLASS['written']/sum(FULL.values()),3))
# 題組得分率（exam_config.GROUPS）
for nm,qs,_ in GROUPS:
    qs=list(qs); tot=sum(PTS[q] for q in qs); print(nm, round(st.mean(sum(x['item'][q]['pts'] for q in qs) for x in STUDENTS)/tot,3))
# 各非選擇題空白人數與批改說明分類（取說明前 14 字）
for q in FULL:
    print(q,'blank',sum(1 for x in STUDENTS if W[x['idx']][q][1].startswith(B)))
    print('  ',Counter(W[x['idx']][q][1][:14] for x in STUDENTS).most_common(6))
# 各科低於一半的學生與失分題
for sb in SUBJECTS:
    low=sorted([x for x in STUDENTS if x['subj'][sb]<SUBJ_FULL*0.5],key=lambda x:x['subj'][sb])
    print(sb,[(x['seat'],x['name'],x['subj'][sb],[q for q in QS if SUBJ[q]==sb and x['item'][q]['pts']<PTS[q]-1e-9]) for x in low])
print(sorted([(round(CLASS['q'][q],3),q,SUBJ[q],TOPIC[q]) for q in QS])[:12])
