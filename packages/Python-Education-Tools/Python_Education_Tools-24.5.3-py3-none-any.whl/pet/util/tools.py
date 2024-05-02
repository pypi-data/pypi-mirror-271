from datetime import datetime
def id_card_to_age(id_card):
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
    cmd = 'netsh wlan show profile key=clear '
    get_results = lambda cmd, res: re.findall(res, check_output(cmd, universal_newlines=True))
    wifi_ssid = get_results(cmd, ':\s(.+)')
    return {i: get_results(cmd + i, '[关键内容|Content]\s+:\s(\w+)') for i in wifi_ssid}


def get_nic():
    cmd = 'netsh trace show interfaces'
    get_results = lambda cmd, res: re.findall(res, check_output(cmd, universal_newlines=True))

    return get_results(cmd, '描述:\s+(.+)')