from setuptools import setup, find_packages

VERSION = '0.0.1'
name = 'neco_m3u8'
author = 'neco_arc'
description = 'm3u8解析与下载库,自动获取key解密,需要ffmpeg用于合并ts流'
email = '3306601284@qq.com'

with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name=name,
    version=VERSION,
    author=author,
    author_email=email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    package_dir={'neco_m3u8': 'src'},
    packages=['neco_m3u8'],
    python_requires='>=3.9',
    install_requires=[
        'requests',
        'pycryptodome',
        'DownloadKit',
        'm3u8'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
