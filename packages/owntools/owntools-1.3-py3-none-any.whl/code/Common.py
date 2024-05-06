import datetime
import json
import requests
import re
from retry import retry
from pprint import pprint
import functools
import time


class DateEncode(json.JSONEncoder):
    '''
    TypeError: Object of type 'datetime' is not JSON serializable 解决方法：


    这个错误的原因是json.dumps无法对字典中的datetime时间格式数据进行转化，dumps的原功能是将dict转化为str格式，不支持转化时间，所以需要将json类部分内容重新改写，来处理这种特殊日期格式。

    使用方式： json.dumps(dict,cls=DateEncoder)

    '''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.timedelta):
            return obj.seconds
        else:
            return json.JSONEncoder.default(self, obj)

def creat_cookies(from_path: str, to_path: str):
    with open(from_path, "r") as file:
        cookies = json.loads(file.read())

    real_cookies = {}
    for item in cookies['cookies']:
        real_cookies[item['name']] = item['value']

    with open(to_path, "w") as file:
        _ = file.write(json.dumps(real_cookies, indent=4))

def get_run_time(info="used"):
    def _time_me(fn):
        print("Begin to timing:", fn.__name__)

        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            start = time.perf_counter()
            print("Start at:", start)
            fn(*args, **kwargs)
            print("%s %s %s" % (fn.__name__, info, time.perf_counter() - start), "second")

        return _wrapper

    return _time_me


def get_headers(copys):
    headers = copys
    headers = headers.strip().split('\n')
    # 使用字典生成式将参数切片重组，并去掉空格，处理带协议头中的://
    headers = {x.split(':')[0].strip(): ("".join(x.split(':')[1:])).strip().replace('//', "://") for x in headers}
    # 使用json模块将字典转化成json格式打印出来

    return headers


def get_suffix(filename):
    """ Get file's suffix """
    return re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', filename)[0]


def search_torrent(content) -> str | None:

    # In case name like : hhd1080
    content = re.sub("hhd", "", content)
    content = re.sub("chd", "", content)
    content = re.sub("1080", "", content)
    torrent_pattern = '[a-z]{2,5}[0-9]{3,5}|[A-Z]{2,5}-[0-9]{3,5}'

    torrent = re.search(torrent_pattern, content)
    torrent = torrent.group() if torrent else None

    if torrent:
        part_pattern = '([a-zA-Z]{2,5})-([0-9]{2,5})'
        name_part = re.search(part_pattern, torrent)

        if name_part:

            first_part = name_part.group(1).lower()
            second_part = name_part.group(2)

            for _ in range(5 - len(second_part)):
                second_part = '0' + second_part

            torrent = first_part + second_part

    return torrent


def isChinese(word):
    """ 判断word中是否含有汉字 """
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def isJapanese(word):
    """ 判断word中是否含有日语 """
    for ja in word:
        if '\u0800' <= ja <= '\u4e00':
            return True
    return False


def change_path_form(path: str):
    new_path = eval(repr(path).replace('\\', '/'))
    return new_path


@retry(tries=3, delay=3)
def requests_retry(url, _header=None):
    ''' 提取并分析一页内容时的requests方法，使用retry装饰器自动重试，失败则抛出异常)

    成功返回response 错误返回false'''
    if _header:
        response = requests.get(url, headers=_header, timeout=10)
    else:
        response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response
    else:
        # print(f'Response status code wrong : {response.status_code}')
        return False


def write_json(all_data, file_name='test', ensure=True):

    with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(all_data, indent=4, ensure_ascii=ensure))


if __name__ == '__main__':
    print(time.perf_counter())
