from typing import TypedDict
import httpx


class CrackCode(object):
    """
        Identify verification code

        postPic(image:bytes|url,codetype):

        postPicAsync(image:bytes|url,codetype):

        codetype : http://www.chaojiying.com/price.html

        return:

        err_no=int, err_str=str, pic_id=str, pic_str=str, md5=str
    """

    ResultModel = TypedDict("ResultModel", err_no=int, err_str=str, pic_id=str, pic_str=str, md5=str)

    def __init__(self, headers: dict | None = None):
        """
        'pass2': md5(password.encode('utf8')).hexdigest(),
        """
        self.base_data = {
            'user': 'liangxiuyu',
            'pass2': "b9c23cc6007dcec86a7577770790e534",
            'softid': '927673',  # 用户中心>>软件ID 生成一个替换 96001
            'len_min': 4
        }
        self.headers = headers or {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
        }

        self.base_url = "http://upload.chaojiying.net/Upload/Processing.php"

    def postPic(self, image: bytes | str, codetype: str = "1004") -> ResultModel:
        """
        image: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        print("-> Nomal identifing verification code...")
        # Isinstance image bytes or Url link
        if isinstance(image, bytes):
            files = {'userfile': ('code.jpg', image)}
        else:
            res = httpx.get(image, headers=self.headers)
            files = {'userfile': ('code.jpg', res.content)}

        self.base_data.update({'codetype': codetype})
        response = httpx.post(self.base_url, data=self.base_data, files=files, headers=self.headers)
        return response.json()

    async def postPicAsync(self, image: bytes | str, codetype: str = "1004") -> ResultModel:

        print("-> Async identifing verification code...")

        client = httpx.AsyncClient(headers=self.headers)

        # Isinstance image bytes or Url link
        if isinstance(image, bytes):
            files = {'userfile': ('code.jpg', image)}
        else:
            res = await client.get(image)
            files = {'userfile': ('code.jpg', res.content)}

        self.base_data.update({'codetype': codetype})

        response = await client.post(self.base_url, data=self.base_data, files=files)

        _ = await client.aclose()

        # print("Code Result:",response.text)
        return response.json()

    def reportError(self, image_id):
        """
        im_id:报错题目的图片ID
        """
        print("-> Report to server this error")
        self.base_data.update({
            'id': image_id,
        })
        r = httpx.post('http://upload.chaojiying.net/Upload/ReportError.php', data=self.base_data, headers=self.headers)
        return r.json()
