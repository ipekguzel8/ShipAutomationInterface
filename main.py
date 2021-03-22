from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys
import serial
import datetime
import socket
import sqlite3
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtGui import QPolygon
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
import vtk
from analoggaugewidget import AnalogGaugeWidget
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
ser = serial.Serial(bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
now = QDate.currentDate ()
time = QTime.currentTime()
class Pencere(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vt = sqlite3.connect('C:/Users/ipekg/Desktop/test.sqlite')
        im = vt.cursor()
        im.execute("CREATE TABLE IF NOT EXISTS adres_defteri (HIZ, PRUVA, DURUM)")#tablo varsa tekrar oluşturmayacak       
        #im.execute("""SELECT * FROM faturalar""")
        #veriler = im.fetchall()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((socket.gethostbyname(socket.gethostname()), 53201))  
        sock.listen(2)
        uruntarih=datetime.datetime.now()
        print(str(uruntarih.strftime("%Y-%m-%d %H:%M:%S")))
        self.setGeometry(0, 30, 1920, 1010)
        self.setStyleSheet("background-color: #004C99;") 
        self.groupbox = QGroupBox(self)
        self.groupbox.setGeometry(150, 50, 1000, 200)
        self.groupbox.setStyleSheet("background: #004C99;")
        self.groupbox2 = QGroupBox(self)
        self.groupbox2.setGeometry(1250, 50, 500, 200)
        self.groupbox2.setStyleSheet("background: #004C99;")
        self.port=QLabel("Port:",self.groupbox)
        self.port.move(30, 50)
        self.port.setStyleSheet("font:bold 15px; ")
        self.port.setFixedWidth(55)
        self.portsecimi=QComboBox(self.groupbox)
        self.portn=list()
        self.portn.append(str(sock.getsockname()[1]))
        self.ports=socket.gethostname()[1]
        print(str(socket.gethostbyname(socket.gethostname())))
        #self.portsecimi.addItems(self.portn)
        #self.portsecimi.addItems(self.portn)
        self.portsecimi.addItems(self.portlar())
        #print(type(sock.getsockname()[1]))
        print(type(self.portlar()))   
        #self.portsecimi.addItems(self.portn)
        self.portsecimi.setFixedWidth(100)
        self.portsecimi.setStyleSheet("background: #fff; font:15px; ")
        self.portsecimi.move(80, 50)
        self.baudrate=QLabel("Baudrate:",self.groupbox)
        self.baudrate.setStyleSheet("font:bold 15px; border:2px")
        self.baudrate.setFixedWidth(85)
        self.baudrate.move(290, 50)
        self.baudratesecimi=QComboBox(self.groupbox)
        self.baudratesecimi.addItems(["","9600","19200", "38400","115200"])
        self.baudratesecimi.setStyleSheet("background: #fff; font:15px; ")
        self.baudratesecimi.setFixedWidth(100)
        self.baudratesecimi.move(370, 50)
        self.updaterate=QLabel("Update Rate:",self.groupbox)
        self.updaterate.setFixedWidth(100)
        self.updaterate.setStyleSheet("font:bold 15px; border:2px")
        self.updaterate.move(590, 50)
        self.updateratesecimi=QComboBox(self.groupbox)
        self.updateratesecimi.addItems(["","30Hz","60Hz", "75Hz","85Hz","144Hz"])
        self.updateratesecimi.setStyleSheet("background: #fff; font:15px; ")
        self.updateratesecimi.setFixedWidth(85)
        self.updateratesecimi.move(690, 50)
        self.basla=QPushButton("START",self.groupbox)
        self.basla.clicked.connect(self.start)
        self.basla.move(30, 100)
        self.dur=QPushButton("STOP",self.groupbox)
        self.dur.move(300, 100)
        self.dur.clicked.connect(self.stop)
        self.yenidenb=QPushButton("RESTART",self.groupbox)
        self.yenidenb.move(600, 100)
        self.basla.setStyleSheet("background: #ccc; font:15px;")
        self.dur.setStyleSheet("background: #ccc; font:15px;")
        self.yenidenb.setStyleSheet("background: #ccc; font:15px;")
        self.led1=QPushButton(self.groupbox2)
        self.led1.setGeometry(30, 10, 30, 30) 
        self.led1.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi1=QLabel("Kapı 1",self.groupbox2)
        self.kapi1.move(70, 15)
        self.kapi1.setStyleSheet("font:bold 15px; ")
        self.kapi1.setFixedWidth(45)
        self.led2=QPushButton(self.groupbox2)
        self.led2.setGeometry(30, 60, 30, 30) 
        self.led2.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi2=QLabel("Kapı 2",self.groupbox2)
        self.kapi2.move(70, 65)
        self.kapi2.setStyleSheet("font:bold 15px; ")
        self.kapi2.setFixedWidth(45)
        self.led3=QPushButton(self.groupbox2)
        self.led3.setGeometry(30, 110, 30, 30) 
        self.led3.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi3=QLabel("Kapı 3",self.groupbox2)
        self.kapi3.move(70, 115)
        self.kapi3.setStyleSheet("font:bold 15px; ")
        self.kapi3.setFixedWidth(45)
        self.led4=QPushButton(self.groupbox2)
        self.led4.setGeometry(30, 160, 30, 30) 
        self.led4.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi4=QLabel("Yangın Alarmı",self.groupbox2)
        self.kapi4.move(70, 165)
        self.kapi4.setStyleSheet("font:bold 15px; ")
        self.kapi4.setFixedWidth(90)
        self.led5=QPushButton(self.groupbox2)
        self.led5.setGeometry(250, 10, 30, 30) 
        self.led5.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi5=QLabel("Motor Uyarısı",self.groupbox2)
        self.kapi5.move(290, 15)
        self.kapi5.setStyleSheet("font:bold 15px; ")
        self.kapi5.setFixedWidth(90)
        self.led6=QPushButton(self.groupbox2)
        self.led6.setGeometry(250, 60, 30, 30) 
        self.led6.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi6=QLabel("Sintine Uyarısı",self.groupbox2)
        self.kapi6.move(290, 65)
        self.kapi6.setStyleSheet("font:bold 15px; ")
        self.kapi6.setFixedWidth(90)
        self.led7=QPushButton(self.groupbox2)
        self.led7.setGeometry(250, 110, 30, 30) 
        self.led7.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi7=QLabel("Temiz Su Uyarısı",self.groupbox2)
        self.kapi7.move(290, 115)
        self.kapi7.setStyleSheet("font:bold 15px; ")
        self.kapi7.setFixedWidth(140)
        self.led8=QPushButton(self.groupbox2)
        self.led8.setGeometry(250, 160, 30, 30) 
        self.led8.setStyleSheet("background: #fff; border-radius: 15; border : 2px solid black;")
        self.kapi8=QLabel("Yakıt Uyarısı",self.groupbox2)
        self.kapi8.move(290, 165)
        self.kapi8.setStyleSheet("font:bold 15px; ")
        self.kapi8.setFixedWidth(140)
        self.groupbox3=QGroupBox(self)
        self.groupbox3.setGeometry(150, 300, 1000, 670)
        self.groupbox3.setStyleSheet("background: #004C99;") 
        
        self.tarih=QLabel(self.groupbox3)
        self.tarih.setText(now.toString(Qt.ISODate))
        self.tarih.move(900, 10)
        self.tarih.setStyleSheet("font:bold 15px")
        self.tarih1=QLineEdit('Gün/Ay/Yıl',self.groupbox3)
        self.tarih1.setGeometry(10,10,80,25)
        self.tarih1.setFixedWidth(100)
        self.tarih1.setStyleSheet("color: gray; background: #fff;")  
        self.tarih1.setReadOnly(True)
        self.tarihsec1=QPushButton("...",self.groupbox3)
        self.tarihsec1.move(120,10)
        self.tarihsec1.setStyleSheet("background: #ccc; font:15px;")
        self.tarihsec1.clicked.connect(self.tarih1sec)
        
        self.saat=QLabel(self.groupbox3)
        self.saat.move(900,50)
        self.saat.setText(time.toString(Qt.DefaultLocaleLongDate))
        self.saat.setStyleSheet("font:bold 15px")
        self.timeedit = QTimeEdit(self.groupbox3)
        self.timeedit.setFont(QFont("Sanserif", 12))
        self.timeedit.move(209, 11)
        self.timeedit.setFixedWidth(80)
        self.timeedit.setStyleSheet("background: #fff;")
        self.timeedit2 = QTimeEdit(self.groupbox3)
        self.timeedit2.setFont(QFont("Sanserif", 12))
        self.timeedit2.move(209, 48)
        self.timeedit2.setFixedWidth(80)
        self.timeedit2.setStyleSheet("background: #fff;")
        self.tarih2=QLineEdit('Gün/Ay/Yıl',self.groupbox3)
        self.tarih2.setGeometry(10,45,80,25)
        self.tarih2.setFixedWidth(100)
        self.tarih2.setStyleSheet("color: gray; background: #fff;")  
        self.tarih2.setReadOnly(True)
        self.tarihsec2=QPushButton("...",self.groupbox3)
        self.tarihsec2.move(120,45)
        self.tarihsec2.setStyleSheet("background: #ccc; font:15px;")
        self.tarihsec2.clicked.connect(self.tarih2sec)
        self.tarihsec2.setDisabled(True)
        self.test2=QPushButton("Verileri Listele",self.groupbox3)
        self.test2.move(310,22)
        self.test2.setStyleSheet("z-index: 5; background: #ccc; font:15px;")
        self.sp=QSplitter()
        self.tableWidget2=QTableWidget()
        self.tableWidget2.setStyleSheet("QHeaderView::section { background-color:#fff }")
        self.tableWidget2.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget2.setColumnCount(11)   
        self.tableWidget2.setHorizontalHeaderLabels(str("ZAMAN;HIZ;YÖN;KAPI 1;KAPI 2;KAPI 3;YANGIN ALARMI;MOTOR UYARISI;SİNTİNE UYARISI;TEMİZ SU UYARISI;YAKIT UYARISI").split(";"))
        self.tableWidget2.verticalHeader().hide()
        self.tableWidget2.horizontalHeader().setStyleSheet("font: bold 12px;")
        self.tableWidget2.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableWidget2.horizontalScrollBar().hide()
        self.tableWidget2.setColumnWidth(0,110)
        self.tableWidget2.setColumnWidth(1,55)
        self.tableWidget2.setColumnWidth(2,56)
        self.tableWidget2.setColumnWidth(3,55)
        self.tableWidget2.setColumnWidth(4,55)
        self.tableWidget2.setColumnWidth(5,55)
        self.tableWidget2.setColumnWidth(6,105)
        self.tableWidget2.setColumnWidth(7,115)
        self.tableWidget2.setColumnWidth(8,115)
        self.tableWidget2.setColumnWidth(9,140)
        self.tableWidget2.setColumnWidth(10,110)
        self.tableWidget2.setStyleSheet(" background: #fff;")
        self.sekmeler=QTabWidget(self.groupbox3)
        self.sekmeler.addTab(self.tableWidget2, "VERİLER")
        self.sekmeler.setGeometry(10,90,980,570)
        self.sekmeler.setStyleSheet("z-index: 5; background: #fff;")
        self.groupbox4=QGroupBox(self)
        self.groupbox4.setStyleSheet("background: #004C99;")   
        self.groupbox4.setGeometry(1250, 300, 300, 320)
        filename = "arrow.STL"
        self.frames =QFrame(self.groupbox4)
        self.vl =QVBoxLayout()
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName(filename)
        self.coneMapper2 = vtk.vtkPolyDataMapper()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frames)
        self.vl.addWidget(self.vtkWidget)
        self.iren =self.vtkWidget.GetRenderWindow().GetInteractor()
        self.ren = vtk.vtkRenderer()
        self.prev=0
        WIDTH=260
        HEIGHT=260       
        self.frames.setFixedWidth(260)
        self.frames.setFixedHeight(260)
        self.transform = vtk.vtkTransform()
        self.transform.RotateX(-90)
        self.transform.RotateY(0)
        self.transform.RotateZ(0)
        self.transformFilter=vtk.vtkTransformPolyDataFilter()
        self.transformFilter.SetTransform(self.transform)
        self.transformFilter.SetInputConnection(self.reader.GetOutputPort())
        self.transformFilter.Update()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.coneMapper2.SetInput(self.transformFilter.GetOutput())
        else:
            self.coneMapper2.SetInputConnection(self.transformFilter.GetOutputPort())
        self.actor2 = vtk.vtkActor()
        self.actor2.SetMapper(self.coneMapper2)
        self.frames.setLayout(self.vl)
        self.frames.setLineWidth(0.6)
        self.frames.setStyleSheet("border:1px solid #000000; border-radius:10px; background-color:#66b2ff")
        self.actor2.GetProperty().SetColor(0.5,0.5,0.5)# (R,G,B)
        self.actor2.SetScale(1, 1, 1)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.ren.AddActor(self.actor2)
        self.ren.SetBackground(0.398,0.695,0.996)
        self.iren.Initialize()
        self.iren.Start()
        self.frames.move(10,10)
        self.yon=QLabel('YÖN:',self.groupbox4)
        self.yon.setStyleSheet("border:1px solid #000000; font:bold 15px;")
        self.yon.setGeometry(30,280,90,25)
        #------------------------------------------------------------------------------------
        self.groupbox5=QGroupBox(self)
        self.groupbox5.setStyleSheet("background: #004C99;")   
        self.groupbox5.setGeometry(1250, 650, 300, 320)
        self.widget = AnalogGaugeWidget(self.groupbox5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setGeometry(10,30,280,280)
        self.widget.setMinimumSize(QtCore.QSize(100, 100))
        self.widget.setMaximumSize(QtCore.QSize(600, 600))
        self.widget.setBaseSize(QtCore.QSize(300, 300))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        #--------------------------------------------------------------------------------------
        
        #cal.clicked[QDate].connect(self.showDate)
        self.setWindowTitle("Arayuz")   
        self.show()
    def tarih1sec(self):   
        self.cal = QCalendarWidget(self.groupbox3)
        self.cal.setGridVisible(True)
        self.cal.move(210, 10)
        self.cal.show()
        self.cal.setStyleSheet("z-index: 8;")
        self.cal.clicked[QDate].connect(self.showDate)
    def start(self): #seri haberleşmeye başlamak için oluşturulmuş butonun tıklanması halinde haberleşmayi başlatan fonksiyon
        if str(self.portsecimi.currentText())== str('') and str(self.baudratesecimi.currentText())== str(''):
            print("Port Seçmediniz veya Baudrate Seçmediniz!!") 
        else:
            self.start.setDisabled(True)
            ser.port=str(self.portsecimi.currentText())
            ser.baudrate=int(self.baudratesecimi.currentText())
            ser.timeout=0.5
            ser.open()
            self.runnable = Runnable(self)
            QtCore.QThreadPool.globalInstance().start(self.runnable)
    def tarih2sec(self):   
        self.cal2 = QCalendarWidget(self.groupbox3)
        self.cal2.setGridVisible(True)
        self.cal2.move(210, 10)
        self.cal2.show()
        self.cal2.setStyleSheet("z-index: 8;")
        self.cal2.clicked[QDate].connect(self.showDate2)
    def showDate(self, date):
        self.tarih1.setText(date.toString())
        self.tarih1.setStyleSheet("color: black;")
        date = self.cal.selectedDate()
        self.cal.close()
        self.tarihsec2.setDisabled(False)
    def showDate2(self, date):
        self.tarih2.setText(date.toString())
        self.tarih2.setStyleSheet("color: black;")
        date = self.cal2.selectedDate()
        self.cal2.close()
    def portlar(self): #seri bağlı olmuş olan cihazın port adı bilgisini aldığımız fonksiyon
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    def stop(self):
        self.stop2.setDisabled(True)
        self.stopflag2 = True

class Runnable(QtCore.QRunnable,Pencere,QtCore.QThread):#verilerin okunduğu, arayüze eklendiği ve kaydedildiği sınıf
    def __init__(self, w, *args, **kwargs):
        QtCore.QRunnable.__init__(self, *args, **kwargs)
        self.w = w
    def run(self):
        while True:  
            if (self.w.stopflag): 
                self.w.stopflag = False
                break
            else:
                reading = ser.readline()
                if len(str(reading))>3:
                    try:
                        z=reading.decode('utf-8')
                    except UnicodeDecodeError:
                        continue                   
                    t=z.split(',')
                    if len(t)!=10:
                        continue
                    #tabloya veri girme im.execute("INSERT INTO personel VALUES ('Fırat', 'Özgül', 'Adana')")
                    #Bu girdiğimiz verileri veritabanına işleyebilmek için vt.commit()
                    self.w.tableWidget2.insertRow(0)
                    self.w.tableWidget2.setItem(0,0,QTableWidgetItem(str(now.toString(Qt.ISODate))+"/"+time.toString(Qt.DefaultLocaleLongDate)))
                    for i in range(1,11):
                        self.w.tableWidget2.setItem(0,i,QTableWidgetItem(str(t[i])))
        ser.close()
if __name__=="__main__":
    app=QApplication(sys.argv)
    pencere=Pencere()
    sys.exit(app.exec())