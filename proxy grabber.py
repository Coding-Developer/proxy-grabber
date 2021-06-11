import re
import asyncio
from aiohttp import ClientSession



ProxyPattern = re.compile(
    r'(?P<ip>(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))'
    r'(?=.*?(?:(?:(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))|(?P<port>\d{2,5})))',
    flags=re.DOTALL,
)




count = 0
async def scrape(*urls, debug=False):


    async with ClientSession() as session:
        for url in urls:
            try:
                resp = await session.get(url)
                if resp.status <= 400:
                    data = await resp.text()
                    for ip, port in ProxyPattern.findall(await resp.text()):
                        if port != '':

                            wfile = open('scraped proxies.txt', 'a')

                            wfile.write(ip + ':' + port + '\n')

                            wfile.close()



                         #   print(f"{ip}:{port}")

            except:
                continue



def removedups(inputfile, outputfile):
    lines = open(inputfile, 'r').readlines()
    lines_set = set(lines)
    out = open(outputfile, 'w')
    for line in lines_set:
        out.write(line)



def main(*urls,debug=False):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        return loop.run_until_complete(scrape(*urls,debug))

    finally:
        loop.close()
        asyncio.set_event_loop(None)




def urls():
    ''' 6 thousand proxy urls '''

    file1 = open('proxy urls.txt', 'r', encoding='utf-8')

    Lines = file1.readlines()
    for line in Lines:
        yield line.strip()


#removedups('scraped proxies.txt','newt.txt')

#for u in urls():
 #   main(u)


