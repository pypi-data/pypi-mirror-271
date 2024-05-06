import time
import json
import requests
import re
import httpx

class Translation():
    def __init__(self):
        """
        Translate Function
        """
        import sys
        from importlib import reload
        reload(sys)

        self.YOUDAO_URL = 'https://openapi.youdao.com/api'
        self.APP_KEY = '55780d0d419052ba'
        self.APP_SECRET = 'cm9nQh6b4rrBfDBBEpWOD1i2eDTGkdCx'

    def encrypt(self, signStr):
        import hashlib
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    async def do_request_async(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        async with httpx.AsyncClient(headers=headers) as client:
            result = await client.post(self.YOUDAO_URL, data=data)
        return result

    def trans(self, from_language, content, useby='p'):
        """
        from_language : ja = japan; en = english;
        if useby = 'p' => filter bracket content
        """
        import uuid

        if useby == 'p':
            pattern = '\(.*?\)|（.*?）|\[.*?\]'
            content = re.sub(pattern, '', content, 0)

        if content.endswith('\\') or content.endswith("'"):
            content = content[:-1]

        data = {}
        data['from'] = from_language
        data['to'] = 'zh-CHS'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(content) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = content
        data['salt'] = salt
        data['sign'] = sign
        #data['vocabId'] = "您的用户词表ID"

        response = self.do_request(data)
        #contentType = response.headers['Content-Type']
        result = json.loads(response.content.decode())

        if result['errorCode'] == '0':
            return result['translation'][0]
        else:
            errorcode = result['errorCode']
            print(f'Translation wrong Error Code : {errorcode} \n Retring...')

            response = self.do_request(data)
            result = json.loads(response.content.decode())

            if result['errorCode'] == '0':
                return result['translation'][0]
            else:
                errorcode = result['errorCode']
                return f'Translation wrong Error Code : {errorcode}'

    async def trans_async(self, from_language, content, useby='p'):
        """
        from_language : ja = japan; en = english;
        if useby = 'p' => filter bracket content
        """
        import uuid
        if useby == 'p':
            pattern = '\(.*?\)|（.*?）|\[.*?\]'
            content = re.sub(pattern, '', content, 0)

        if content.endswith('\\') or content.endswith("'"):
            content = content[:-1]

        data = {}
        data['from'] = from_language
        data['to'] = 'zh-CHS'
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(content) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = content
        data['salt'] = salt
        data['sign'] = sign
        #data['vocabId'] = "您的用户词表ID"

        response = await self.do_request_async(data)
        #contentType = response.headers['Content-Type']
        result = json.loads(response.content.decode())

        if result['errorCode'] == '0':
            return result['translation'][0]
        else:
            errorcode = result['errorCode']
            print(f'Translation wrong Error Code : {errorcode} \n Retring...')

            response = await self.do_request_async(data)
            result = json.loads(response.content.decode())

            if result['errorCode'] == '0':
                return result['translation'][0]
            else:
                errorcode = result['errorCode']
                return f'Translation wrong Error Code : {errorcode}'
