# -*- coding:utf8 -*-

"""
额外方法定义
"""



"""
日期格式编辑器
定义方法，需设置两个参数：date(传入数据),targetFormat(目标格式), 并且返回处理后的数据
"""
from .com.util import timeTool

def dateFormat_1(date, targetFormat):
    print(date)
    baseDate = "2023-08-01"  ##基准日期
    baseNum = 45139  ##基准数字
    number = int(float(date))
    date = timeTool.changeTime(baseDate, "days", number - baseNum, targetFormat)
    print(date)

    return date

def dateFormat_2(date, targetFormat):
    """
    未知年份处理
    """
    now = timeTool.getNow()
    nowDate = now[:10]
    nowYear = now[:4]

    ##生成时间
    date = nowYear + "/" + date
    date = timeTool.dateToStr(timeTool.strToDate(date, "%Y/%m/%d"), targetFormat)

    ##获取当前日期向后六个月的日期
    maxDate = timeTool.changeTime(nowDate, "days", 180)
    if timeTool.cmp_date(date, maxDate) == -1:  # 若比最大日期小
       return date

    nowYear = str(int(nowYear)-1)

    ##生成时间
    date = nowYear + "/" + date
    date = timeTool.dateToStr(timeTool.strToDate(date, "%Y/%m/%d"), targetFormat)

    return date

def dateFormat_3(date, targetFormat):
    """
    三进未知年份处理
    """
    now = timeTool.getNow()
    nowDate = now[:10]
    nowYear = now[:4]

    if isinstance(date, str):
        if len(date) > 0:
            if date[0] == '"':
                date = date[1:]

    ##生成时间
    date = nowYear + "/" + date
    date = timeTool.dateToStr(timeTool.strToDate(date, "%Y/%m/%d"), targetFormat)

    ##获取当前日期向后六个月的日期
    maxDate = timeTool.changeTime(nowDate, "days", 180)
    if timeTool.cmp_date(date, maxDate) == -1:  # 若比最大日期小
       return date

    nowYear = str(int(nowYear)-1)

    ##生成时间
    date = nowYear + "/" + date
    date = timeTool.dateToStr(timeTool.strToDate(date, "%Y/%m/%d"), targetFormat)

    return date
