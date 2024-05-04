# -*- coding:utf8 -*-
"""
##执行excel级别转换
"""
import os, xlrd
from pandas import read_excel
from openpyxl import load_workbook
from . import cheakConf, sheet, insert2sqlite

class excel:
    def __init__(self, value, conf):

        """
        excel级别操作
        :param value: 变量文件
        :param conf: excel级别配置（清洗前）
        :param excelUrl: excel文件路径
        """
        self.value = value
        cheakConf.excelConf(self.value, conf) ##获取excel级别配置(清洗后)

    def excel(self, excelUrl):
        ##获取excel文件名
        (path, fileName) = os.path.split(excelUrl)
        (name, suffix) = os.path.splitext(fileName)
        self.value.excelFileName = name

        ##打开excel文件
        if self.value.excelConf["notReadHideSheet"] == True:
            if suffix == '.xls':
                sheetName = self.read_visible_sheets_xls(excelUrl)
            elif suffix == '.xlsx':
                sheetName = self.read_visible_sheets_xlsx(excelUrl)
            else:
                raise Exception("文件类型错误")
        else:
            sheetName = None

        df = read_excel(
            io=excelUrl,
            sheet_name=sheetName,
            header=None
        )

        self.value.sheetList = list(df.keys())
        self.value.excelData = df

        self.value.dbClass = insert2sqlite.insert2sqlite(self.value)

        sheetConf = cheakConf.combinSheetConf(self.value) ##sheet级别配置文件合并

        for conf in sheetConf:
            sheetManager = sheet.sheet(self.value, conf)
            sheetManager.sheet()

    def read_visible_sheets_xls(self, filename):
        # 打开 Excel 文件
        book = xlrd.open_workbook(filename)

        # 获取所有工作表的名称
        all_sheet_names = book.sheet_names()

        # 过滤出未隐藏的工作表名称
        visible_sheet_names = [name for name in all_sheet_names if book.sheet_by_name(name).visibility == 0]

        return visible_sheet_names

    def read_visible_sheets_xlsx(self, filename):
        # 使用 openpyxl 加载 Excel 文件
        wb = load_workbook(filename, read_only=True)

        # 获取所有工作表的名称
        all_sheet_names = wb.sheetnames

        # 过滤出未隐藏的工作表名称
        visible_sheet_names = [name for name in all_sheet_names if not wb[name].sheet_state == 'hidden']

        return visible_sheet_names