from .Common import requests_retry
from pprint import pprint
from PIL import Image


def checkOneImage(path):
    ''' 判断path是否为有效图片，是返回true，否返回flase且删除文件 '''
    try:
        Image.open(path)
        return True
    except IOError:
        # os.remove(path)
        return False


def downloadImage(url, name, path, _header=None):
    '''
    下载一张图片
    
    TODO: Change the suffix 
    '''

    # print(f"Donwloading Image: {name}")

    response = requests_retry(url, _header)

    if response:

        image_path = f'{path}{name}.jpg'

        with open(image_path, 'wb') as f:
            f.write(response.content)

        if checkOneImage(image_path):
            return True
        else:
            print(f"Donloaded wrong image: {name}")
            return False

    else:
        # print(f"Failed Donload: {name}")
        return False
