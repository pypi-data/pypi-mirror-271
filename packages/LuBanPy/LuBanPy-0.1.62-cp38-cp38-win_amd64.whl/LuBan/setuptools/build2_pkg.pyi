#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：build2_pkg.py
@Author     ：Alex
@Date       ：2024/3/5 16:59 
@Function   ：构建生成发行包
"""
import os
from typing import Optional, Union, List, Tuple, Set, Dict,  Iterable
from pathlib import Path


class Build2PKG:


    def __init__(self, name: Optional[str] = None, version=None, modules=None, auto_install_requires_mode: int = 3):
        """
        初始化方法

        :param name:                      在 PyPI 上搜索的项目名称（名字不区分大小写）
        :param Optional[str] version:                   项目版本号，一般由三部分组成：MAJOR, MINOR, MAINTENANCE，保证每次发布都是版本都是唯一的
        :param modules:     指定需要打包的模块（不需要.py后缀）名包
        :param int auto_install_requires_mode:          自动包含安装依赖模式，0不自动包含，1只检查包存在，2指定版本，3保持自动更新
        """
        pass

    @property
    def name(self) -> str:
        """
        获取库元信息的名称
        :return:
        """
        pass

    def contact(self, author: Optional[str] = None, author_email: Optional[str] = None, maintainer: Optional[str] = None, maintainer_email: Optional[str] = None):
        """
        设置联系信息

        :param Optional[str] author:                    程序的作者
        :param Optional[str] author_email:              程序的作者的邮箱地址
        :param Optional[str] maintainer:                维护者
        :param Optional[str] maintainer_email:          维护者的邮箱地址
        :return:
        """
        pass

    def links(self, url: Optional[str] = None, download_url: Optional[str] = None, project_urls: Optional[Dict[str, str]] = None):
        """
        设置项目相关链接
        :param Optional[str] url:                       项目主页
        :param Optional[str] download_url:              下载软件包的位置
        :param Optional[Dict[str, str]] project_urls:   项目相关额外连接，如代码仓库，文档地址等。
            - 示例：
            {
                'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
                'Funding': 'https://donate.pypi.org',
                'Say Thanks!': 'http://saythanks.io/to/example',
                'Source': 'https://github.com/pypa/sampleproject/',
                'Tracker': 'https://github.com/pypa/sampleproject/issues',
            }
        :return:
        """
        pass

    def description(self, description: Optional[str] = None, long_description: Union[str, Path, None] = None, long_description_content_type: Optional[str] = None, keywords: Union[str, List[str], None] = None, platforms: Union[str, List[str], None] = None):
        """
        项目描术信息

        :param description:                         项目的简短描述，一般一句话就好，会显示在 PyPI 上名字下端
        :param long_description:                    对项目的完整描述，如果此字符串是 rst 格式的，PyPI 会自动渲染成 HTML 显示，当设置为Path类型时，自动读取文件内容。
        :param long_description_content_type:       不设置格式，默认是rst格式文档解读 或 根据文件后缀名自动识别
        :param keywords:                            项目关键词列表
        :param platforms:                           适用的软件平台列表
        :return:
        """
        pass

    def classifiers(self, classifiers: Union[str, List[str]]):
        """
        提供给pypi的分类依据，参考：https://pypi.org/classifiers/

        :param classifiers:     分类依据
        :return:
        """
        pass

    def license(self, license: Optional[str] = None, license_files: Optional[List] = None):
        """
        设置项目许可信息
        :param license:             指定包的许可证的字符串
        :param license_files:       应包含的许可证相关文件的全局模式列表。如果 或license_file均未license_files指定，则此选项默认为LICEN[CS]E*、COPYING*、NOTICE*和AUTHORS*。
        :return:
        """
        pass

    def find_packages(self, where: Union[str, os.PathLike] = '.', exclude: Union[str, Iterable[str]] = (), include: Iterable[str] = ('*',)):
        """
        搜索标准包

        :param where:
        :param exclude:
        :param include:
        :return:
        """
        pass

    def find_namespace_packages(self, where: Union[str, os.PathLike] = '.', exclude: Union[str, Iterable[str]] = (), include: Iterable[str] = ('*',)):
        """
        搜索Namespace包

        :param where:
        :param exclude:
        :param include:
        :return:
        """
        pass

    def packages(self, packages: Union[str, Iterable[str]]):
        """
        指示打包分发时需要包含的package
        一般通过find_packages或find_namespace_packages方法返回

        :param Iterable[str] packages:      指定包列表
        :return:
        """
        pass

    def package_dir(self, arg: Optional[Dict[str, str]] = None):
        """
        重新映射 package 和目录的关系
        :param arg:
        :return:
        """
        pass

    def package_data(self, data: Optional[Dict[str, Union[str, Iterable[str]]]] = None):
        """
        该参数是一个从包名称到 glob 模式列表的字典。
        如果数据文件包含在包的子目录中，则 glob 可以包括子目录名称。
        其格式一般为 {'package_name': ['files']}，
        比如：`package_data={'mypkg': ['data/*.dat'],}`
        :param data:        当设置为None时，清除`package_data`配置
        :return:
        """
        pass

    def include_package_data(self, include: bool):
        """
        include_package_data是bool类型，默认值为True。
        当为True时，将根据[MANIFEST.in](https://manifest.in/)文件来打包分发库。

        该参数被设置为 True 时自动添加包中受版本控制的数据文件，可替代 package_data，同时，`exclude_package_data` 可以排除某些文件。
        注意当需要加入没有被版本控制的文件时，还是仍然需要使用 package_data 参数才行
        :param bool include:
        :return:
        """
        pass

    def exclude_package_data(self, exclude: Optional[Dict[str, Union[str, Iterable[str]]]] = None):
        """
        用来指定要从软件包中排除的文件或目录。它接受一个字典作为参数，字典的键是软件包的相对路径，值是一个包含排除规则的列表。
        :param exclude: 当值为None时，清空exclude_package_data配置
        :return:
        """
        pass

    def data_files(self, files: Optional[Iterable[Tuple[str, Union[str, Iterable[str]]]]] = None):
        """
        包含项目外的文件, 如：配置文件，消息目录，数据文件

        如果数据文件存在于项目外，则可以使用 data_files 参数或者 MANIFEST.in 文件进行管理。
        - 如果用于源码包，则使用 MANIFEST.in；
        - 如果用于 wheel，则使用 data_files。

        ```data_files=[(‘mydata’, [‘data/conf.yml’])]```

        上述设置将在打包 wheel 时，将 data/conf.yml 文件添加至 mydata 目录。

        注意：data_files 不能使用路径通配符。
        :param files:   指定了一系列二元组，即`(目的安装目录，源文件)` ，表示哪些文件被安装到哪些目录中。如果目录名是相对路径，则相对于安装前缀进行解释
        :return:
        """
        pass

    def python_requires(self, val: Optional[str] = None):
        """
        指定python的版本进行限制
        :param val:     与 Python 版本的版本说明符（如 PEP 440 中定义）相对应的字符串，用于指定 PEP 345 中定义的 Requires-Python。
        :return:
        """
        pass

    def install_requires(self, requires: Union[str, Dict[str, Optional[str]], List[str], Tuple[str], Set[str], None], flag: bool = False):
        """
        项目依赖的 Python 库，使用 pip 安装本项目时会自动检查和安装依赖。

        :param requires:
            - str: 指定一个依赖项
            - Dict[str, str]:       通过key-value指定多个依赖项，key为库名，value为依赖配置
            - List[str], Tuple[str], Set[str]:   指定多个依赖项
            - None：  当requires为None和flag为True时，清空全部安装依赖配置
        :param bool flag:       合并模式，True强制覆盖（清空原来项），False追加新项或修改已有项
        :return:
        """
        pass

    def prepare(self, dist: bool = True, build_ext: Optional[bool] = None):
        """
        执行构建准备

        :param dist:        发行包方式
            - True:     以二进制包形式发布
            - False:    以源码包的方式发布
        :param build_ext:     是否执行编译，设置为None时根据dist识别
        :return:
        """
        pass

    def clean(self):
        """
        清空构建的缓存
        :return:
        """
        pass

    def build(self, dist: bool = True, build_ext: Optional[bool] = None):
        """
        构建生成发行包

        :param dist:        发行包方式
            - True:     以二进制包形式发布
            - False:    以源码包的方式发布
        :param build_ext:     是否执行编译，设置为None时根据dist识别
        :return:
        """
        pass
