#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：build2_exe.py
@Author     ：Alex
@Date       ：2024/3/5 17:01 
@Function   ：构建生成可执行程序
"""
from typing import Union, Optional, List, Set, Tuple
from pathlib import Path
from os import PathLike


class Build2EXE:

    def __init__(self,
                 entry: Union[str, Path, PathLike],
                 name: Optional[str] = None,
                 modules_list: Union[str, Path, List[str], List[Path], Tuple[str], Tuple[Path], Set[str], Set[Path]] = None,
                 excludes_list: Union[str, Path, List[str], List[Path], Tuple[str], Tuple[Path], Set[str], Set[Path]] = None,
                 onefile: bool = False,
                 console: bool = True,
                 key: Union[str, bool] = None,
                 frozen: bool = True):
        """
        初始化

        :param entry:       程序入口script文件名
        :param name:        指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字
        :param Union[str, Path, List[str], List[Path]] modules_list:         项目需要包含的模块入口
        :param Union[str, Path, List[str], List[Path]] excludes_list:          需要排除的module，可以是文件
        :param onefile:     是否产生单个可执行文件或目录（包含多个文件）
        :param console:     指定使用命令行窗口运行程序（仅对 Windows 有效）
        :param key:         代码加密密钥，Ture自动生成随机密码，空值不加密
        :param frozen:      是否冻结.env和config配置，默认True
        """
        pass

    def icon(self, icon: Union[str, Path, PathLike]):
        """
        设置图标文件
        :param icon:
        :return:
        """
        return self

    def data(self, data: dict):
        """
        打包额外资源

        :param dict data:   打包额外资源，key源目录，val为目标目录
        :return:
        """
        return self

    def binary(self, binary: dict):
        """
        打包额外的代码，与–add-data不同的是，用binary添加的文件，pyi会分析它引用的文件并把它们一同添加进来

        :param dict binary:
        :return:
        """
        return self

    def exclude(self, exclude: Union[str, list, tuple, set]):
        """
        添加需要排除的包名

        :param exclude: Union[str, list, tuple, set] exclude:       需要排序的模块名称（非文件路径）
        :return:
        """
        return self

    def hidden(self, hidden: Union[str, list, tuple, set]):
        """
        设置–hidden-import

        :param Union[str, list, tuple, set] hidden:
        :return:
        """
        return self

    def upx(self, upx: Union[str, Path, bool] = True):
        """
        upx设置

        :param Union[str, Path, bool] upx:  True尽量使用upx，False强制不使用，字符串或路径时指定upx目录
        :return:
        """
        return self

    def frozen(self, frozen: bool = True):
        """
        冻结环境变量及配置

        :param frozen:      是否冻结.env和config配置，默认True
        :return:
        """
        return self

    def run(self, force: bool = True, compiled: bool = True, autoClean: bool = True):
        """
        运行打包构建

        :param bool force:      如果dist文件夹内已经存在生成文件，则不询问用户，直接覆盖
        :param bool compiled:   项目是否需要使用Cython进行编译
        :param bool autoClean:  构建完成后，是否自动清空临时文件
        :return:
        """
        pass

    def clean(self, force: bool = False):
        """
        清空打包构建生成的文件

        :param force:   删除已存在的dist包
        :return:
        """
        pass
