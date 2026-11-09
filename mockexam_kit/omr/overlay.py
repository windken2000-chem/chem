import json, sys
from PIL import Image, ImageDraw
import os; D=os.environ.get('MOCK_BASE','.').rstrip('/')+'/'
R=json.load(open(D+'work/omr.json')); C=json.load(open(D+'work/centers.json')); T=json.load(open(D+'work/thr.json'))
def ov(p, box, out, scale=0.5):
    side='F' if p%2 else 'K'
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from common import load_u8
    im=Image.fromarray(load_u8(p)).convert('RGB'); d=ImageDraw.Draw(im)
    thr=T[str(p)][2]
    for q,cs in C[side].items():
        dy,dx=R[str(p)][q]['d']; f=R[str(p)][q]['f']
        for (cx,cy),v in zip(cs,f):
            x,y=cx+dx,cy+dy
            col='red' if v>=thr else ('orange' if v>=0.6*thr else None)
            w,h=(20,20) if q in ('39','47') else (24,12)
            if col: d.rectangle((x-w,y-h,x+w,y+h),outline=col,width=4)
            else: d.rectangle((x-w,y-h,x+w,y+h),outline=(120,180,255),width=1)
    im=im.crop(box); im=im.resize((int(im.width*scale),int(im.height*scale)))
    im.save(out)
if __name__=='__main__':
    p=int(sys.argv[1]); side='F' if p%2 else 'K'
    box=(380,1330,2300,3280) if side=='F' and (len(sys.argv)<3 or sys.argv[2]=='L') else ((2650,550,3600,3260) if side=='F' else (500,350,3600,2650))
    ov(p, box, D+f'chk/ov{p}{"" if len(sys.argv)<3 else sys.argv[2]}.png')
