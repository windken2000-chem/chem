import json
O=json.load(open('omr.json')); T=json.load(open('thr.json'))
L='ABCDEF'
res={}; amb=[]
for p in range(1,len(O)+1):
    o=O[str(p)]; bg,mk,thr=T[str(p)]
    for q,v in o.items():
        f=v['f']
        if q in ('39','47'):
            m=max(range(len(f)),key=lambda i:f[i])
            ans=str(m) if f[m]>0.06 else ''
            res.setdefault(p,{})[q]=ans
            srt=sorted(f,reverse=True)
            if 0.03<f[m]<0.09 or (len(srt)>1 and srt[1]>0.05): amb.append((p,q,[round(x,3) for x in f]))
            continue
        ans=''.join(L[i] for i,x in enumerate(f) if x>=thr)
        res.setdefault(p,{})[q]=ans
        band=[(L[i],round(x,3)) for i,x in enumerate(f) if 0.55*thr<=x<thr or thr<=x<1.25*thr]
        if band: amb.append((p,q,ans,band,round(thr,3)))
json.dump(res,open('dec.json','w'))
for a in amb: print(a)
print(len(amb))
