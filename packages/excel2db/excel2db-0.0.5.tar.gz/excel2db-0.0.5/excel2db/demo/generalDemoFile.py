
demo = {
    "demo1":{
        "file":"""
\"\"\"
快速演示
\"\"\"
from excel2db.excel2db import excel2db

if __name__ == "__main__":
    excelUrl = "./demo1.xlsx"
    ed = excel2db()
    ed.excel2db(excelUrl)
    ed.value.dbConnect.close()
        """,
        "json":"",
        "excel":[
            {
                "sheetName":"st1",
                "data":[
                    ["姓名","性别"],
                    ["张三","男"],
                    ["李四","女"]
                ]
            }
        ]
    },
    "demo2":{
        "file":"""
\"\"\"
无标题文件
\"\"\"
from excel2db.excel2db import excel2db

if __name__ == "__main__":
    excelUrl = "./demo2.xlsx"
    ed = excel2db("./demo2.json")
    ed.excel2db(excelUrl)
    ed.value.dbConnect.close()
        """,
        "json":"""
{
  "sheet" : [
    {
      "sheetID" : 0,
      "titleLines" : 0
    }
  ]
}
        """,
        "excel":[
            {
                "sheetName":"st1",
                "data":[
                    ["张三","男"],
                    ["李四","女"]
                ]
            }
        ]
    },
    "demo3":{
        "file":"""
\"\"\"
明细表示例
\"\"\"
from excel2db.excel2db import excel2db

if __name__ == "__main__":
    excelUrl = "./demo3.xlsx"
    ed = excel2db("./demo3.json")
    ed.excel2db(excelUrl)
    ed.value.dbConnect.close()
        """,
        "json":"""
{
  "sheet" : [
    {
      "sheetID" : 0,
      "isIncludeDetail" : true,
      "detailSplitByColumnID" : "C",
      "detailTitle": {
        "detailTitleName":[
          "科目"
        ]
      }
    }
  ]
}
        """,
        "excel":[
            {
                "sheetName":"st1",
                "data":[
                    ["姓名","性别","语文","数学","英语"],
                    ["张三","男",56,67,76],
                    ["李四","女",45,34,54]
                ]
            }
        ]
    },
    "demo4":{
        "file":"""
\"\"\"
多sheet演示
\"\"\"
from excel2db.excel2db import excel2db

if __name__ == "__main__":
    excelUrl = "./demo4.xlsx"
    ed = excel2db()
    ed.excel2db(excelUrl)
        """,
        "json":"""
        """,
        "excel":[
            {
                "sheetName":"st1",
                "data":[
                    ["姓名","性别"],
                    ["张三","男"],
                    ["李四","女"]
                ]
            },
            {
                "sheetName": "st2",
                "data": [
                    ["课程", "分数"],
                    ["语文", 34],
                    ["数学", 43]
                ]
            }
        ]
    },
    "demo5":{
        "file":"""
\"\"\"
多sheet演示(2)
\"\"\"
from excel2db.excel2db import excel2db

if __name__ == "__main__":
    excelUrl = "./demo5.xlsx"
    ed = excel2db("./demo5.json")
    ed.excel2db(excelUrl)
    ed.value.dbConnect.close()
        """,
        "json":"""
{
  "readAllSheet" : false,
  "sheet" : [
    {
      "sheetID" : 0
    },
    {
      "sheetName" : "st2"
    },
    {
      "sheetID" : -1
    }
  ]
}
        """,
        "excel":[
            {
                "sheetName":"st1",
                "data":[
                    ["姓名","性别"],
                    ["张三","男"],
                    ["李四","女"]
                ]
            },
            {
                "sheetName": "st2",
                "data": [
                    ["课程", "分数"],
                    ["语文", 34],
                    ["数学", 43]
                ]
            },
            {
                "sheetName": "st3",
                "data": [
                    ["课程", "分数"],
                    ["语文", 34],
                    ["数学", 43]
                ]
            },
            {
                "sheetName": "st4",
                "data": [
                    ["课程", "分数"],
                    ["语文", 34],
                    ["数学", 43]
                ]
            }
        ]
    },
    "demo6":{
        "file":"""
\"\"\"
读取字段配置演示
\"\"\"
from excel2db.excel2db import excel2db

if __name__ == "__main__":
    excelUrl = "./demo6.xlsx"
    ed = excel2db("./demo6.json")
    ed.excel2db(excelUrl)
    ed.value.dbConnect.close()
        """,
        "json":"""
{
  "datLoad" : "./test.db",
  "sheet" : [
    {
      "sheetID" : 0,
      "mainTitle": {
        "readAllTitle": false,
        "titleList" : [
          {
            "titleName" : "性别",
            "columnName": "sex"
          },{
            "titleIndex" : 0,
            "columnName": "name"
          },{
            "titleLetter": "C",
            "columnName": "age"
          }
        ]
      }
    }
  ]
}
        """,
        "excel":[
            {
                "sheetName":"st1",
                "data":[
                    ["姓名","性别","年龄","爱好"],
                    ["张三","男",23,"篮球"],
                    ["李四","女",21,"足球"]
                ]
            }
        ]
    },
    "demo7":{
        "file":"""
\"\"\"
获取数据演示
\"\"\"
from excel2db.excel2db import excel2db
from excel2db.com.util import dbconnect

if __name__ == "__main__":
    excelUrl = "./demo7.xlsx"
    ed = excel2db()
    ed.excel2db(excelUrl)

    ##获取列表
    print("获取列表")
    sql = 'SELECT id, "姓名" AS name, "性别" AS sex, "年龄" AS age FROM "st1"'
    ed.value.dbConnect.cursor.execute(sql)
    for row in ed.value.dbConnect.cursor.fetchall():
        print(row)

    selectData = dbconnect.selectData(ed.value.dbConnect, sql)
    print("获取字段名")
    print(selectData.columns)
    print("获取列表")
    for row in selectData.dataByRow:
        print(row.toLis())
    print("获取字典")
    for row in selectData.dataByRow:
        print(row.toDic())

    ed.value.dbConnect.close()
        """,
        "json":"""
        """,
        "excel":[
            {
                "sheetName":"st1",
                "data":[
                    ["姓名","性别","年龄","爱好"],
                    ["张三","男",23,"篮球"],
                    ["李四","女",21,"足球"]
                ]
            }
        ]
    },
}

from excel2db.com.util import fileTool
import openpyxl
filetool = fileTool.fileTool()

def generalDemoFile():
    for demoName in demo:
        filetool.createDir("./" + demoName, mode=1)
        filetool.writeOverFile("./" + demoName + "/__init__.py", "")
        filetool.writeOverFile("./" + demoName + "/" + demoName + ".py", demo[demoName]["file"])
        filetool.writeOverFile("./" + demoName + "/" + demoName + ".json", demo[demoName]["json"])

        # 生成一个 Workbook 的实例化对象，wb即代表一个工作簿（一个 Excel 文件）
        wb = openpyxl.Workbook()
        index = 1
        for sheet in demo[demoName]["excel"]:
            if index==1:
                ws=wb.active
                ws.title = sheet["sheetName"]
            else:
                wb.create_sheet(sheet["sheetName"])
                ws = wb[sheet["sheetName"]]

            index += 1

            for row in sheet["data"]:
                ws.append(row)

        wb.save("./" + demoName + "/" + demoName + ".xlsx")

if __name__ == "__main__":
    generalDemoFile()