#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_module_finder.py
@Author     ：Alex
@Date       ：2024/3/8 0:04 
@Function   ：模块搜索器
"""
import os
from typing import Union, Iterable, Set, Dict
_Path = Union[str, os.PathLike]


class ModuleFinder:

    def __init__(self, where: _Path = '.', exclude: Union[str, Iterable[str]] = (), include: Iterable[str] = ('*',), namespace: bool = False):
        """
        初始化
        :param where:
        :param exclude:
        :param include:
        :param namespace:
        """
        pass

    def packages(self) -> Set[str]:
        """
        获取包集合
        :return:
        """
        pass

    def dirMaps(self) -> Dict[str, str]:
        """
        获取目录映射
        :return:
        """
        pass



