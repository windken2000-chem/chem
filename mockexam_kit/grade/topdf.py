import sys, asyncio
from playwright.async_api import async_playwright
async def main(src, out):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto('file://' + src)
        await pg.wait_for_timeout(500)
        await pg.pdf(path=out, format='A4', print_background=True, prefer_css_page_size=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
