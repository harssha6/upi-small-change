"""Render media/counter.html frame by frame into media/out/counter.mp4 (+ gif, contact sheet)."""
import asyncio, pathlib, shutil, subprocess, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).parent
FPS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
FRAMES = ROOT / 'frames'; OUT = ROOT / 'out'
CHROME = '/Users/harsshavardan/Library/Caches/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-mac-arm64/chrome-headless-shell'

async def main():
    shutil.rmtree(FRAMES, ignore_errors=True); FRAMES.mkdir(); OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME)
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        logs = []; pg.on('pageerror', lambda e: logs.append(str(e))); pg.on('console', lambda m: logs.append(f'{m.type}: {m.text}'))
        await pg.goto((ROOT / 'counter.html').as_uri(), wait_until='networkidle')
        await pg.evaluate('window.__ready'); await pg.wait_for_timeout(300)
        dur = await pg.evaluate('window.DURATION'); n = int(dur * FPS)
        for i in range(n):
            shown = await pg.evaluate(f'window.__frame({1 / FPS})')
            await pg.locator('#c').screenshot(path=str(FRAMES / f'f{i:04d}.png'))
            if i % 30 == 0: print(f'frame {i}/{n} t={i / FPS:.1f}s shown={shown}', flush=True)
        print('\n'.join(logs) or 'no console output')
        await b.close()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', str(FRAMES / 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '22', '-movflags', '+faststart', str(OUT / 'counter.mp4')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'counter.mp4'), '-vf', 'fps=10,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=bayer', str(OUT / 'counter.gif')], check=True)
    # contact sheet of 8 frames
    from PIL import Image
    picks = [int(n * f) for f in (0.02, 0.08, 0.16, 0.3, 0.5, 0.7, 0.85, 0.99)]
    ims = [Image.open(FRAMES / f'f{i:04d}.png').resize((360, 450)) for i in picks]
    sheet = Image.new('RGB', (360 * 4, 450 * 2), 'white')
    for k, im in enumerate(ims): sheet.paste(im, ((k % 4) * 360, (k // 4) * 450))
    sheet.save(OUT / 'sheet.png'); Image.open(FRAMES / f'f{n - 1:04d}.png').save(OUT / 'last.png')
    print('done', n, 'frames')
asyncio.run(main())
