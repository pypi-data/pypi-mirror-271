from datetime import datetime
def id_card_to_age(id_card):
    '''
    身份证号码换算为年龄
    :param id_card: 身份证号码
    :return: 年龄
    '''
    if len(id_card) != 18:
        raise ValueError("身份证号码长度错误")

    birth_year = int(id_card[6:10])
    birth_month = int(id_card[10:12])
    birth_day = int(id_card[12:14])

    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    age = current_year - birth_year

    if (birth_month, birth_day) > (current_month, current_day):
        age -= 1
    return age

from random import shuffle
# 按要求生成n副扑克牌，每副牌有54张，然后洗牌
def gen_poker(shuffled=True, n=1):
    '''
    随机生成 n 副扑克牌
    :param shuffled: 是否洗牌
    :param n: 几副牌
    :return: 扑克牌列表
    '''
    number = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
    kind = ['黑桃', '红桃', '梅花', '方块']
    pk = [j + '-' + i for i in number for j in kind] + ['King', 'Queen']
    pk = pk * n
    if shuffled: shuffle(pk)
    return pk

import re
from subprocess import check_output
import pandas as pd

def get_wifi_password():
    '''

    :return: 登录wifi过的ap和密码 字典
    '''
    cmd = 'netsh wlan show profile key=clear '
    get_results = lambda cmd, res: re.findall(res, check_output(cmd, universal_newlines=True))
    wifi_ssid = get_results(cmd, ':\s(.+)')
    return {i: get_results(cmd + i, '[关键内容|Content]\s+:\s(\w+)') for i in wifi_ssid}

from pathlib import Path
def directory_to_str(directory_path=Path.home(), sep='\n'):
    """
    :param directory_path: 目录名
    :param sep: 分隔符
    :return: 返回一个目录下的子目录和文件，返回字符串
    """

    directory = Path(directory_path)
    print(f'Please wait for browsing {directory_path}..... ')
    # 获取目录下的所有子目录和文件（包括子目录的子目录）
    all_items = map(str, list(directory.rglob('*')))
    return sep.join(all_items)

def get_reg_parameters(x, y, data):
    """

    :param x: dataframe colum name_x
    :param y: dataframe colum name_x
    :param data: dataframe name
    :return:
    {'slope': -0.384322, 'intercept': 3.7414,
    'r_value': -0.389, 'p_value': 0.339, 'std_err ': 0.3705}
	Slope：如果斜率接近于1，则表明数据之间存在较强的线性关系。
	Intercept：截距的大小表示回归模型的拟合程度。
	r-value：r-value表示回归线和数据之间的相关性。r-value越接近于1，则说明回归模型对数据的拟合越好。
	p-value：p-value表示回归系数是否有统计学意义。如果p-value小于0.05，则说明回归系数有统计学意义。
	std_err：标准误差反映了拟合数据的精度。std_err越小，拟合数据的精度越高。

    """
    from scipy.stats import linregress
    x, y = data[x], data[y]
    names = 'slope', 'intercept', 'r_value', 'p_value', 'std_err '
    values = linregress(x, y)
    return dict(zip(names, values))


