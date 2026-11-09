import sys, asyncio
from playwright.async_api import async_playwright
async def main(src, idx, out):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':800,'height':1200})
        await pg.goto('file://' + src); await pg.wait_for_timeout(400)
        el = (await pg.query_selector_all('.page'))[int(idx)]
        await el.screenshot(path=out)
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3]))
