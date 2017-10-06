import sqlite3
import os
import xlrd

class Sqlop():
    """对数据库进行操作的类
    """
    def __init__(self,path):
        self.connectdb(path)

    def connectdb(self,path):
        self.conn=sqlite3.connect(path)
        self.cursor=self.conn.cursor()
    def closedb(self):
        self.cursor.close()
        self.conn.close()

    def insert(self,datetime, pm2_5, pm10, humidity,tempture,height):
        self.cursor.execute("""insert into weather  values ("%s",%f,%f,%f,%f,%f);"""%(datetime,pm2_5,pm10,humidity,tempture,height))
        self.conn.commit()

    def select(self,starttime,stoptime,column):
        colstr=""
        for col in column:
            colstr+='\"'+col+'\"'+','
        colstr = colstr[:-1]
        searchstr="select %s from weather where \"时间\">=\"%s\" and \"时间\"<=\"%s\" order by \"时间\" desc" %(colstr,starttime,stoptime)
        #print(searchstr)
        self.cursor.execute(searchstr)

        #for row in self.cursor.fetchall():
        #    print(row)
        return self.cursor.fetchall()


#该程序用于读取电子表格数据并将数据输入数据库
def loadexcel():
    workbook = xlrd.open_workbook(u'data2015-2017.xlsx')#读取文件
    sheet_names= workbook.sheet_names()#获取表名称
    sheet2 = workbook.sheet_by_name(sheet_names[0])#选择表格
    rows=sheet2.nrows#获取行数
    db_history=sqlop("weather_history.db")
    for i in range(1,rows):
        rowvalue= sheet2.row_values(i)#获取该行数据
        db_history.insert("null",rowvalue[0],rowvalue[1],rowvalue[2],rowvalue[3],rowvalue[4])


if __name__=="__main__":
    dbop=Sqlop("weather.db")
    starttime="2017-10-01 10:00:00"
    stoptime="2017-10-01 10:25:00"
    column=["时间","PM2.5","PM10"]
    dbop.select(starttime,stoptime,column)
    #loadexcel()
