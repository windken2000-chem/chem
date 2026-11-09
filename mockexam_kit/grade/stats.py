import json, statistics as st
from collections import Counter
import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'score.py'),encoding='utf-8').read().split("if __name__ == '__main__':")[0])
_pp=os.path.join(WORK,'prev_totals.json'); E2=json.load(open(_pp)) if os.path.exists(_pp) else {}
for sb in SUBJECTS:
    vals=[x['subj'][sb] for x in STUDENTS]
    same=[(x['subj'][sb],E2[str(x['seat'])][2][sb]) for x in STUDENTS if str(x['seat']) in E2]
    print('##',sb,'avg',round(st.mean(vals),2),'rate',round(st.mean(vals)/SUBJ_FULL,3),'med',st.median(vals),'min',min(vals),'max',max(vals),
          '<half:',sum(v<SUBJ_FULL/2 for v in vals),'>=75%:',sum(v>=SUBJ_FULL*0.75 for v in vals),
          'E2 same-n',len(same),'now',round(st.mean(a for a,b in same),2) if same else '-','prev',round(st.mean(b for a,b in same),2) if same else '-')
    qs=[q for q in QS if SUBJ[q]==sb]
    for q in qs:
        r=CLASS['q'][q]; full=sum(1 for x in STUDENTS if x['item'][q]['pts']>=PTS[q]-1e-9)
        if q in KEY:
            c=Counter(x['item'][q]['ans'] for x in STUDENTS)
            wrong=[(a,n) for a,n in c.most_common() if a!=KEY[q]][:4]
            optw=''
            if q in MULTI:
                n=NOPT[q]; L='ABCDEF'[:n]
                ow={o:sum(1 for x in STUDENTS if x['item'][q]['ans']!='—' and ((o in KEY[q])!=(o in x['item'][q]['ans']))) for o in L}
                optw=' opt-err '+' '.join(f'{o}{"*" if o in KEY[q] else ""}:{v}' for o,v in ow.items())
            print(f'  Q{q} {TOPIC[q]} key={KEY[q]} rate={r:.2f} full={full} wrong={wrong}{optw}')
        else:
            dist=Counter(x['item'][q]['pts'] for x in STUDENTS)
            print(f'  Q{q} {TOPIC[q]} W full={PTS[q]} rate={r:.2f} full={full} dist={sorted(dist.items())}')
    print('  low:',sorted([(x['subj'][sb],x['seat'],x['name']) for x in STUDENTS])[:8])
