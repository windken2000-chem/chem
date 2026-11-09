from PIL import Image,ImageDraw,ImageFont
from common import load_u8
import os
# 簽名／姓名欄範圍：預設為 112E3 版面；其他版面設環境變數 MOCK_NAME_BOX='x0,y0,x1,y1'
BOX = tuple(int(v) for v in os.environ.get('MOCK_NAME_BOX', '1250,540,2300,1060').split(','))
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
def tile(pages,out):
    s=0.32; w=int((BOX[2]-BOX[0])*s); h=int((BOX[3]-BOX[1])*s)
    cols=3; rows=(len(pages)+cols-1)//cols
    M=Image.new('L',(cols*(w+70),rows*(h+8)),255); d=ImageDraw.Draw(M)
    for k,p in enumerate(pages):
        im=Image.fromarray(load_u8(p)).crop(BOX).resize((w,h))
        x=(k%cols)*(w+70); y=(k//cols)*(h+8)
        M.paste(im,(x+65,y)); d.text((x+2,y+20),str((p+1)//2),fill=0,font=f)
    M.save('../chk/'+out)
from common import NPAGES
F=list(range(1,NPAGES+1,2))
for k in range(0,len(F),18): tile(F[k:k+18],f'names{k//18+1}.png')
