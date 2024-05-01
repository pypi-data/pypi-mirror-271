#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：build2_ext.py
@Author     ：Alex
@Date       ：2024/4/27 20:33 
@Function   ：编译项目代码
"""
from typing import Union, List, Set, Tuple
from pathlib import Path


class Build2EXT:

    def __init__(self,
                 modules: Union[str, Path, List[str], List[Path], Set[str], Set[Path], Tuple[str], Tuple[Path]],
                 excludes: Union[str, Path, List[str], List[Path], Set[str], Set[Path], Tuple[str], Tuple[Path], None] = None,
                 pre_install_optimize: bool = False,
                 build_dir: Union[str, Path] = 'build',
                 out_dir: Union[str, Path] = None):
        """
        初始化方法

        :param modules:                     指定模块列表，可以模块名或文件名
        :param excludes:                    需要排除的模块
        :param pre_install_optimize:        安装打包编译优化
        :param build_dir:                   c代码生成构建目录，默认build
        :param out_dir:                     生成到输出到当前目录，默认None为当前相同目录(inplace=True)
        """
        pass

    def findModuleFiles(self) -> Set[Path]:
        """
        收集模块或包的所有文件
        :return:
        """
        pass

    def clean(self):
        """
        清空编译，包括c、pyd文件
        :return:
        """
        pass

    def run(self, force: bool = True):
        """
        运行编译
        编译生成pyd、so扩展

        :param force: 是否自动清空已生成的文件
        :return:
        """
        pass

