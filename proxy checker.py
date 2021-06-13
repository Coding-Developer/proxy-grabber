import asyncio, httpx
import sys

from bs4 import BeautifulSoup

sema = asyncio.BoundedSemaphore(10)

a = 0


async def fetch(ip):
    global a
    a += 1
    print(a)

    try:
        proxies = {
            "http://": f"http://{ip}",
            "https://": f"http://{ip}"
        }

        async with httpx.AsyncClient(proxies=proxies) as session:
            response = await session.get('https://httpbin.org/ip')
            resp = response.text
            print(resp)

            with open(r'C:\Users\mway\PycharmProjects\proxy-grabber\working proxies.txt', 'a') as wfile:
                wfile.write(ip + '\n')




    except Exception:
        pass


async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        await res


def proxies():
    file1 = open(r'C:\Users\mway\PycharmProjects\proxy-grabber\scraped proxies.txt', 'r', encoding='utf-8')

    Lines = file1.readlines()
    for line in Lines:
        yield line.strip()


def start():
    coros = [
        fetch(p)  # try username as password

        for p in proxies()
    ]

    loop = asyncio.get_event_loop()

    # use threads
    all_workers = asyncio.gather(print_when_done(coros))

    results = loop.run_until_complete(all_workers)
    loop.close()


print('Proxy checker..')
print('Now checking..')
start()
