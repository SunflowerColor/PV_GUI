from PyQt5 import QtWidgets,QtGui,QtCore
import sys
import random
import matplotlib
import datasql
from imp import reload
reload(datasql)
matplotlib.use("Qt5Agg")#声明使用Qt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

app=QtWidgets.QApplication(sys.argv)

class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("光伏发电功率预测")

        #创建曲线绘制页面
        plot_widget = QtWidgets.QWidget(self)
        plot_layout=QtWidgets.QGridLayout(plot_widget)
        plot_cavas = PlotCanvas(width=7, height=5, dpi=100)
        plot_layout.addWidget(plot_cavas)

        sql_widget=datatable(self)

        #标签页设置
        self.main_tabwidget = QtWidgets.QTabWidget()
        self.main_tabwidget.addTab(plot_widget,"曲线")
        self.main_tabwidget.addTab(sql_widget,"数据库")
        self.setCentralWidget(self.main_tabwidget)

        self.show()




class PlotCanvas(FigureCanvas):
    """
    该类继承matplotlib中的FigureCanvas类，使得该类既是个PyQt5的Qwidget，
    又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
    """
    def __init__(self, parent=None,width=5, height=4, dpi=100):
        fig=Figure(figsize=(width,height),dpi=dpi)
        self.axes = fig.add_subplot(111)# 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        FigureCanvas.__init__(self,fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.test()

    def test(self):
        self.init_plot()
        #每秒更新一次图像
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def init_plot(self):
        x=[1,2,3,4,5,6,7,8,9]
        y=[23,21,32,13,3,132,13,3,1]
        self.axes.plot(x, y)

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(10)]
        self.axes.cla()
        self.axes.plot(range(0,10), l)
        self.draw()

class datatable(QtWidgets.QWidget):
    def __init__(self,parent_widget):
        super(datatable,self).__init__(parent_widget)
        #创建数据库显示页面
        self.layout=QtWidgets.QGridLayout(self)
        self.table=QtWidgets.QTableView()
        #设置表格数据模式
        self.model=QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderItem(0,QtGui.QStandardItem("时间"))
        self.model.setHorizontalHeaderItem(1,QtGui.QStandardItem("PM2.5"))
        self.model.setHorizontalHeaderItem(2,QtGui.QStandardItem("PM10"))
        self.model.setHorizontalHeaderItem(3,QtGui.QStandardItem("湿度"))
        self.model.setHorizontalHeaderItem(4,QtGui.QStandardItem("气温"))
        self.model.setHorizontalHeaderItem(5,QtGui.QStandardItem("边界层高度"))

        self.table.setModel(self.model)#连接表格与数据

        self.searchbutton=QtWidgets.QPushButton('查询')
        self.searchbutton.clicked.connect(self.search)

        #设置时间日期列表
        self.firsttime=QtWidgets.QDateTimeEdit()
        self.firsttime.setDisplayFormat("yyyy-MM-dd hh:mm")#设置显示格式
        self.firsttime.setDateTime(QtCore.QDateTime.currentDateTime().addDays(-1))#设置时间为当前系统时间的前一天
        self.firsttime.setCalendarPopup(True)#设置使用日历的界面来选时间
        self.secondtime=QtWidgets.QDateTimeEdit()
        self.secondtime.setDisplayFormat("yyyy-MM-dd hh:mm")
        self.secondtime.setDateTime(QtCore.QDateTime.currentDateTime())
        self.secondtime.setCalendarPopup(True)

        self.layout.addWidget(self.table,3,0)
        self.layout.addWidget(self.firsttime,0,0)
        self.layout.addWidget(self.secondtime,1,0)
        self.layout.addWidget(self.searchbutton,2,0)

    def insertrow(self,rowdate):
        #rowdate = ("2017-10-01 10:20:10",10, 20, 30, 40, 50)
        qtrowdate=[]
        for date in rowdate :
            qtrowdate.append(QtGui.QStandardItem(str(date)))
        self.model.appendRow(qtrowdate)
    def search(self):
        starttime=self.firsttime.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        stoptime=self.secondtime.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        #starttime = "2017-10-01 10:00:00"
        #stoptime = "2017-10-01 10:25:00"
        column = ["时间", "PM2.5", "PM10","湿度","气温","边界层高度"]
        sear_date=dbserver.select(starttime,stoptime,column)
        print(sear_date)
        for date in sear_date:
            self.insertrow(date)



dbserver=datasql.Sqlop("weather.db")
mainwindow=Mainwindow()

sys.exit(app.exec_())