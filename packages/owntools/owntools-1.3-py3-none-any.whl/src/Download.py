import asyncio
import httpx
from typing import List
from tqdm import tqdm
from urllib.parse import urlparse
from pathlib import Path


def getDonwloadsPath():
    import winreg
    """ 获取windows下downloads文件夹路径 """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]


class AsyncDownloader(object):

    def __init__(self, thread_num: int, url: str, folder: str, filename: str | None = None, proxies=False):
        """
            Async Download

            Args:
                thread_num (int): async num
                url (str): download url
                folder (str): save path
                filename (str, optional): If Defaults to None it will get name from the url
                proxies (bool, optional): Chose if to use the 127.0.0.1:1080 sockets proxies. Defaults to False.
        """

        self.proxies = "http://127.0.0.1:1080" if proxies else None

        if not filename:
            filename = urlparse(url).path.split('/')[-1]

        self.url = url
        self.client = httpx.AsyncClient(proxies=self.proxies)
        self.thread_num = thread_num

        self.folder_path = Path(folder)  # .joinpath(Path(filename).stem)
        self.file_path = self.folder_path.joinpath(filename)

        self.file_size = self._get_file_size()
        self.cut_info = self._cutting()

        # Progress Bar
        self.tqdm_obj = tqdm(total=self.file_size, unit_scale=True, unit_divisor=1024, unit="B")

        self._create_folder(self.folder_path)

    def __call__(self):
        self.main()

    def _create_folder(self, folder_path):
        """
            Create a folder path

            Args:
                folder_path (path): normal path or Path obj
        """
        p = Path(folder_path)

        if not p.exists():
            p.mkdir()

        return

    def _get_file_size(self):

        with httpx.stream("GET", self.url, proxies=self.proxies) as res:

            size = res.headers.get("Content-Length")

            if not size:
                size = len(res.read())

            return int(size)

    def _cutting(self):
        """
        切割成若干份
        :param file_size: 下载文件大小
        :param thread_num: 线程数量
        :return:
        :[0, 31409080],
        :[31409081, 62818160],
        :[62818161, 94227240],
        :[94227241, 125636320],
        :[125636321, 157045400],
        :[157045401, 188454480],
        :[188454481, 219863560],
        :[219863561, 251272640],
        :[251272641, 282681720],
        :[282681721, '-']]
        """
        cut_info: List[List[int | str]] = []
        cut_size = self.file_size // self.thread_num

        for num in range(self.thread_num):
            cut_info.append([cut_size*num + 1, cut_size * (num + 1)])

            if num == self.thread_num - 1:
                cut_info[-1][1] = "-"
            elif num == 0:
                cut_info[0][0] = 0

        return cut_info

    def _merge_files(self):
        """
        合并分段下载的文件
        :param file_path:
        :return:
        """

        with open(self.file_path.absolute(), 'ab') as f_count:
            for index in range(self.thread_num):

                sub_file = self.folder_path.joinpath(f"{index}_{self.file_path.name}")

                with open(sub_file.absolute(), 'rb') as sub_write:
                    f_count.write(sub_write.read())

                # 合并完成删除子文件
                sub_file.unlink()

        return

    async def downloader(self, index, start_size, stop_size, retry=False):

        sub_file = self.folder_path.joinpath(f"{index}_{self.file_path.name}")

        if sub_file.exists():
            temp_size = sub_file.stat().st_size  # 本地已经下载的文件大小
            if not retry:
                self.tqdm_obj.update(temp_size)  # 更新下载进度条
        else:
            temp_size = 0

        stop_size = "" if stop_size == '-' else stop_size

        headers = {'Range': f'bytes={start_size + temp_size}-{stop_size}'}

        down_file = open(sub_file.absolute(), 'ab')

        try:
            async with self.client.stream("GET", self.url, headers=headers) as response:
                num_bytes_downloaded = response.num_bytes_downloaded
                async for chunk in response.aiter_bytes():
                    if chunk:
                        down_file.write(chunk)
                        self.tqdm_obj.update(response.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = response.num_bytes_downloaded

        except Exception as e:
            print("{}:请求超时,尝试重连\n报错信息:{}".format(index, e))
            await self.downloader(index, start_size, stop_size, retry=True)

        finally:
            down_file.close()

        return

    async def main_download(self):

        index = 0
        tasks = []
        for info in self.cut_info:
            task = asyncio.create_task(self.downloader(index, info[0], info[1]))
            tasks.append(task)
            index += 1

        await asyncio.gather(*tasks)
        await self.client.aclose()

    async def async_main(self):
        """ 异步中下载防止event loop """
        if self.file_path.exists():
            if self.file_path.stat().st_size >= self.file_size:
                print(f"{self.file_path.name} Already exists.")
                return

        await self.main_download()
        self._merge_files()

    def main(self):

        if self.file_path.exists():
            if self.file_path.stat().st_size >= self.file_size:
                print(f"{self.file_path.name} Already exists.")
                return

        asyncio.run(self.main_download())
        self._merge_files()


if __name__ == "__main__":

    folder = "D:/Downloads"
    url = r"https://d3.qinkan.net/d/mobi/26/%E3%80%8A%E5%87%A1%E4%BA%BA%E4%BF%AE%E4%BB%99%E4%BC%A0%E3%80%8B(%E7%B2%BE%E6%A0%A1%E7%89%88)_qinkan.net.mobi"
    AsyncDownloader(20, url, folder, proxies=False)()
 
