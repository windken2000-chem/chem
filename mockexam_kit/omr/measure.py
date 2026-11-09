# 【換答案卷版面時要改】ROWS 為各題列的概略 y 座標與 x 範圍（對照 med_F.png / med_K.png）
import numpy as np, json
from PIL import Image
import os; D=os.environ.get('MOCK_BASE','.').rstrip('/')+'/work/'
M={s:np.asarray(Image.open(D+f'med_{s}.png'))<150 for s in 'FK'}
def edge_rows(m,x0,x1,yc,R=40):
    prof=m[yc-R:yc+R,x0:x1].sum(1)
    idx=np.argsort(prof)[::-1]
    # pick top two peaks separated by 12-22 px
    best=None
    for i in idx[:12]:
        for j in idx[:12]:
            if 12<=j-i<=22:
                sc=prof[i]+prof[j]
                if best is None or sc>best[0]: best=(sc,yc-R+i,yc-R+j)
    return best
def runs(m,y,x0,x1):
    line=m[y-1:y+2,x0:x1].any(0)
    out=[];s=None
    for i,v in enumerate(line):
        if v and s is None: s=i
        if not v and s is not None:
            if 28<=i-s<=60: out.append(round(x0+(s+i-1)/2,1))
            s=None
    return out
ROWS={'F':{}, 'K':{}}
# left grid
ly=[1433,1501,1570,1638,1707,1810,1879,1947,2015,2084,2187,2256,2324,2393,2462,2565,2633,2702,2771,2839,2942,3011,3079,3148,3216]
for q,y in enumerate(ly,1): ROWS['F'][q]=(y,450,1260)
for q,y in zip(range(26,37),ly[:11]): ROWS['F'][q]=(y,1400,2250)
for q,y in ((37,628),(40,2132),(42,3184)): ROWS['F'][q]=(y,2700,3560)
for q,y in ((43,412),(45,1068),(46,1192),(48,1956),(49,2076),(50,2180)): ROWS['K'][q]=(y,560,1350)
for q,y in ((53,1292),(54,1412),(56,2228),(57,2336),(58,2448),(59,2560)): ROWS['K'][q]=(y,2740,3540)
OUT={'F':{},'K':{}}
for side in 'FK':
    m=M[side]
    for q,(y,x0,x1) in sorted(ROWS[side].items()):
        e=edge_rows(m,x0,x1,y)
        yt,yb=e[1],e[2]
        xs=runs(m,yt,x0,x1); xs2=runs(m,yb,x0,x1)
        OUT[side][q]={'yt':int(yt),'yb':int(yb),'xs':xs,'xs2':xs2}
        print(side,q,yt,yb,xs,xs2)
json.dump(OUT,open(D+'meas.json','w'))
