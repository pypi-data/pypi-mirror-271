# -*- coding:utf8 -*-
"""
用于excel转sqlite数据库
注意：
依据变量修改配置文件，应在cheakConf中进行
依据配置文件修改变量，应在配置文件完全生成后进行
"""
from . import value, cheakConf, excel

class excel2db:

    def __init__(self, *configFileUrl):
        """
        :param *configFileUrl: 配置文件路径
        """
        self.value = value.value() ##生成变量文件
        self.value.rawConf = cheakConf.combinExcelConf(*configFileUrl) ##生成配置文件

    def excel2db(self, excelUrl):
        ##执行excel级别转换
        excelManager = excel.excel(self.value, self.value.rawConf)
        excelManager.excel(excelUrl)

    def setDateFormatFunc(self, *dateFormat):
        """
        设置日期格式化方法
        """
        for func in dateFormat:
            self.value.dateFormatFunc[func.__name__] = func