#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_pkg.py
@Author     ：Alex
@Date       ：2024/3/11 16:09 
@Function   ：Pkg包管理套件
"""
from typing import Union, Tuple, Optional, Iterable, List
from os import PathLike
from pathlib import Path
import contextlib



class PkgUtil:

    @contextlib.contextmanager
    def keep_sys_modules_clean(self):
        pass

    @staticmethod
    def getProjectRoot(project_root=None) -> Path:
        """
        获取项目根目录
        :param project_root:
        :return:
        """
        pass

    @classmethod
    def getPackagePath(cls, package, project_root=None) -> Optional[Path]:
        """
        获取包或模块的绝对路径

        TODO：当前只支持用户自定义包

        :param package:
                    - 包名（获取包所在目录）
                    - 模块名（自动转换为.py文件路径）
                    - 文件或目录
        :param project_root:
        :return:
        """
        pass

    @classmethod
    def findPackageModuleFiles(cls,
                               package,
                               exclude: Union[str, Iterable[str]] = (),
                               recursive: bool = True, project_root=None) -> List[Path]:
        """
        获取包的模块文件

        TODO：当前只支持用户自定义包

        :param package:     包名
                    - 包名（获取包所在目录）
                    - 模块名（自动转换为.py文件路径）
                    - 文件或目录
        :param exclude:     排除
        :param recursive:   递归
        :param project_root:        指定项目根目录，默认为
        :return:
        """
        pass

    @staticmethod
    def importFrom(pkg: str):
        """
        通过字符串导入模块
        :param str pkg:       包名
        :return:
        """
        pass

    @classmethod
    def findPackages(cls, where: Union[str, PathLike] = '.', exclude: Union[str, Iterable[str]] = (),
                     include: Iterable[str] = ('*',), namespace: bool = False,
                     project_root: Optional[Union[str, Path, PathLike]] = None) -> List[str]:
        """
        搜索包
        :param where:
        :param exclude:
        :param include:
        :param namespace:
        :param project_root:        项目根路径，默认为Env.PROJECT_PATH
        :return:
        """
        pass

    @classmethod
    def parseFileImports(
            cls,
            fpath: Union[str, Path, PathLike],
            visit_doc_str: bool = False,
            parse_requirement_annotations: bool = False) -> Tuple[List, List]:
        """
        分析文件的import项
        :param fpath:       支持.py或.ipynb类型文件
        :param bool visit_doc_str:
        :param bool parse_requirement_annotations:
        :return:
        """
        pass

    @classmethod
    def searchDistributions(cls,
                            names: Union[str, Iterable[str]],
                            index_url: str = 'https://pypi.org/simple/',
                            include_prereleases: bool = False
        ) -> List[dict]:
        """
        搜索发行的包

        :param names:               Search packages/distributions by the top level import/module names
        :param str index_url:       Base URL of the Python Package Index, this should point to a repository compliant with PEP 503 (the simple repository API)
        :param bool include_prereleases:         Include pre-release and development versions.
        :return:
        """
        pass

    @classmethod
    def isUserModule(cls, module, project_root: Optional[Union[PathLike, Path, str]] = None) -> bool:
        """
        是否自定义模块

        :param module:     模块
        :param project_root:     项目工程根目录
        :return:
        """
        pass

    @classmethod
    def checkStdLib(cls, name: str) -> Tuple[bool, str]:
        """
        检查是否标准模块
        :param name:
        :return Tuple[bool, str]:     结果：（是否标准模块，模块路径）
        """
        pass

    @classmethod
    def dumpRequirements(cls, modules=None, project_root=None):
        """
        提取modules依赖
        :param modules:
            - 本地模块、包名列表
            - 文件目录清单
        :param project_root:        工程根目录
        :return:
        """
        pass










