import re
import asyncio
from aiohttp import ClientSession



ProxyPattern = re.compile(
    r'(?P<ip>(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))'
    r'(?=.*?(?:(?:(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))|(?P<port>\d{2,5})))',
    flags=re.DOTALL,
)




count = 0

_run=True
async def scrape(*urls,limit):
    global count,_run

    while _run:

        try:
            async with ClientSession() as session:

                for url in urls:
                    resp = await session.get(url)
                    if resp.status <= 400:
                        data = await resp.text()
                        for ip, port in ProxyPattern.findall(await resp.text()):
                            if port != '':
                                count += 1
                                print(count)
                                if count == limit:

                                    _run = False
                                    removedups('scraped proxies.txt', 'scraped proxies.txt')


                                wfile = open('scraped proxies.txt', 'a')

                                wfile.write(ip + ':' + port + '\n')

                                wfile.close()



            break                #   print(f"{ip}:{port}")

        except:
            break



def removedups(inputfile, outputfile):
    lines = open(inputfile, 'r').readlines()
    lines_set = set(lines)
    out = open(outputfile, 'w')
    for line in lines_set:
        out.write(line)



def main(*urls,limit):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        return loop.run_until_complete(scrape(*urls,limit=limit))

    finally:
        loop.close()
        asyncio.set_event_loop(None)




def urls():
    ''' 2 thousand proxy urls '''

    file1 = open('proxy urls.txt', 'r', encoding='utf-8')

    Lines = file1.readlines()
    for line in Lines:
        yield line.strip()





for u in urls():
    main(u,limit=2000)



