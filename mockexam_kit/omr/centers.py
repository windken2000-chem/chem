# 【換答案卷版面時要改】xa_default（各區 A 格的 x）、SP（格距）、勾選框座標
import json, numpy as np
import os; D=os.environ.get('MOCK_BASE','.').rstrip('/')+'/work/'
M=json.load(open(D+'meas.json'))
SP=136.8
def xa_default(side,q):
    q=int(q)
    if side=='F': return 512 if q<=25 else (1472 if q<=36 else 2770)
    return 612 if q<=50 else 2798
C={'F':{},'K':{}}
for side in 'FK':
    rows=M[side]
    est={}
    for q,v in rows.items():
        xs=v['xs']+v['xs2']; xa=xa_default(side,q)
        if int(q)<=25 and side=='F': xa=512+ (int(q)-1)*0.4  # skew drift
        vals=[x-SP*round((x-xa)/SP) for x in xs if abs((x-xa)/SP-round((x-xa)/SP))<0.15 and 0<=round((x-xa)/SP)<=5]
        est[q]=(np.median(vals) if len(vals)>=2 else None, (v['yt']+v['yb'])/2)
    for q,(a,yc) in est.items():
        if a is None:
            # neighbors in same panel
            nb=[est[k][0] for k in est if est[k][0] is not None and abs(int(k)-int(q))<=3 and xa_default(side,k)==xa_default(side,q)]
            a=float(np.mean(nb))
        C[side][q]=[(round(a+SP*j,1), yc) for j in range(6)]
C['F']['39']=[(2758,1543),(3045,1543),(3332,1543),(3618,1543),(3993,1543)]
C['K']['47']=[(838.5,1407.5),(1257,1407),(1675.5,1407),(2093.5,1407)]
json.dump(C,open(D+'centers.json','w'))
for side in 'FK':
    for q in sorted(C[side],key=int): print(side,q,[c[0] for c in C[side][q]][:6], C[side][q][0][1])
