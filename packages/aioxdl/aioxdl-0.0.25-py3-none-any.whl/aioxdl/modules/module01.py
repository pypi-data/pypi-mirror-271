import time, aiohttp, asyncio
from ..functions import Hkeys
from ..scripts import Scripted
from yt_dlp import YoutubeDL, DownloadError
#=========================================================================================================

class Aioxdl:

    def __init__(self, **kwargs):
        self.dsizes = 0
        self.tsizes = 0
        self.stimes = time.time()
        self.comand = Hkeys.DATA01
        self.fnames = Hkeys.DATA02
        self.chunks = kwargs.get("chunk", 1024)
        self.errors = kwargs.get("errors", None)
        self.otimes = kwargs.get("timeout", 1000)

#=========================================================================================================

    async def download(self, url, location, timeout, progress, kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                self.tsizes += await self.getsizes(response)
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

#=========================================================================================================

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

#=========================================================================================================

    async def getsizes(self, response):
        return int(response.headers.get("Content-Length", 0))

#=========================================================================================================

    async def display(self, progress, kwargs):
        if progress and kwargs:
            await progress(self.stimes, self.tsizes, self.dsizes, kwargs)
        elif progress:
            await progress(self.stimes, self.tsizes, self.dsizes)
        else: pass

#=========================================================================================================

    async def start(self, url, location, progress=None, **kwargs):
        try:
            location = await self.download(url, location, self.otimes, progress, kwargs)
        except aiohttp.ClientConnectorError as errors:
            self.errors = errors
        except asyncio.TimeoutError:
            self.errors = Scripted.DATA01
        except Exception as errors:
            self.errors = errors

        return location

#=========================================================================================================
