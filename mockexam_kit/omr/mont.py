import sys,json
from PIL import Image,ImageDraw,ImageFont
from common import load_u8
C=json.load(open('centers.json'))
def crop_q(p,q,pad=(60,60)):
    side='F' if p%2 else 'K'; cs=C[side][q]; xs=[c[0] for c in cs]; y=cs[0][1]
    if q in('39','47'): box=(int(xs[0]-60),int(y-60),int(xs[-1]+260),int(y+60))
    else: box=(int(xs[0]-120),int(y-60),int(xs[-1]+60),int(y+40))
    return Image.fromarray(load_u8(p)).crop(box)
items=[a.split(':') for a in sys.argv[2:]]
ims=[(f'p{p} Q{q}',crop_q(int(p),q)) for p,q in items]
s=0.6
W=max(int(i.width*s) for _,i in ims)+130; H=sum(int(i.height*s)+6 for _,i in ims)
out=Image.new('L',(W,H),255); d=ImageDraw.Draw(out)
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
except: f=None
y=0
for lab,i in ims:
    i=i.resize((int(i.width*s),int(i.height*s))); out.paste(i,(130,y)); d.text((4,y+10),lab,fill=0,font=f); y+=i.height+6
out.save('../chk/'+sys.argv[1])
