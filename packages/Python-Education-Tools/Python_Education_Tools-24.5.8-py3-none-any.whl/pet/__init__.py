from pet.this import  *
import shutil,os
from pathlib import Path
from importlib.abc import Traversable
from importlib.resources import files
# 创建用户使用本案例的工作目录
pet_home = Path.home() / 'pet_home'
pet_home.mkdir(parents=True, exist_ok=True)
pet_desktop = Path.home() / 'Desktop/Python与数据分析及可视化教学案例'


def download_textbook1(dst=pet_desktop):
    """
    将教学案例拷贝到用户桌面
    :param dst: 拷贝文件的目标目录，默认是用户桌面
    :return:
    """
    src: Traversable = files('pet.textbook_case')
    print('Copying,please wait....')
    shutil.copytree(str(src), dst, dirs_exist_ok=True)
    print('done!!')
    os.startfile(dst)

download_textbook1()