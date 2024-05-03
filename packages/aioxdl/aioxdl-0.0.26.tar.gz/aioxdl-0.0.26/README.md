<p align="center">
    📦 <a href="https://pypi.org/project/aioxdl" style="text-decoration:none;">AIO DOWNLOADER</a>
</p>

<p align="center">
   <a href="https://telegram.me/clinton_abraham"><img src="https://img.shields.io/badge/𝑪𝒍𝒊𝒏𝒕𝒐𝒏 𝑨𝒃𝒓𝒂𝒉𝒂𝒎-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/Space_x_bots"><img src="https://img.shields.io/badge/Sᴘᴀᴄᴇ ✗ ʙᴏᴛꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/sources_codes"><img src="https://img.shields.io/badge/Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
</p>

## INSTALLATION
```bash
pip install aioxdl
```

## USAGE

```python
import asyncio
from aioxdl.modules import Aioxdl

async def progress(stime, tsize, dsize):
    # stime = start_time
    # tsize = total_size
    # dsize = download_size
    percentage = round((dsize / tsize) * 100, 2)
    print("\rCOMPLETED : {}%".format(percentage), end="", flush=True)

async def main():
    core = Aioxdl(timeout=2000)
    link = "https://example.link/file.txt"
    loca = await core.filename(link)
    file = await core.start(link, loca, progress=progress)
    fine = file if core.errors == None else core.errors
    print(fine)

asyncio.run(main())
```

## GET FILENAME
```python
from aioxdl.modules import Aioxdl

async def main():
    core = Aioxdl()
    link = "https://example.link/file.txt"
    name = await core.filename(link)
    print(name)

asyncio.run(main())
```

