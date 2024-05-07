#setup.py代码里面的name一定要跟程序包src文件下的mylibrary一致
from setuptools import setup, find_packages
setup(
    name='AppAuthN',
    version='0.0.16',
    packages=find_packages('src'), #包含所有src中的包
    package_data={"AppAuthN": ["*.json"]},  # 包含src目录下的所有JSON文件
    package_dir={'': 'src'}, #告訴distutils包都在src下
    install_requires=['requests'],
    python_requires='>=3'
)