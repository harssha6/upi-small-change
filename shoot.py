import asyncio, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).parent
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1280
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/Users/harsshavardan/Library/Caches/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-mac-arm64/chrome-headless-shell')
        pg = await b.new_page(viewport={"width": W, "height": 820}, device_scale_factor=1)
        logs = []
        pg.on("console", lambda m: logs.append(f"{m.type}: {m.text}"))
        pg.on("pageerror", lambda e: logs.append(f"PAGEERROR: {e}"))
        await pg.goto((ROOT / "index.html").as_uri(), wait_until="networkidle")
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f"shots/hero-{W}.png")
        await pg.add_style_tag(content="html{scroll-behavior:auto!important}")
        # scroll through so lazy charts render and reveals fire
        h = await pg.evaluate("document.body.scrollHeight")
        for y in range(0, h, 600):
            await pg.evaluate(f"scrollTo(0,{y})"); await pg.wait_for_timeout(120)
        await pg.evaluate("scrollTo(0, document.body.scrollHeight)")
        await pg.wait_for_timeout(2200)
        print("height", h, "| hero:", await pg.inner_text('#h-count'))
        await pg.screenshot(path=f"shots/light-{W}.png", full_page=True)
        async def docbox(sel, idx=0):
            return await pg.evaluate("([s,i]) => {const r=document.querySelectorAll(s)[i].getBoundingClientRect(); return {y:r.top+scrollY,h:r.height}}", [sel, idx])
        for i in range(1, 8):
            box = await docbox(f'#c{i}')
            await pg.screenshot(path=f"shots/c{i}.png", full_page=True, clip={"x": 0, "y": box["y"], "width": W, "height": min(box["h"], 1100)})
        for i in range(3):
            box = await docbox('.bleed', i); await pg.screenshot(path=f"shots/bleed{i}.png", full_page=True, clip={"x": 0, "y": box["y"], "width": W, "height": box["h"]})
        await pg.click('#theme'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f"shots/dark-{W}.png", full_page=True)
        async def hover(sel, name, fx=0.5, fy=0.5):
            await pg.locator(sel).first.scroll_into_view_if_needed(); await pg.wait_for_timeout(150)
            box = await pg.locator(sel).first.bounding_box()
            await pg.mouse.move(box["x"] + box["width"] * fx, box["y"] + box["height"] * fy); await pg.wait_for_timeout(150)
            print(name, "tip:", (await pg.inner_text('#tip')).replace("\n", " | ")[:120])
        await hover('#chart4 rect.b', 'skyline'); await hover('#chart5 circle', 'ladder'); await hover('#chart7 rect', 'state'); await hover('#chart6 .hit', 'stack', 0.6); await hover('#chart2 .cell rect', 'calendar')
        await pg.evaluate("document.querySelector('[data-sort=\"share\"]').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
        await pg.click('[data-sort="share"]'); await pg.wait_for_timeout(1300)
        box = await docbox('#c4 .fig'); await pg.screenshot(path="shots/c4-share.png", full_page=True, clip={"x": 0, "y": box["y"], "width": W, "height": box["h"]})
        await pg.evaluate("document.querySelector('[data-lane=\"1\"]').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
        await pg.click('[data-lane="1"]'); await pg.wait_for_timeout(500)
        print("nav solid:", await pg.evaluate("document.getElementById('nav').classList.contains('solid')"))
        print("\n".join(logs) or "no console output")
        await b.close()
asyncio.run(main())
