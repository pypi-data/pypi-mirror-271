# -*- coding:utf8 -*-
"""
##执行scale级别转换
"""
from . import cheakConf
from .com.util import timeTool
import numpy as np

class scale:
    def __init__(self, value, conf):

        """
        scale级别操作
        :param value: 变量文件
        :param conf: scale级别配置（清洗前）
        """
        self.value = value
        cheakConf.scaleConf(self.value, conf) ##获取scaleTitle级别配置(清洗后)

    def scale(self):
        ##获取scale坐标范围
        scaleCoordinate = self.value.scaleConf["coordinate"]

        ##判断scale是否存在
        if scaleCoordinate.STATUS:  ##若不存在
            return None

        if self.value.scaleConf["setNull"]:
            self.setNull(scaleCoordinate)
            return None

        ##整个单元格匹配才替换
        self.value.sheetData.iloc[
            scaleCoordinate.start[0] - 1: scaleCoordinate.start[0] + scaleCoordinate.rows - 1,
            scaleCoordinate.start[1] - 1: scaleCoordinate.start[1] + scaleCoordinate.columns - 1
        ].replace(self.value.scaleConf["replaceAll"], inplace=True)

        ##单元格内匹配就替换
        self.value.sheetData.iloc[
            scaleCoordinate.start[0] - 1: scaleCoordinate.start[0] + scaleCoordinate.rows - 1,
            scaleCoordinate.start[1] - 1: scaleCoordinate.start[1] + scaleCoordinate.columns - 1
        ].replace(self.value.scaleConf["replaceSome"], regex=True, inplace=True)

        ##调整日期格式
        if self.value.scaleConf["isDateFormat"]:
            targetFormat = self.value.scaleConf["dateFormat"]["targetFormat"] ##目标格式
            for i in range(scaleCoordinate.start[0] - 1, scaleCoordinate.start[0] + scaleCoordinate.rows - 1):
                for j in range(scaleCoordinate.start[1] - 1, scaleCoordinate.start[1] + scaleCoordinate.columns - 1):
                    date = self.value.sheetData.iloc[i, j]
                    if not isinstance(date, str): date = str(date)
                    self.value.sheetData.iloc[i, j] = self.dateFormat(date, targetFormat)

        ##填充合并单元格
        ##单行填充
        if self.value.scaleConf["fillRows"]:
            self.fillRows(scaleCoordinate)
        ##单列填充
        if self.value.scaleConf["fillColumns"]:
            self.fillColumns(scaleCoordinate)

    def setNull(self, scaleCoordinate):
        """
        设为空值
        """
        self.value.sheetData.iloc[
            scaleCoordinate.start[0] - 1: scaleCoordinate.start[0] + scaleCoordinate.rows - 1,
            scaleCoordinate.start[1] - 1: scaleCoordinate.start[1] + scaleCoordinate.columns - 1
        ] = np.nan

    def fillRows(self, scaleCoordinate):
        """
        单行填充
        """
        for i in range(scaleCoordinate.start[0] - 1, scaleCoordinate.start[0] + scaleCoordinate.rows - 1):
            flag = 0  ##是否处于空值填充范围
            preThis = -1;
            this = -1  ##当前坐标与上一个坐标
            start = -1;
            end = -1  ##开始与结束范围
            value = None
            for j in range(scaleCoordinate.start[1] - 1, scaleCoordinate.start[1] + scaleCoordinate.columns - 1):
                preThis = this;
                this = j
                if flag == 1:  ##若处于空值填充范围
                    if self.value.sheetData.iloc[i, j] == self.value.sheetData.iloc[i, j]:  # 若不是空值
                        end = preThis

                        ##补充操作,替换空值
                        self.value.sheetData.iloc[
                        i,
                        start + 1: end + 1
                        ].fillna(value, inplace=True)

                        start = this
                        value = self.value.sheetData.iloc[i, j]
                        flag = 0
                else:
                    if self.value.sheetData.iloc[i, j] == self.value.sheetData.iloc[i, j]:  # 若不是空值
                        start = this
                        value = self.value.sheetData.iloc[i, j]
                    else:
                        flag = 1

            if flag == 1:
                ##补充操作,替换空值
                y = scaleCoordinate.start[1] + scaleCoordinate.columns - 1
                self.value.sheetData.iloc[i, start+1:y].fillna(value, inplace=True)


    def fillColumns(self, scaleCoordinate):
        """
        单列填充
        """
        for i in range(scaleCoordinate.start[1] - 1, scaleCoordinate.start[1] + scaleCoordinate.columns):
            flag = 0  ##是否处于空值填充范围
            preThis = -1;
            this = -1  ##当前坐标与上一个坐标
            start = -1;
            end = -1  ##开始与结束范围
            value = None
            for j in range(scaleCoordinate.start[0] - 1, scaleCoordinate.start[0] + scaleCoordinate.rows):
                preThis = this;
                this = j
                if flag == 1:  ##若处于空值填充范围
                    if self.value.sheetData.iloc[j, i] == self.value.sheetData.iloc[j, i]:  # 若不是空值
                        end = preThis

                        ##补充操作,替换空值
                        self.value.sheetData.iloc[
                        start: end - 1,
                        i
                        ].fillna(value, inplace=True)

                        flag = 0
                else:
                    if self.value.sheetData.iloc[j, i] == self.value.sheetData.iloc[j, i]:  # 若不是空值
                        start = this
                        value = self.value.sheetData.iloc[j, i]

            if flag == 1:
                ##补充操作,替换空值
                self.value.sheetData[
                start: end - 1,
                i
                ].fillna(value, inplace=True)

    def dateFormat(self, date, targetFormat):
        """
        日期转换
        :param date: 传入数据
        :param targetFormat: 目标格式
        :return:
        """
        ##尝试使用格式转换
        for dateFormat in self.value.scaleConf["dateFormat"]["format"]:
            try:
                date = timeTool.dateToStr(timeTool.strToDate(date, dateFormat), targetFormat)
                return date
            except Exception:
                pass

        ##尝试使用自定义转换器转换
        for dateFormat in self.value.scaleConf["dateFormat"]["dateFormat"]:
            try:
                date = self.value.extraFuncList[dateFormat](date, targetFormat)
                return date
            except Exception as e:
                pass

        if self.value.scaleConf["dateFormat"]["isEmptyWhenFalse"]:
            return ""
        else:
            return date