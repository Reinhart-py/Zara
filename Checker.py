import asyncio
import aiohttp
import sys
import time

TEST_URL = 'http://httpbin.org/get'
TIMEOUT = 5
CONCURRENCY = 3000

G, W, F, E = '\033[2;36m', '\033[1;37m', '\033[2;32m', '\033[1;31m'

print(f'''
{G}                 _
{G}              _ | |
{G}   ____ _____ | | |
{G}  / ___) ___ | | |
{G} | |  | ____| | |
{G} |_|  |_____) |_|
{E}-----------------------------
{W}   Tool    : {F}Zara {W}v1.0
{W}   Credit  : {F}Reinhart
{E}-----------------------------
''')

async def check(s, p, stats):
    try:
        async with s.get(TEST_URL, proxy=f"http://{p}", timeout=TIMEOUT) as resp:
            if resp.status == 200:
                stats['working'].append(p)
    except Exception:
        pass
    finally:
        stats['checked'] += 1

async def reporter(start_time, stats, total):
    while stats['checked'] < total:
        elapsed = time.monotonic() - start_time
        rate = stats['checked'] / elapsed if elapsed > 0 else 0
        hits = len(stats['working'])
        progress = (stats['checked'] / total) * 100
        
        print(
            f"{W}Alive: {F}{hits}{W} | "
            f"Checked: {G}{stats['checked']}/{total}{W} ({progress:.1f}%) | "
            f"Speed: {F}{rate:.0f}/s{W}", end='\r'
        )
        await asyncio.sleep(0.1)

async def run():
    f_in = sys.argv[1] if len(sys.argv) > 1 else "proxies.txt"
    f_out = "working.txt"

    try:
        with open(f_in, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies: raise FileNotFoundError
    except FileNotFoundError:
        print(f"{E}Can't find '{f_in}' or it's empty.")
        return

    total = len(proxies)
    stats = {'checked': 0, 'working': []}
    start_time = time.monotonic()

    print(f"{W}Loaded {G}{total}{W} proxies. Firing on all cylinders...")
    print(f'{E}-----------------------------{W}')

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None, ssl=False)) as s:
        sem = asyncio.Semaphore(CONCURRENCY)
        async def task_wrapper(p):
            async with sem:
                await check(s, p, stats)
        
        reporter_task = asyncio.create_task(reporter(start_time, stats, total))
        await asyncio.gather(*(task_wrapper(p) for p in proxies))
        reporter_task.cancel()

    with open(f_out, 'w') as f:
        f.write('\n'.join(stats['working']))
    
    end_time = time.monotonic()
    elapsed = end_time - start_time
    rate = total / elapsed if elapsed > 0 else 0
    hits = len(stats['working'])

    print(f"\n{E}-----------------------------{W}")
    print(f"Finished in {G}{elapsed:.2f}s{W}. Results below.")
    print(f"Total: {G}{total}{W} | Alive: {F}{hits}{W} | Avg Speed: {F}{rate:.0f}/s")
    print(f"Working proxies saved to {G}{f_out}{W}.")
    print(f"{E}-----------------------------{W}")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print(f"\n{E}Aborted.{W}")
