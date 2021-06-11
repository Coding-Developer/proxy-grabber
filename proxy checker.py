import asyncio
import httpx
import aiohttp

proxy_type = "http"
test_url = "http://chatango.com/"
timeout_sec = 15


def proxies():
    file1 = open(r'C:\Users\mway\PycharmProjects\proxy-grabber\scraped proxies.txt', 'r', encoding='utf-8')

    Lines = file1.readlines()
    for line in Lines:
        yield line.strip()


async def is_bad_proxy(ipport):
    with open('working proxies.txt', 'a') as wfile:

        try:
            proxyurl = "http://" + ipport
            session = aiohttp.ClientSession()
            resp = await session.get(test_url, proxy=proxyurl)
            print(ipport)
            wfile.write(ipport + '\n')

            session.close()
        except Exception:
            session.close()


tasks = []

loop = asyncio.get_event_loop()

for item in proxies():
    tasks.append(asyncio.ensure_future(is_bad_proxy(item)))

loop.run_until_complete(asyncio.wait(tasks))

loop.close()