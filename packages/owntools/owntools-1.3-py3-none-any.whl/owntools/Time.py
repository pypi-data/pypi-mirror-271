import time
import re
import datetime
from time import gmtime, strftime


def find_date(content):

    pattern = "\\d{4}-\\d{1,2}-\\d{1,2}"
    result = re.findall(pattern, content)
    if result:
        return result[0]
    else:
        return ""


def get_t_time():

    return str(time.time())[:10]


def get_d_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_short_d_time():

    return datetime.datetime.now().strftime('%Y-%m-%d')


def translate_timestamp(timestamp: int, form: str = '%Y-%m-%d %H:%M:%S'):
    """ 将时间戳转换为form格式化字符串.默认：%Y-%m-%d %H:%M:%S """
    formatted_time = datetime.datetime.fromtimestamp(timestamp).strftime(form)
    return formatted_time


def convert_second(second):

    res = strftime("%H:%M:%S", gmtime(second))
    return (res)


def translate_time(_time, data_type):
    '''
    时间转换格式

    _time = 输入的时间

    data_type = 想要的格式：
        t_time = 时间戳形式
        d_time = datetime格式
    '''

    if data_type == 't_time':
        return int(time.mktime(time.strptime(_time, "%Y-%m-%d %H:%M:%S")))
    if data_type == 'd_time':
        timeArray = time.localtime(_time)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def convert_datetime(date: str):

    date_list = re.findall(r'([0-9]{4})\D([0-3]?[0-9])\D([0-3]?[0-9])', date)

    if date_list:
        date_list = [int(i) for i in date_list[0]]
        datetime_date = datetime.datetime(date_list[0], date_list[1], date_list[2])
        return datetime_date

    else:
        raise BaseException("Not validated date string.")


def calculate_date(date: str, num: int, format: str = "%Y-%m-%d"):
    """
        Calculate date with given args

        Args:
            date (str): %Y-%m-%d
            num (int): +num or -num
            format(str) : default is %Y-%m-%d

        Returns:
            str: format
    """

    datetime_date = convert_datetime(date)
    result = (datetime_date + datetime.timedelta(days=num)).strftime(format)

    return result
