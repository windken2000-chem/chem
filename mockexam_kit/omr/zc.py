import sys
from PIL import Image
from common import load_u8
p=int(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); out=sys.argv[6]; s=float(sys.argv[7]) if len(sys.argv)>7 else 0.5
im=Image.fromarray(load_u8(p)).crop((x0,y0,x1,y1))
im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS); im.save('../chk/'+out)
