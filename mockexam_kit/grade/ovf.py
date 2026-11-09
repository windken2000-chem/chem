import sys, asyncio
from playwright.async_api import async_playwright
async def main(src):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://' + src); await pg.wait_for_timeout(400)
        r = await pg.evaluate('''() => [...document.querySelectorAll('.page')].map((p,i)=>{
            const foot=p.querySelector('.foot'); let maxb=0;
            for (const c of p.children){ if(c.classList.contains('foot')||c.classList.contains('side')) continue; const rb=c.getBoundingClientRect().bottom - p.getBoundingClientRect().top; if(rb>maxb) maxb=rb;}
            const fb = foot.getBoundingClientRect().top - p.getBoundingClientRect().top;
            return [i, Math.round(maxb), Math.round(fb)]; })''')
        bad=[x for x in r if x[1] > x[2]-4]
        print('pages',len(r),'overflow',bad[:20])
        print('max content by page side', max(x[1] for x in r[0::2]), max(x[1] for x in r[1::2]), r[0][2])
        await b.close()
asyncio.run(main(sys.argv[1]))
