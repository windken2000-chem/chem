# 【換答案卷版面時要改】BOX：各非選擇題作答區範圍 (side, (x0,y0,x1,y1))
import sys
from PIL import Image,ImageDraw,ImageFont
from common import load_u8
import os,sys; sys.path.insert(0, os.path.join(os.environ.get('MOCK_BASE','.'),'work'))
from roster import SHEET_SEAT
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
BOX={'38':('F',(2560,700,4720,1300)),'39':('F',(2560,1480,4720,2110)),'41':('F',(2560,2190,4720,3150)),
     '44':('K',(455,450,2390,1030)),'47':('K',(455,1250,2390,1845)),'51':('K',(455,2225,2390,3140)),
     '52':('K',(2680,360,4690,1230)),'55':('K',(2680,1450,4690,2140)),'60':('K',(2680,2610,4690,3140))}
try:
    from exam_config import WBOX as _WB
    BOX = {str(k): v for k, v in _WB.items()}
except ImportError:
    pass
q=sys.argv[1]; s=float(sys.argv[2]); cols=int(sys.argv[3]); per=int(sys.argv[4])
side,b=BOX[q]
idx=list(range(len(SHEET_SEAT)))
for g in range(0,len(idx),per):
    grp=idx[g:g+per]; w=int((b[2]-b[0])*s); h=int((b[3]-b[1])*s)
    rows=(len(grp)+cols-1)//cols
    M=Image.new('L',(cols*(w+60),rows*(h+6)),255); d=ImageDraw.Draw(M)
    for k,i in enumerate(grp):
        p=2*i+1 if side=='F' else 2*i+2
        im=Image.fromarray(load_u8(p)).crop(b).resize((w,h),Image.LANCZOS)
        x=(k%cols)*(w+60); y=(k//cols)*(h+6)
        M.paste(im,(x+56,y)); d.rectangle((x+56,y,x+56+w-1,y+h-1),outline=0)
        d.text((x+2,y+8),str(SHEET_SEAT[i]),fill=0,font=f)
    M.save(f'../chk/w{q}_{g//per}.png')
