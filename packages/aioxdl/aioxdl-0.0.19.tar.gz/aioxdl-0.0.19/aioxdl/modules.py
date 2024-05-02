import time, aiohttp, asyncio
from aioxdl.functions import Hkeys
from aioxdl.scripts import Scripted
from yt_dlp import YoutubeDL, DownloadError
#====================================================================================================

class Downloader:

    def __init__(self, **kwargs):
        self.dsizes = 0
        self.tsizes = 0
        self.stimes = time.time()
        self.comand = Hkeys.DATA01
        self.fnames = Hkeys.DATA02
        self.chunks = kwargs.get("chunk", 1024)
        self.result = kwargs.get("result", None)
        self.errors = kwargs.get("errors", None)

#====================================================================================================
    
    async def filename(self, filelink):
        with YoutubeDL(self.comand) as ydl:
            try:
                resultse = ydl.extract_info(filelink, download=False)
                filename = ydl.prepare_filename(resultse, outtmpl=self.fnames)
            except DownloadError:
                filename = Scripted.DATA02
            except Exception:
                filename = Scripted.DATA02

            return filename

#====================================================================================================
    
    async def getsizes(self, response):
        return int(response.headers.get("Content-Length", 0)) or 0

    async def checkurl(self, url, timeout=20):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                return 200 if response.status == 200 else response.status

#====================================================================================================

    async def download(self, url, location, timeout, progress, kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                self.tsize += await self.getsizes(response)
                with open(location, "wb") as handlexo:
                    while True:
                        chunks = await response.content.read(self.chunks)
                        if not chunks:
                            break
                        handlexo.write(chunks)
                        self.dsizes += self.chunks
                        try: await self.display(progress, kwargs)
                        except ZeroDivisionError: pass

                await response.release()
                return location if location else None

#====================================================================================================

    async def start(self, url, flocations, **kwargs):
        try:
            timeouts = kwargs.get("timeout", 1000)
            progress = kwargs.get("progress", None)
            flocations = await self.download(url, flocations, timeouts, progress, kwargs)
        except aiohttp.ClientConnectorError as errors:
            self.errors = errors
        except asyncio.TimeoutError:
            self.errors = Scripted.DATA01
        except Exception as errors:
            self.errors = errors

        return flocations

#====================================================================================================

    async def display(self, progress, kwargs):
        await progress(self.stimes, self.tsizes, self.dsizes, kwargs) if progress else None

#====================================================================================================
