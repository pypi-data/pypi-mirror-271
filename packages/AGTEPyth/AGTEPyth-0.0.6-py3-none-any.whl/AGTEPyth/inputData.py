import sys
import math
import os
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QFileInfo, QSettings, QEvent, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
try:
    from AGTPytGD import Ui_TurboValQ
    from Functions import *
    from PRINT_RESULST_TO_DOCX import InFileResult
except:
    from AGTEPyth.AGTPytGD import Ui_TurboValQ
    from AGTEPyth.Functions import *
    from AGTEPyth.PRINT_RESULST_TO_DOCX import InFileResult    
app = QApplication(sys.argv) #Must construct a QApplication before a QWidget - lỗi này sẽ xuất hiện khi 1 Qwidget (đối tượng xây dựng từ 1 Qwidget bất kỳ như
#QMainWindow,QMessageBox...) được gọi (sử dụng lệnh .show()) trước khi gọi QApplication(sys.argv). Theo mặc định thì các Qwidget xây dựng từ module QMainwindow
#hoặc các Qwidget với vai trò là layout nền sẽ được show() sau QApplication(sys.argv) do đó QApplication(sys.argv) thường đặt dưới cùng trước lệnh show()
#tuy nhiên khi một số layout phụ ví dụ như widget cửa sổ thông báo xây dựng từ QMessageBox được gọi (show()) ở giữa chương trình khi sự kiện được gọi ra (tức là sau khi
#nền chính đã được gọi thì QApplication(sys.argv) khi đó cần đưa lên đầu để không vi phạm lỗi cú pháp.
#TẠO LỚP CỬA SỔ THÔNG BÁO (QMESSAGEBOX)
class MessageBox(QMessageBox): #Các đối tượng xây dựng layout phụ như cửa sổ thông báo xuất hiện khi gọi sự kiện không thuộc khai báo của class chính
    #cần được khai bảo trước class chính. Việc gọi các layout này có được thực hiện bằng lệnh show() trong class chính
    def __init__(self):
        QMessageBox.__init__(self) #Thêm thuộc tính cho class MessageBoxSave đang khai báo bằng cách gọi chính các phương thức
        #trong init khai báo thuộc tính mẫu của class cha. Lệnh này tương đương với lệnh super().__init__() cho 1 class cha
    def MessageBoxSave(self):
        self.setText("Файл сохранен!")
        #self.setInformativeText("Informative text provides more space to explain the message purpose.")#Thêm dòng thông báo phụ
        self.setIcon(QMessageBox.Information) #Thay đổi biểu tượng của thông báo, ở đây là dạng !.
        self.setStandardButtons(QMessageBox.Close) #Cài đặt nút mặc định
        #self.Ok = QPushButton('Да', self) QMessageBox cũng có thể tạo các PushButton để gắn sự kiện như QDialog
        self.setWindowTitle("Сообщение")
        try:
            self.setWindowIcon(QtGui.QIcon('iconMatryoshka.ico')) #Thêm icon cho thông báo theo mẫu: msgBox.setWindowIcon(QtGui.QIcon('PathToIcon/icon.png'))
        except:
            self.setWindowIcon(QtGui.QIcon('AGTEPyth\iconMatryoshka.ico'))
        self.show()
    def MessageBoxFalse(self):
        self.setText("Незаполненно значение или неправильный формат вводимых значений!")
        #self.setInformativeText("Informative text provides more space to explain the message purpose.")#Thêm dòng thông báo phụ
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Close)
        self.setWindowTitle("ВНИМАНИЕ!")#
        try:
            self.setWindowIcon(QtGui.QIcon('iconMatryoshka.ico')) #Thêm icon cho thông báo theo mẫu: msgBox.setWindowIcon(QtGui.QIcon('PathToIcon/icon.png'))
        except:
            self.setWindowIcon(QtGui.QIcon('AGTEPyth\iconMatryoshka.ico'))
        #self.Ok = QPushButton('Да', self) QMessageBox cũng có thể tạo các PushButton để gắn sự kiện như QDialog
        self.show()
    def FalseOpen(self):
        self.setText("Данные файла недоступны!")
        #self.setInformativeText("Informative text provides more space to explain the message purpose.")#Thêm dòng thông báo phụ
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Close)
        self.setWindowTitle("ВНИМАНИЕ!")#
        try:
            self.setWindowIcon(QtGui.QIcon('iconMatryoshka.ico')) #Thêm icon cho thông báo theo mẫu: msgBox.setWindowIcon(QtGui.QIcon('PathToIcon/icon.png'))
        except:
            self.setWindowIcon(QtGui.QIcon('AGTEPyth\iconMatryoshka.ico'))
        #self.Ok = QPushButton('Да', self) QMessageBox cũng có thể tạo các PushButton để gắn sự kiện như QDialog
        self.show()
    def InvalidFormat(self):
        self.setText("Неправильный формат '.rsk'")
        #self.setInformativeText("Informative text provides more space to explain the message purpose.")#Thêm dòng thông báo phụ
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Close)
        self.setWindowTitle("ВНИМАНИЕ!")#
        try:
            self.setWindowIcon(QtGui.QIcon('iconMatryoshka.ico')) #Thêm icon cho thông báo theo mẫu: msgBox.setWindowIcon(QtGui.QIcon('PathToIcon/icon.png'))
        except:
            self.setWindowIcon(QtGui.QIcon('AGTEPyth\iconMatryoshka.ico'))
            #self.Ok = QPushButton('Да', self) QMessageBox cũng có thể tạo các PushButton để gắn sự kiện như QDialog
        self.show()
MessageBox=MessageBox() #Vì nhiều tín hiệu signals tạo bởi các sự kiện có thể gọi được cùng 1 đường dẫn (slot) nên có thể dùng 1 Hộp thoại để báo nhiều trường hợp lỗi
#Cần xây dựng các đối tượng layout phụ là phương thức trong 1 class phụ kế thừa từ class gốc như QMessageBox, QDialog 
#và sau đó class đó với 1 biến để kích hoạt class bên ngoài khai báo class chính của chương trình
#còn nếu tạo đối tượng sau đó trong khai báo class của layout chính thì sẽ không có tác dụng vì không chứa các phương thức của class ngoài 
#hoặc nếu có tích hợp thêm kế thừa thì sẽ chồng chéo (không nên nếu không chuyên)

#TẠO LỚP CỬA SỔ HIỆN THÔNG TIN BỔ SUNG
TEXT_HELP=("Instruksia", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">ИНСТРУКЦИЯ К ДАННОЙ МЕДОТИКЕ</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">Методика предназначена для расчитать термодинамические циклы турбовальных ГТД</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">Горячие клавиши:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">- Открыть файл расчета (формат .rsx): Ctrl + O</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">- Сохранить текущий расчет: Ctrl + S</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">- Сохранить файл расчет в папку (сохранить как): Ctrl + K</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">- Выйти из программы (выход): Ctrl + E</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">- Расчитать вариант (Счет): Ctrl + Q</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">- Ввод данных заново: Ctrl + R</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f; background-color:#ffffff;\">- Инструкция программы: Ctrl + I</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f;\">...</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:10pt; color:#0f0f0f;\">Системные требования: Window 7 и выше, х64</span></p></body></html>")
TEXT_AUTHOR=("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">СЕРТИФИКАТ</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Автор: Фам Тхань Кует (аспирант - Вьетнам)</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Соавторы:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Год создана программа: 2023</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Организация: &quot;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; color:#000000;\">Турбины, гидромашины и авиационные двигатели&quot; - </span><span style=\" font-size:10pt;\">Институт Энергетики - СПбПУ Петра Великого</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">...</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p></body></html>")

class DialogWD(QDialog):
    def __init__(self):
        super().__init__()
    def DialogTEXT(self,TITLE,TEXT):
        self.setWindowTitle(TITLE)
        self.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.resize(380, 250)
        self.setMinimumSize(QtCore.QSize(380, 250))
        self.setMaximumSize(QtCore.QSize(380, 250))
        try:
            self.setWindowIcon(QtGui.QIcon('iconMatryoshka.ico')) #Thêm icon cho thông báo theo mẫu: msgBox.setWindowIcon(QtGui.QIcon('PathToIcon/icon.png'))
        except:
            self.setWindowIcon(QtGui.QIcon('AGTEPyth\iconMatryoshka.ico'))
        self.frame = QtWidgets.QFrame(self)
        self.frame.setEnabled(True)
        self.frame.setMinimumSize(QtCore.QSize(360, 250))
        self.frame.setMaximumSize(QtCore.QSize(360, 250))
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 360, 220))
        self.textBrowser.setMinimumSize(QtCore.QSize(340, 220))
        self.textBrowser.setMaximumSize(QtCore.QSize(340, 220))
        _translate = QtCore.QCoreApplication.translate
        self.textBrowser.setHtml(_translate(*TEXT)) #Phải bung các giá trị trong tuple thành đối số ntn mới sử dụng được làm đối số của _translate
        #Có thể đổi sang font Times New Roman,serif nhưng loại font này quá mảnh hiển thị màn hình máy tính cỡ nhỏ không đẹp, dễ mỏi mắt
        self.Close = QPushButton('Закрыть', self)
        self.Close.setGeometry(QtCore.QRect(165, 225, 60, 25))
        self.Close.clicked.connect(self.CancelClose)
        self.show()
    def CloseApp(self):
        sys.exit()
    def CancelClose(self):
        self.close()
DialogWindow=DialogWD()

#TẠO LỚP CỬA SỔ XÁC NHẬN (QDIALOG) ĐÓNG BÊN NGOÀI MAINWINDOW
class DialogCloseWD(QDialog):
    def __init__(self):
        super().__init__()
    def DialogClose(self):
        self.setWindowTitle('Вы действительно хотите выйти?')
        self.resize(250, 60)
        self.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.Ok = QPushButton('Да', self)
        self.Ok.move(30, 20)
        self.Ok.clicked.connect(self.CloseApp)
        try:
            self.setWindowIcon(QtGui.QIcon('iconMatryoshka.ico')) #Thêm icon cho thông báo theo mẫu: msgBox.setWindowIcon(QtGui.QIcon('PathToIcon/icon.png'))
        except:
            self.setWindowIcon(QtGui.QIcon('AGTEPyth\iconMatryoshka.ico'))
        self.Cancel = QPushButton('Нет', self)
        self.Cancel.move(142, 20)
        self.Cancel.clicked.connect(self.CancelClose)
        self.show()
    def CloseApp(self):
        sys.exit()
    def CancelClose(self):
        self.close()
DialogClose=DialogCloseWD()
#TẠO LỚP CỬA SỔ GIAO DIỆN TỪ FILE GIAO DIỆN ĐÃ TẠO TRÊN QTDESIGNER
class MainWindow(QMainWindow,QDialog,QWidget): #khai báo lớp sử dụng kế thừa các phương thức của QMainWindow,QWidget để có thể sử dụng chúng
    def __init__(self): #Khai báo thuộc tính bằng hàm contructor (init) để tạo khuôn mẫu thuộc tính gắn với các đối số từ bên ngoài
    #trong trường hợp này các đối số là các biến, hàm,... global đã được xác định trước khi khai báo class như Ui_TurboValQ(), cùng 
    #các đối tượng xây dựng giao diện trong Qt -> do đó đối số của init chỉ có self.
    #tất cả các sự kiện cơ bản đều phải được khai báo trong phần khai báo thuộc tính khuôn mẫu này, kết quả xử lý xự kiện sẽ được 
    #kết nối đến các phương thức của class thông qua phương thức connect của các class QtPy5 (hầu như đều có phương thức này).
        super().__init__()
        self.settingspos = QSettings('AppPTQ', 'A2GTPyt') #Tạo vị trí lưu và load các cấu hình vị trí thoát cuối cùng người dùng muốn lưu sau khi thoát ứng dụng
        try:
            self.move(self.settingspos.value('window position')) #Lấy giá trị ứng với cấu hình người dùng lưu mặc định làm đối số của phương thức gọi cấu hình tương ứng
            #Ở đây là giá trị vị trí của ứng dụng trong Qsetting được sử dụng làm đối số của phương thức tương ứng move() để di chuyển ứng dụng đến vị trí ở phiên làm việc trước đó
        except:
            pass
        self.uic = Ui_TurboValQ() #Gắn class Ui_TurboValQ vừa import từ file giao diện vào thuộc tính uic - đây sẽ là object chứa tất cả thuộc tính của lớp giao diện đã tạo
        self.uic.setupUi(self) #Gọi ra phương thức setupUi của uic (phương thức của class Ui_TurboValQ) với đối số cũng là chính class đang khai báo
        #để sau đó gọi các đối tượng trong phương thức này ra. Để dễ hình dung ta có thể thấy ở đây đối số self sau đó tương ứng với TurboValQ trong Ui_TurboValQ(), còn 
        #self.uic ứng với Ui_TurboValQ() (đã được gắn ở trên) hay ứng với chính self trong khai báo class Ui_TurboValQ().
        self.setWindowTitle('A2GTPyt') #ĐỔI LẠI TÊN CỬA SỔ PHẦN MỀM (THEO Ý THẦY)
        self.uic.progressBar.hide()
        self.uic.T3Chon1gd.setChecked(True)#Chọn phương án 1 luôn là mặc định
        self.uic.PiChon1gd.setChecked(True)
        self.uic.T3Listgd.setDisabled(True) #Thiết lập để phương án 2 luôn ẩn khi ban đầu chưa được chọn
        self.uic.PiListgd.setDisabled(True)
        self.uic.KPD_sentgd.setDisabled(True)
        self.WorkFile=0
        try:
            self.LoadSettingsFunc(sys.argv[1]) #Load dữ liệu khi mở (open with) từ file .ptq (đổi sang .rsk tri ân thầy) thông qua phương thức LoadSettingsFunc() của lớp
            self.WorkFile=1
        except:
            pass
        #self.uic.action_saveas.triggered.connect(self.SaveValues) #Kết nối đến lưu các dữ liệu nhập vào khi bấm nút lưu
        #Gắn các phương thức khi gọi các tác vụ
        self.uic.action_open.triggered.connect(self.openFileNameDialog)
        self.uic.action_save.triggered.connect(self.saveDialog)
        self.uic.action_saveas.triggered.connect(self.saveFileDialog)
        self.uic.action_run.triggered.connect(self.OpenDialogQuestion)
        self.uic.buttonRun.clicked.connect(self.OpenDialogQuestion)
        self.uic.action_resetting.triggered.connect(self.ResetSettings)

        self.uic.action_intruction.triggered.connect(self.DialogHelpMT) #!!!Thêm phần hướng dẫn
        self.uic.action_certificate.triggered.connect(self.DialogAuthorMT) #Có thể gọi trực tiếp cửa sổ không qua phương thức bằng DialogWindow.DialogAuthor 
        #Nhưng tốt nhất là tạo phương thức để gọi

        self.uic.action_exit.triggered.connect(self.close) #Kết nối đến phương thức close đóng giao diện.

        self.uic.T3Chon2gd.toggled.connect(self.T3ChonRadioButton) #Tạo sự kiện liên quan đến nút chọn phương án 2 của giá trị T3 
        #kết nối với các trường hợp trong phương thức T3ChonRadioButton nhằm xác nhận theo trạng thái ban đầu của nút này là không được check
        self.uic.PiChon2gd.toggled.connect(self.PiChonRadioButton) 
        #1 Sự kiện có thể kết nối tới 1 hoặc nhiều slot (đường dẫn)
        #self.uic.action_exit.setShortcut("Ctrl+E") #Thêm phím tắt cho tác vụ
        self.uic.TipKompgd.activated.connect(self.TipKompBox)

        #Định dạng lại các ô QDoubleSpinBox nhập giá trị để đồng bộ định dạng các mũi tên lên xuống (sau khi thay đổi do có lỗi)
        self.uic.T3Duoigd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Trengd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Buocgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiTrengd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiDuoigd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiBuocgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.KPD_sentgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")

        #Định nghĩa các thuộc tính là các biến hoặc container sẽ sử dụng để gắn giá trị có như vậy mới có thể sử dụng chúng trong các phương thức khác nhau
        #vì chúng là các thuộc tính của lớp, nếu không chúng chỉ có tác dụng là biến nội bộ (như trong khai báo hàm) trong chỉ phương thức đó.
        self.radiostatusT3,self.radiostatusPi=0,0 #Định nghĩa thuộc tính để tạo biến đọc liên kết trạng thái ban đầu (hiển thị nhưng thực tế là chưa chọn gì 
        #do đó cần gắn với 0 trùng giá trị của lựa chọn mặc định) của các nút radiobutton và combobox chọn nhập giá trị T3 và KPD máy nén khi xử lý dữ liệu
        self.T3_polnoe,self.Pi_polnoe,self.TipKomp,self.KPD_sent,self.MH,self.TH,self.DeltaT_Kom,self.DeltaT_VozOxl,self.T_ct,self.Sigma_vx,self.Sigma_kom,self.Sigma_ks,self.Fi_c,self.KPD_ks=[],[],0,0,'','','','','','','','','',''
        self.KPD_VnutT,self.h0_cr,self.g_otb_,self.g_utech_,self.alpha_,self.Ne,self.KPD_vnTV,self.KPD_reduk,self.k_ispol,self.X='','','','','','','','','',''
        self.T3Duoi,self.T3Tren,self.T3Buoc,self.PiDuoi,self.PiTren,self.PiBuoc=0,0,0,0,0,0
        self.UserName,self.UserGroup,self.T3List,self.PiList='','','',''
        self.fileNameOpen=''
        self.fileNameSave=''
        self.folderNameSelect='NotSelect'
        #TẠO NHÃN 'BẢN DEMO' BẢN QUYỀN TRƯỚC KHI ỨNG DỤNG ĐƯỢC ĐĂNG KÝ:
        '''self.uic.verticalLayout_Demo = QtWidgets.QVBoxLayout(self.uic.frame_13) #Tạo hộp bố cục QVBoxLayout trong frame_13 là khung đối tượng trống được chọn trên giao diện .ui để thêm nhãn
        self.uic.verticalLayout_Demo.setContentsMargins(0, 0, 0, 0) #Căn lề trên, dưới trái phải trong hộp bố cục về 0 hết
        self.uic.verticalLayout_Demo.setSpacing(0)
        self.uic.verticalLayout_Demo.setObjectName("verticalLayout_Demo")
        self.uic.TacGia_Demo = QtWidgets.QLabel(self.uic.frame_13) #Tạo 1 nhãn trong khung frame_13 và gắn các thuộc tính. Phải là QLabel mới xuống dòng được, Qline chỉ có 1 dòng
        self.uic.TacGia_Demo.setMaximumSize(QtCore.QSize(100, 80))
        font = QtGui.QFont() #Tạo các thuộc tính font để gắn vào nhãn
        font.setPointSize(10) #Cỡ chữ
        font.setBold(True) #Tạo in đậm
        font.setWeight(75)
        self.uic.TacGia_Demo.setFont(font) #Gắn thuộc tính font vào nhãn
        self.uic.TacGia_Demo.setObjectName("TacGia_Demo")
        self.uic.verticalLayout_Demo.addWidget(self.uic.TacGia_Demo) #Gắn nhãn với hộp bố cục đã tạo ra trước đó với lựa chọn căn giữa
        self.uic.TacGia_Demo.setAlignment(QtCore.Qt.AlignCenter)
        self.uic.TacGia_Demo.setStyleSheet("background: #458B74;""color: #FF8000;")
        self.uic.TacGia_Demo.setText("Демо-версия \n Ф. Т. Кует") #Thêm nội dung cho nhãn
        self.uic.TacGia_Demo.setWordWrap(True) #Cho phép xuống dòng
        self.uic.TacGia_Demo.setDisabled(True) #Tắt chỉnh sữa'''

        #ĐỊNH NGHĨA THUỘC TÍNH CÁC ĐỐI TƯỢNG BIỂU ĐỒ BAN ĐẦU CHO CLASS
        self.fig= plt.figure()
        self.ax1 = plt.subplot(2,1,1)
        self.ax2 = plt.subplot(2,1,2)
        self.line1, = self.ax1.plot([],[]) #Tạo các đường line2D rỗng line1, line2 trên các đối tượng biểu đồ ax1 và ax2
        self.line2, = self.ax2.plot([],[])
        self.ColumnNeudlist, self.ColumnCelist=[],[]
        self.ColumnNeudarray, self.ColumnCearray,self.ColumnNeudarray_, self.ColumnCearray_=np.array([]),np.array([]),np.array([]),np.array([])
        self.Pi_polnoearray,self.Pi_polnoearray_=np.array([]),np.array([])
        #Tạo dữ liệu định dạng đường của các đồ thị
        self.Markergraph=['.','o','v','^','<','>','1','2','3','4','s','P','p','*','h','d','+','x','X','D']

        self.Animateline1_=()
        self.Animateline2_=()
        self.anim = []
        self.SetProgr=0 #Tạo giá trị tính vòng lặp của hàm tính toán để đưa vào thanh tiến trình
    def DialogHelpMT(self):
        DialogWindow.DialogTEXT('Справка',TEXT_HELP)
    def DialogAuthorMT(self):
        DialogWindow.DialogTEXT('Об авторах',TEXT_AUTHOR)
    def ResetPlots(self): #TẠO LỚP RESET VÀ ĐỊNH NGHĨA LẠI CÁC THUỘC TÍNH BIỂU ĐỒ. PHƯƠNG THỨC NÀY PHẢI ĐƯỢC MỞ (LIÊN KẾT VỚI NÚT) TRƯỚC KHI CHẠY HÀM ĐỒ THỊ ĐỘNG
        plt.close()
        self.fig=plt.figure(num='Графики_A2GTPyt',figsize=(6.5,6.5),layout='tight',facecolor='#F0F8FF')#Tạo ra cửa sổ biểu đồ để chuẩn bị vẽ ở cuối module này
        #Tạo các vùng biểu đồ con
        self.ax1=plt.subplot(2,1,1)
        self.ax2=plt.subplot(2,1,2)
        self.Animateline1_=()
        self.Animateline2_=()
        IndexMarker=0 #Tạo index phần tử đầu của thuộc tính marker
        for k in range(len(self.T3_polnoe)):
            self.line1, = self.ax1.plot([],[],marker=self.Markergraph[IndexMarker],markersize=5,label=str(self.T3_polnoe[k])+' K') #Tạo các đường line2D rỗng line1, line2 trên các đối tượng biểu đồ ax1 và ax2
            self.line2, = self.ax2.plot([],[],marker=self.Markergraph[IndexMarker],markersize=5,label=str(self.T3_polnoe[k])+' K')
            self.Animateline1_+=(self.line1,)
            self.Animateline2_+=(self.line2,)
            IndexMarker+=1

    def CreateAnimPlots(self,i):
        for k in range(len(self.T3_polnoe)):
            #Các đường line thay đổi Neud vào T3_pol và Pik_pol
            self.Animateline1_[k].set_data(self.Pi_polnoearray_[:i,0],self.ColumnNeudarray_[:i,k])#Thêm đồ thị vào biểu đồ con sau mỗi vòng lặp
            self.Animateline2_[k].set_data(self.Pi_polnoearray_[:i,0],self.ColumnCearray_[:i,k])

    def ShowAnimPlots(self): #TẠO HÀM HIỂN THỊ 
        self.ResetPlots()
        self.uic.progressBar.setValue(85)
        self.anim = FuncAnimation(self.fig, self.CreateAnimPlots, frames=50, interval=50, repeat=False) #Tạo đối tượng đồ thị động từ hàm FuncAnimation()
        self.ax1.set_title('Зависимость удельной эффективной мощности от степени повышения давления\nпри разных значениях температур газа перед турбиной Т*3, К',fontsize=9,fontweight='bold')
        self.ax1.set_xlabel('П*к',fontsize=9,fontweight='bold',fontstyle='italic')
        self.ax1.set_ylabel('Neуд (кВт.с/кг)',fontsize=9,fontweight='bold',fontstyle='italic')
        self.ax1.set_xticks(ticks=np.arange(self.Pi_polnoe[0],self.Pi_polnoe[len(self.Pi_polnoe)-1]+1,2)) #Thiết lập chủ động hiển thị chia trục hoành khi biết giá trị cố định, xlim và ylim chỉ là giới hạn khoảng hiển thị
        self.ax1.grid(True,linewidth=0.5,color='black')
        self.ax1.grid(which='minor',linewidth=0.5)
        self.ax1.minorticks_on()
        self.ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator(n = 2))
        self.ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(n = 5))
        self.ax2.set_title('Зависимость удельного расхода топлива от степени повышения давления\nпри разных значениях температур газа перед турбиной Т*3, К',fontsize=9,fontweight='bold')
        self.ax2.set_xlabel('П*к',fontsize=9,fontweight='bold',fontstyle='italic')
        self.ax2.set_ylabel('СЕ (кг/кВт.ч)',fontsize=9,fontweight='bold',fontstyle='italic')
        self.ax2.set_xticks(ticks=np.arange(self.Pi_polnoe[0],self.Pi_polnoe[len(self.Pi_polnoe)-1]+1,2))
        self.ax2.grid(True,linewidth=0.5,color='black')
        self.ax2.grid(which='minor',linewidth=0.5)
        self.ax2.minorticks_on()
        self.ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator(n = 2))
        self.ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(n = 5))
        self.ax1.set_xlim(self.Pi_polnoe[0],self.Pi_polnoe[-1]) #Điều chỉnh thuộc tính của biểu đồ ax1
        self.ax1.set_ylim(math.floor(np.amin(self.ColumnNeudarray)/50)*50, math.ceil(np.amax(self.ColumnNeudarray)/50)*50)
        self.ax2.set_xlim(self.Pi_polnoe[0],self.Pi_polnoe[-1]) #Điều chỉnh thuộc tính của biểu đồ ax2
        self.ax2.set_ylim(math.floor(np.amin(self.ColumnCearray)*10)/10, math.ceil(np.amax(self.ColumnCearray)*10)/10)
        self.ax1.legend(ncol=2,loc='lower left',bbox_to_anchor=(0.05, 0., 0.5, 0.5),framealpha=1.0,fontsize=9,shadow=True)
        self.ax2.legend(ncol=2,loc='upper center',framealpha=1.0,fontsize=9,shadow=True)
        self.uic.progressBar.setValue(88)
        self.uic.progressBar.setValue(90)
        self.uic.progressBar.setValue(92)
        self.uic.progressBar.setValue(94)
        self.uic.progressBar.setValue(96)
        self.uic.progressBar.setValue(98)
        self.uic.progressBar.setValue(100)
        plt.show()
        self.uic.progressBar.hide()
    #TẠO LỚP CỬA SỔ XÁC NHẬN (QDIALOG) CHUYỂN CÂU LỆNH BÊN TRONG MAINWINDOW ĐỂ XÁC NHẬN LƯU/KO LƯU KẾT QUẢ VÀ CHẠY
    def OpenDialogQuestion(self,QDialog): #Tạo hộp thoại save file
        self.uic.progressBar.setValue(0)
        self.windowDialog=QtWidgets.QDialog()
        try:
            self.windowDialog.setWindowIcon(QtGui.QIcon('iconMatryoshka.ico')) 
        except:
            self.windowDialog.setWindowIcon(QtGui.QIcon('AGTEPyth\iconMatryoshka.ico'))
        self.windowDialog.setWindowTitle('Сохранить результаты?')
        self.windowDialog.resize(250, 60)
        self.windowDialog.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.windowDialog.Ok = QPushButton('Да', self.windowDialog)
        self.windowDialog.Ok.move(30, 20)
        self.windowDialog.Ok.clicked.connect(self.ChoseFolder)
        self.windowDialog.Cancel = QPushButton('Нет', self.windowDialog)
        self.windowDialog.Cancel.move(142, 20)
        self.windowDialog.Cancel.clicked.connect(self.CancelClose)
        self.windowDialog.show()
    def ChoseFolder(self): #Tạo hộp thoại save file
        self.windowDialog.close()
        folderName = str(QFileDialog.getExistingDirectory(self, "Выбирайте папку для сохранения результатов!"))
        if folderName:
            self.folderNameSelect=str(folderName)
            self.uic.progressBar.show()
            try:
                self.SolutionThermalCycle()
                self.ThermalCycle(self.T3_polnoe,self.Pi_polnoe,self.TipKomp,self.KPD_sent,self.MH,self.TH,self.DeltaT_Kom,self.DeltaT_VozOxl,
                self.T_ct,self.Sigma_vx,self.Sigma_kom,self.Sigma_ks,self.Fi_c,self.KPD_ks,self.KPD_VnutT,self.h0_cr,self.g_otb_,
                self.g_utech_,self.alpha_,self.k_ispol,self.Ne,self.X,self.KPD_vnTV,self.KPD_reduk,self.folderNameSelect,self.UserName,self.UserGroup)
                self.ColumnNeudarray, self.ColumnCearray=np.array(self.ColumnNeudlist),np.array(self.ColumnCelist)
                self.ColumnNeudarray_, self.ColumnCearray_=self.ColumnNeudarray.transpose(), self.ColumnCearray.transpose()
                self.ResetPlots()
                self.uic.progressBar.setValue(55)

                self.ax1.set_title('Зависимость удельной эффективной мощности от степени повышения давления\nпри разных значениях температур газа перед турбиной Т*3, К',fontsize=9,fontweight='bold')
                self.ax1.set_xlabel('П*к',fontsize=9,fontweight='bold',fontstyle='italic')
                self.ax1.set_ylabel('Neуд (кВт.с/кг)',fontsize=9,fontweight='bold',fontstyle='italic')
                self.ax1.set_xticks(ticks=np.arange(self.Pi_polnoe[0],self.Pi_polnoe[len(self.Pi_polnoe)-1]+1,2)) #Thiết lập chủ động hiển thị chia trục hoành khi biết giá trị cố định, xlim và ylim chỉ là giới hạn khoảng hiển thị
                self.ax1.grid(True,linewidth=0.5,color='black')
                self.ax1.grid(which='minor',linewidth=0.5)
                self.ax1.minorticks_on()
                self.ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator(n = 2))
                self.ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(n = 5))
                self.ax2.set_title('Зависимость удельного расхода топлива от степени повышения давления\nпри разных значениях температур газа перед турбиной Т*3, К',fontsize=9,fontweight='bold')
                self.ax2.set_xlabel('П*к',fontsize=9,fontweight='bold',fontstyle='italic')
                self.ax2.set_ylabel('СЕ (кг/кВт.ч)',fontsize=9,fontweight='bold',fontstyle='italic')
                self.ax2.set_xticks(ticks=np.arange(self.Pi_polnoe[0],self.Pi_polnoe[len(self.Pi_polnoe)-1]+1,2))
                self.ax2.grid(True,linewidth=0.5,color='black')
                self.ax2.grid(which='minor',linewidth=0.5)
                self.ax2.minorticks_on()
                self.ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator(n = 2))
                self.ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(n = 5))
                self.ax1.set_xlim(self.Pi_polnoe[0],self.Pi_polnoe[-1]) #Điều chỉnh thuộc tính của biểu đồ ax1
                self.ax1.set_ylim(math.floor(np.amin(self.ColumnNeudarray)/50)*50, math.ceil(np.amax(self.ColumnNeudarray)/50)*50)
                self.ax2.set_xlim(self.Pi_polnoe[0],self.Pi_polnoe[-1]) #Điều chỉnh thuộc tính của biểu đồ ax2
                self.ax2.set_ylim(math.floor(np.amin(self.ColumnCearray)*10)/10, math.ceil(np.amax(self.ColumnCearray)*10)/10)
                self.ax1.legend(ncol=2,loc='lower left',bbox_to_anchor=(0.05, 0., 0.5, 0.5),framealpha=1.0,fontsize=9,shadow=True)
                self.ax2.legend(ncol=2,loc='upper center',framealpha=1.0,fontsize=9,shadow=True)
                self.uic.progressBar.setValue(88)

                self.uic.progressBar.setValue(100)
                
                self.uic.progressBar.hide()
                IndexMarker=0 #Chạy lại đồ thị để ghi - mất thêm hơn 1s của phần mềm vì animation không thể ghi được hình cuối trọn vẹn (chỉ là 1 góc của biểu đồ) và nhanh hơn
                #Ở đây bắt buộc phải máy móc chạy lại y hệt các code lệnh như trên là vì để cho kết quả ghi này phải được gửi đến plt sau nếu không nó sẽ hiển thị thay vì animation (đã thử rất nhiều lần rồi).
                for k in range(len(self.T3_polnoe)):
                    self.line1, = self.ax1.plot([],[],marker=self.Markergraph[IndexMarker],markersize=5,label=str(self.T3_polnoe[k])+' K') #Tạo các đường line2D rỗng line1, line2 trên các đối tượng biểu đồ ax1 và ax2
                    self.line2, = self.ax2.plot([],[],marker=self.Markergraph[IndexMarker],markersize=5,label=str(self.T3_polnoe[k])+' K')
                    self.Animateline1_+=(self.line1,)
                    self.Animateline2_+=(self.line2,)
                    IndexMarker+=1
                for k in range(len(self.T3_polnoe)):
                    self.Animateline1_[k].set_data(self.Pi_polnoearray_[:,0],self.ColumnNeudarray_[:,k])#Thêm đồ thị vào biểu đồ con sau mỗi vòng lặp
                    self.Animateline2_[k].set_data(self.Pi_polnoearray_[:,0],self.ColumnCearray_[:,k])
                plt.show()
            except:
                MessageBox.MessageBoxFalse()
                self.uic.progressBar.setValue(0)
                self.uic.progressBar.hide()
        else:
            pass
    def CancelClose(self):
        self.folderNameSelect='NotSelect' #QQ Để ngăn không cho nhớ đường dẫn ở lần lưu trước đó
        self.windowDialog.close()
        self.uic.progressBar.show()
        try:
            self.SolutionThermalCycle()
            self.ThermalCycle(self.T3_polnoe,self.Pi_polnoe,self.TipKomp,self.KPD_sent,self.MH,self.TH,self.DeltaT_Kom,self.DeltaT_VozOxl,
                self.T_ct,self.Sigma_vx,self.Sigma_kom,self.Sigma_ks,self.Fi_c,self.KPD_ks,self.KPD_VnutT,self.h0_cr,self.g_otb_,
                self.g_utech_,self.alpha_,self.k_ispol,self.Ne,self.X,self.KPD_vnTV,self.KPD_reduk,self.folderNameSelect,self.UserName,self.UserGroup)
            self.ColumnNeudarray, self.ColumnCearray=np.array(self.ColumnNeudlist),np.array(self.ColumnCelist)
            self.ColumnNeudarray_, self.ColumnCearray_=self.ColumnNeudarray.transpose(), self.ColumnCearray.transpose()
            #Chạy lại đồ thị để ghi - mất thêm hơn 1s của phần mềm vì animation không thể ghi được hình cuối trọn vẹn (chỉ là 1 góc của biểu đồ) và nhanh hơn
            #Ở đây bắt buộc phải máy móc chạy lại y hệt các code lệnh như trên là vì để cho kết quả ghi này phải được gửi đến plt sau nếu không nó sẽ hiển thị thay vì animation (đã thử rất nhiều lần rồi).
            self.ResetPlots()
            self.uic.progressBar.setValue(55)

            self.ax1.set_title('Зависимость удельной эффективной мощности от степени повышения давления\nпри разных значениях температур газа перед турбиной Т*3, К',fontsize=9,fontweight='bold')
            self.ax1.set_xlabel('П*к',fontsize=9,fontweight='bold',fontstyle='italic')
            self.ax1.set_ylabel('Neуд (кВт.с/кг)',fontsize=9,fontweight='bold',fontstyle='italic')
            self.ax1.set_xticks(ticks=np.arange(self.Pi_polnoe[0],self.Pi_polnoe[len(self.Pi_polnoe)-1]+1,2)) #Thiết lập chủ động hiển thị chia trục hoành khi biết giá trị cố định, xlim và ylim chỉ là giới hạn khoảng hiển thị
            self.ax1.grid(True,linewidth=0.5,color='black')
            self.ax1.grid(which='minor',linewidth=0.5)
            self.ax1.minorticks_on()
            self.ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator(n = 2))
            self.ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(n = 5))
            self.ax2.set_title('Зависимость удельного расхода топлива от степени повышения давления\nпри разных значениях температур газа перед турбиной Т*3, К',fontsize=9,fontweight='bold')
            self.ax2.set_xlabel('П*к',fontsize=9,fontweight='bold',fontstyle='italic')
            self.ax2.set_ylabel('СЕ (кг/кВт.ч)',fontsize=9,fontweight='bold',fontstyle='italic')
            self.ax2.set_xticks(ticks=np.arange(self.Pi_polnoe[0],self.Pi_polnoe[len(self.Pi_polnoe)-1]+1,2))
            self.ax2.grid(True,linewidth=0.5,color='black')
            self.ax2.grid(which='minor',linewidth=0.5)
            self.ax2.minorticks_on()
            self.ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator(n = 2))
            self.ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(n = 5))
            self.ax1.set_xlim(self.Pi_polnoe[0],self.Pi_polnoe[-1]) #Điều chỉnh thuộc tính của biểu đồ ax1
            self.ax1.set_ylim(math.floor(np.amin(self.ColumnNeudarray)/50)*50, math.ceil(np.amax(self.ColumnNeudarray)/50)*50)
            self.ax2.set_xlim(self.Pi_polnoe[0],self.Pi_polnoe[-1]) #Điều chỉnh thuộc tính của biểu đồ ax2
            self.ax2.set_ylim(math.floor(np.amin(self.ColumnCearray)*10)/10, math.ceil(np.amax(self.ColumnCearray)*10)/10)
            self.ax1.legend(ncol=2,loc='lower left',bbox_to_anchor=(0.05, 0., 0.5, 0.5),framealpha=1.0,fontsize=9,shadow=True)
            self.ax2.legend(ncol=2,loc='upper center',framealpha=1.0,fontsize=9,shadow=True)
            self.uic.progressBar.setValue(88)
            self.uic.progressBar.setValue(90)
            self.uic.progressBar.setValue(92)
            self.uic.progressBar.setValue(94)
            self.uic.progressBar.setValue(96)
            self.uic.progressBar.setValue(98)
            self.uic.progressBar.setValue(100)
            
            self.uic.progressBar.hide()
            IndexMarker=0 #Chạy lại đồ thị để ghi - mất thêm hơn 1s của phần mềm vì animation không thể ghi được hình cuối trọn vẹn (chỉ là 1 góc của biểu đồ) và nhanh hơn
            #Ở đây bắt buộc phải máy móc chạy lại y hệt các code lệnh như trên là vì để cho kết quả ghi này phải được gửi đến plt sau nếu không nó sẽ hiển thị thay vì animation (đã thử rất nhiều lần rồi).
            for k in range(len(self.T3_polnoe)):
                self.line1, = self.ax1.plot([],[],marker=self.Markergraph[IndexMarker],markersize=5,label=str(self.T3_polnoe[k])+' K') #Tạo các đường line2D rỗng line1, line2 trên các đối tượng biểu đồ ax1 và ax2
                self.line2, = self.ax2.plot([],[],marker=self.Markergraph[IndexMarker],markersize=5,label=str(self.T3_polnoe[k])+' K')
                self.Animateline1_+=(self.line1,)
                self.Animateline2_+=(self.line2,)
                IndexMarker+=1
            for k in range(len(self.T3_polnoe)):
                self.Animateline1_[k].set_data(self.Pi_polnoearray_[:,0],self.ColumnNeudarray_[:,k])#Thêm đồ thị vào biểu đồ con sau mỗi vòng lặp
                self.Animateline2_[k].set_data(self.Pi_polnoearray_[:,0],self.ColumnCearray_[:,k])
            plt.show()
        except:
            MessageBox.MessageBoxFalse()
            self.uic.progressBar.setValue(0)
            self.uic.progressBar.hide()
    def saveDialog(self):
        if self.WorkFile==0: #Trường hợp tạo mới hoàn toàn sẽ mở ra cửa sổ saveas khi bấm lưu
            self.saveFileDialog()
        elif self.WorkFile==1: #Trường hợp mở ứng dụng từ file sẽ tự động gán lại workfile=1 để khi bấm save sẽ lưu đè lên file đó
            self.SaveSettingsFunc(sys.argv[1])
            MessageBox.MessageBoxSave()
        elif self.WorkFile==2: #Trường hợp mở file lên từ ứng dụng sẽ tự động gán lại workfile=2 để khi bấm save sẽ lưu đè lên file vừa mở    
            self.SaveSettingsFunc(self.fileNameOpen)
            MessageBox.MessageBoxSave()
        elif self.WorkFile==3: #Khi tạo file mới từ ứng dụng sau đó lưu file sẽ tự động gán lại workfile=3 để khi thay đổi và bấm save sẽ lưu đè lên file đó
            self.SaveSettingsFunc(self.fileNameSave)
            MessageBox.MessageBoxSave()
        else:
            pass
    def SolutionThermalCycle(self): #QQ Phương thức định dạng lại màu các ô (giá trị giữ nguyên) về dạng ban đầu trước khi kiểm tra lại xem các giá trị đó có đúng định dạng không
        self.uic.progressBar.setValue(1)
        #Định dạng lại các ô QDoubleSpinBox và QLineEdit nhập giá trị để trả lại định dạng bình thường sau đó kiểm tra lại định dạng các giá trị này có lỗi hay không
        self.uic.T3Duoigd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Trengd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Buocgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiTrengd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiDuoigd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiBuocgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.KPD_sentgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Listgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.PiListgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.MHgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.THgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.DeltaT_Komgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.DeltaT_VozOxlgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.T_ctgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Sigma_vxgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Sigma_komgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Sigma_ksgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Fi_cgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_ksgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_VnutTgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.h0_crgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.g_otb_gd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.g_utech_gd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.alpha_gd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Negd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_vnTVgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_redukgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.k_ispolgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Xgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        #QQ bắt đầu xuất và kiểm tra các giá trị từ giao diện
        self.UserName=self.uic.HoTengd.text()
        self.UserGroup=self.uic.Nhomgd.text()
        self.T3_polnoe,self.Pi_polnoe=[],[]#Định nghĩa lại danh sách giá trị T3, Pi mỗi khi lặp lại sự kiện bấm run để không nhớ các kết quả lỗi đã lưu
        #Định nghĩa lại các giá trị cận dưới, trên và bước của T3 mỗi khi lặp lại sự kiện bấm run để ghi lại các kết quả lần nhập sau (thay đổi trước khi bấm run lại) nếu không nó mặc định chúng =0 theo khai báo thuộc tính.
        #Còn nếu ta định nghĩa sau thì sẽ không ghi nhận giá trị chính xác trước khi bấm run.
        self.uic.progressBar.setValue(4)
        self.T3Duoi,self.T3Tren,self.T3Buoc,self.PiDuoi,self.PiTren,self.PiBuoc=self.uic.T3Duoigd.value(),self.uic.T3Trengd.value(),self.uic.T3Buocgd.value(),self.uic.PiDuoigd.value(),self.uic.PiTrengd.value(),self.uic.PiBuocgd.value()
        if self.radiostatusT3==0:
            if self.T3Duoi==self.T3Tren and self.T3Duoi!=0:
                self.T3_polnoe.append(self.T3Duoi)
            elif self.T3Tren==0 or self.T3Duoi>self.T3Tren or self.T3Buoc==0:
                self.uic.T3Duoigd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}") #Phương án: Tạo khung màu cho ô nhập số để đánh dấu lỗi ra màn hình
                self.uic.T3Trengd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                self.uic.T3Buocgd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                    #Các mũi tên của hộp spin chỉ có thể can thiệp bằng cách nhập hình ảnh thay thế bên ngoài (như nhập icon) còn mặc định nó sẽ nhảy do đó cần đồng bộ lại các Qdoublespinbox tại khai báo thuộc tính trước
                    #self.uic.T3Trengd.setStyleSheet('background-color: #FF0000;') #Phương án: Cài đặt tô màu cho ô nhập số để đánh dấu lỗi ra màn hình
                    #self.uic.T3Trengd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid red;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}") #Phương án: Tạo khung màu cho ô nhập số để đánh dấu lỗi ra màn hình
                    #Chỉ phù hợp nếu các ô nhập ở chế độ bình thường (plain text) chứ ko phải nổi (raise) hay chìm...
                MessageBox.MessageBoxFalse()
            elif ((self.T3Tren-self.T3Duoi)/self.T3Buoc)>20:
                self.uic.T3Duoigd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}") #Phương án: Tạo khung màu cho ô nhập số để đánh dấu lỗi ra màn hình
                self.uic.T3Trengd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                self.uic.T3Buocgd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                MessageBox.MessageBoxFalse()
            else:
                while self.T3Duoi<=self.T3Tren:
                    self.T3_polnoe.append(round(self.T3Duoi,2))
                    self.T3Duoi+=self.T3Buoc
        else:
            try:
                self.T3List=self.uic.T3Listgd.text()
                self.T3_polnoe=self.T3List.split(',')
                for i in range(len(self.T3_polnoe)):
                    T3_polnoefloat=float(self.T3_polnoe[i])
                    self.T3_polnoe[i]=T3_polnoefloat
            except:
                self.T3_polnoe=[] #Phải định nghĩa lại self.T3_polnoe vì trong khối try có khối lệnh mạnh tương đương với việc tạo giá trị T3List xác định ngay trong khối try
                #do đó dù có lỗi nhưng self.T3_polnoe vẫn bị gắn giá trị mới tại vị trí trước khi có lỗi (xem xử lý ngoại lệ trong tài liệu Quyết_Học Python)
                self.uic.T3Listgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
                MessageBox.MessageBoxFalse()
        if self.radiostatusPi==0: 
            if self.PiDuoi==self.PiTren and self.PiDuoi!=0:
                self.Pi_polnoe.append(self.PiDuoi)
            elif self.PiTren==0 or self.PiDuoi>self.PiTren or self.PiBuoc==0:
                self.uic.PiDuoigd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}") #Phương án: Tạo khung màu cho ô nhập số để đánh dấu lỗi ra màn hình
                self.uic.PiTrengd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                self.uic.PiBuocgd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                MessageBox.MessageBoxFalse()
            elif  ((self.PiTren-self.PiDuoi)/self.PiBuoc)>20:
                self.uic.PiDuoigd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}") #Phương án: Tạo khung màu cho ô nhập số để đánh dấu lỗi ra màn hình
                self.uic.PiTrengd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                self.uic.PiBuocgd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
                MessageBox.MessageBoxFalse()
            else:
                while self.PiDuoi<=self.PiTren:
                    self.Pi_polnoe.append(round(self.PiDuoi,2))
                    self.PiDuoi+=self.PiBuoc
        else:
            try:
                self.PiList=self.uic.PiListgd.text()
                self.Pi_polnoe=self.PiList.split(',')
                for i in range(len(self.Pi_polnoe)):
                    Pi_polnoefloat=float(self.Pi_polnoe[i])
                    self.Pi_polnoe[i]=Pi_polnoefloat
            except:
                self.Pi_polnoe=[] #Phải định nghĩa lại self.Pi_polnoe vì trong khối try có khối lệnh mạnh tương đương với việc tạo giá trị PiList xác định ngay trong khối try
                #do đó dù có lỗi nhưng self.T3_polnoe vẫn bị gắn giá trị mới tại vị trí trước khi có lỗi (xem xử lý ngoại lệ trong tài liệu Quyết_Học Python)
                self.uic.PiListgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
                MessageBox.MessageBoxFalse()
        #Xác định loại máy nén và công thức tính KPD máy nén
        self.TipKomp=self.uic.TipKompgd.currentIndex()
        self.KPD_sent=self.uic.KPD_sentgd.value()
        if self.TipKomp==2 and self.KPD_sent==0:
            self.uic.KPD_sentgd.setStyleSheet("QDoubleSpinBox""{""background-color: #FF3030;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.MH=float(self.uic.MHgd.text())
        except:
            self.uic.MHgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.TH=float(self.uic.THgd.text())
        except:
            self.uic.THgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.DeltaT_Kom=float(self.uic.DeltaT_Komgd.text())
        except:
            self.uic.DeltaT_Komgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.DeltaT_VozOxl=float(self.uic.DeltaT_VozOxlgd.text())
        except:
            self.uic.DeltaT_VozOxlgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.T_ct=float(self.uic.T_ctgd.text())
        except:
            self.uic.T_ctgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.Sigma_vx=float(self.uic.Sigma_vxgd.text())
        except:
            self.uic.Sigma_vxgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.Sigma_kom=float(self.uic.Sigma_komgd.text())
        except:
            self.uic.Sigma_komgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.Sigma_ks=float(self.uic.Sigma_ksgd.text())
        except:
            self.uic.Sigma_ksgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.Fi_c=float(self.uic.Fi_cgd.text())
        except:
            self.uic.Fi_cgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.KPD_ks=float(self.uic.KPD_ksgd.text())
        except:
            self.uic.KPD_ksgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.KPD_VnutT=float(self.uic.KPD_VnutTgd.text())
        except:
            self.uic.KPD_VnutTgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.h0_cr=float(self.uic.h0_crgd.text())
        except:
            self.uic.h0_crgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.g_otb_=float(self.uic.g_otb_gd.text())
        except:
            self.uic.g_otb_gd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.g_utech_=float(self.uic.g_utech_gd.text())
        except:
            self.uic.g_utech_gd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.alpha_=float(self.uic.alpha_gd.text())
        except:
            self.uic.alpha_gd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.k_ispol=float(self.uic.k_ispolgd.text())
        except:
            self.uic.k_ispolgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.Ne=float(self.uic.Negd.text())
        except:
            self.uic.Negd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.X=float(self.uic.Xgd.text())
        except:
            self.uic.Xgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.KPD_vnTV=float(self.uic.KPD_vnTVgd.text())
        except:
            self.uic.KPD_vnTVgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        try:
            self.KPD_reduk=float(self.uic.KPD_redukgd.text())
        except:
            self.uic.KPD_redukgd.setStyleSheet("QLineEdit""{""background-color: #FF3030;""}""QLineEdit::hover""{""border : 1px solid black;""}")
            MessageBox.MessageBoxFalse()
        self.Pi_polnoearray=np.array([self.Pi_polnoe])
        self.Pi_polnoearray_=self.Pi_polnoearray.transpose()
        #In Kiểm tra
        #Alist=(self.T3_polnoe,self.Pi_polnoe,self.TipKomp,self.KPD_sent,self.MH,self.TH,self.DeltaT_Kom,self.DeltaT_VozOxl,self.T_ct,self.Sigma_vx,self.Sigma_kom,self.Sigma_ks,self.Fi_c,self.KPD_ks,self.KPD_VnutT,self.h0_cr,self.g_otb_,self.g_utech_,self.alpha_,self.k_ispol,self.Ne,self.X,self.KPD_vnTV,self.KPD_reduk)
        #print(Alist)
        self.uic.progressBar.setValue(5)
        self.uic.progressBar.setValue(10)
        self.ColumnNeudlist, self.ColumnCelist=[],[] #QQ Reset lại tất cả các interable chứa các tập giá trị được gắn lại trong phương thức tính toán về rỗng để chuẩn bị chứa các giá trị ở lượt tính mới
        self.ColumnNeudarray, self.ColumnCearray,self.ColumnNeudarray_, self.ColumnCearray_=np.array([]),np.array([]),np.array([]),np.array([])
    def ResetSettings(self):
        #Định dạng lại các ô lỗi trước khi reset giá trị
        self.uic.T3Duoigd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Trengd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Buocgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiTrengd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiDuoigd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.PiBuocgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.KPD_sentgd.setStyleSheet("QDoubleSpinBox""{""border : 1px solid #838B8B;""}""QDoubleSpinBox::hover""{""border : 1px solid black;""}")
        self.uic.T3Listgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.PiListgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.MHgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.THgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.DeltaT_Komgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.DeltaT_VozOxlgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.T_ctgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Sigma_vxgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Sigma_komgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Sigma_ksgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Fi_cgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_ksgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_VnutTgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.h0_crgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.g_otb_gd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.g_utech_gd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.alpha_gd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Negd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_vnTVgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.KPD_redukgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.k_ispolgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.Xgd.setStyleSheet("QLineEdit""{""border : 1px solid #838B8B;""}""QLineEdit::hover""{""border : 1px solid black;""}")
        self.uic.HoTengd.setText('')
        self.uic.Nhomgd.setText('')
        self.uic.T3Chon1gd.setChecked(True)
        self.uic.T3Duoigd.setEnabled(True)
        self.uic.T3Trengd.setEnabled(True)
        self.uic.T3Buocgd.setEnabled(True)
        self.uic.T3Duoigd.setValue(0)
        self.uic.T3Trengd.setValue(0)
        self.uic.T3Buocgd.setValue(0)
        self.uic.T3Listgd.setText('')
        self.uic.T3Listgd.setDisabled(True)
        self.uic.PiChon1gd.setChecked(True)
        self.uic.PiDuoigd.setEnabled(True)
        self.uic.PiTrengd.setEnabled(True)
        self.uic.PiBuocgd.setEnabled(True)
        self.uic.PiDuoigd.setValue(0)
        self.uic.PiTrengd.setValue(0)
        self.uic.PiBuocgd.setValue(0)
        self.uic.PiListgd.setText('')
        self.uic.PiListgd.setDisabled(True)
        self.uic.TipKompgd.setCurrentIndex(0)
        self.uic.KPD_sentgd.setValue(0)
        self.uic.KPD_sentgd.setDisabled(True)
        self.uic.MHgd.setText('')
        self.uic.THgd.setText('')
        self.uic.DeltaT_Komgd.setText('')
        self.uic.DeltaT_VozOxlgd.setText('')
        self.uic.T_ctgd.setText('')
        self.uic.Sigma_vxgd.setText('')
        self.uic.Sigma_komgd.setText('')
        self.uic.Sigma_ksgd.setText('')
        self.uic.Fi_cgd.setText('')
        self.uic.KPD_ksgd.setText('')
        self.uic.KPD_VnutTgd.setText('')
        self.uic.h0_crgd.setText('')
        self.uic.g_otb_gd.setText('')
        self.uic.g_utech_gd.setText('')
        self.uic.alpha_gd.setText('')
        self.uic.Negd.setText('')
        self.uic.KPD_vnTVgd.setText('')
        self.uic.KPD_redukgd.setText('')
        self.uic.k_ispolgd.setText('')
        self.uic.Xgd.setText('')
        #QQ Reset các thuộc tính của class về mặc định trước khi load dữ liệu từ file để reset các thông số đầu vào của hàm tính toán tránh bị chồng chéo 
        self.radiostatusT3,self.radiostatusPi=0,0 #Định nghĩa thuộc tính để tạo biến đọc liên kết trạng thái ban đầu (hiển thị nhưng thực tế là chưa chọn gì 
        #do đó cần gắn với 0 trùng giá trị của lựa chọn mặc định) của các nút radiobutton và combobox chọn nhập giá trị T3 và KPD máy nén khi xử lý dữ liệu
        self.T3_polnoe,self.Pi_polnoe,self.TipKomp,self.KPD_sent,self.MH,self.TH,self.DeltaT_Kom,self.DeltaT_VozOxl,self.T_ct,self.Sigma_vx,self.Sigma_kom,self.Sigma_ks,self.Fi_c,self.KPD_ks=[],[],0,0,'','','','','','','','','',''
        self.KPD_VnutT,self.h0_cr,self.g_otb_,self.g_utech_,self.alpha_,self.Ne,self.KPD_vnTV,self.KPD_reduk,self.k_ispol,self.X='','','','','','','','','',''
        self.T3Duoi,self.T3Tren,self.T3Buoc,self.PiDuoi,self.PiTren,self.PiBuoc=0,0,0,0,0,0
        self.UserName,self.UserGroup,self.T3List,self.PiList='','','',''
        #QQ Cần reset lại các iterable chứa các kết quả đầu ra để xóa các kết quả ở lần tính toán trước đó trước khi load dữ liệu từ file nhất là khi tính toán nhiều lần trong 1 phiên làm việc với phần mềm
        self.ColumnNeudlist, self.ColumnCelist=[],[]
        self.ColumnNeudarray, self.ColumnCearray,self.ColumnNeudarray_, self.ColumnCearray_=np.array([]),np.array([]),np.array([]),np.array([])
        self.Pi_polnoearray,self.Pi_polnoearray_=np.array([]),np.array([])
        #Tạo dữ liệu định dạng đường của các đồ thị
        self.Animateline1_=()
        self.Animateline2_=()
        self.anim = []
    def SaveSettingsFunc(self,fileName):
        SaveSettings=QSettings(fileName,QSettings.IniFormat)
        SaveSettings.setValue('HoTengd',self.uic.HoTengd.text())
        SaveSettings.setValue('Nhomgd',self.uic.Nhomgd.text())
        SaveSettings.setValue('radiostatusT3',self.radiostatusT3)
        if self.radiostatusT3==0:
            SaveSettings.setValue('T3Duoigd',self.uic.T3Duoigd.value())
            SaveSettings.setValue('T3Trengd',self.uic.T3Trengd.value())
            SaveSettings.setValue('T3Buocgd',self.uic.T3Buocgd.value())
        else:
            SaveSettings.setValue('T3Listgd',self.uic.T3Listgd.text())
        SaveSettings.setValue('radiostatusPi',self.radiostatusPi)
        if self.radiostatusPi==0:
            SaveSettings.setValue('PiDuoigd',self.uic.PiDuoigd.value())
            SaveSettings.setValue('PiTrengd',self.uic.PiTrengd.value())
            SaveSettings.setValue('PiBuocgd',self.uic.PiBuocgd.value())
        else:
            SaveSettings.setValue('PiListgd',self.uic.PiListgd.text())
        SaveSettings.setValue('TipKompgd',self.uic.TipKompgd.currentIndex())
        SaveSettings.setValue('KPD_sentgd',self.uic.KPD_sentgd.value())
        SaveSettings.setValue('MHgd',self.uic.MHgd.text())
        SaveSettings.setValue('THgd',self.uic.THgd.text())
        SaveSettings.setValue('DeltaT_Komgd',self.uic.DeltaT_Komgd.text())
        SaveSettings.setValue('DeltaT_VozOxlgd',self.uic.DeltaT_VozOxlgd.text())
        SaveSettings.setValue('T_ctgd',self.uic.T_ctgd.text())
        SaveSettings.setValue('Sigma_vxgd',self.uic.Sigma_vxgd.text())
        SaveSettings.setValue('Sigma_komgd',self.uic.Sigma_komgd.text())
        SaveSettings.setValue('Sigma_ksgd',self.uic.Sigma_ksgd.text())
        SaveSettings.setValue('Fi_cgd',self.uic.Fi_cgd.text())
        SaveSettings.setValue('KPD_ksgd',self.uic.KPD_ksgd.text())
        SaveSettings.setValue('KPD_VnutTgd',self.uic.KPD_VnutTgd.text())
        SaveSettings.setValue('h0_crgd',self.uic.h0_crgd.text())
        SaveSettings.setValue('g_otb_gd',self.uic.g_otb_gd.text())
        SaveSettings.setValue('g_utech_gd',self.uic.g_utech_gd.text())
        SaveSettings.setValue('alpha_gd',self.uic.alpha_gd.text())
        SaveSettings.setValue('Negd',self.uic.Negd.text())
        SaveSettings.setValue('KPD_vnTVgd',self.uic.KPD_vnTVgd.text())
        SaveSettings.setValue('KPD_redukgd',self.uic.KPD_redukgd.text())
        SaveSettings.setValue('k_ispolgd',self.uic.k_ispolgd.text())
        SaveSettings.setValue('Xgd',self.uic.Xgd.text())

    def LoadSettingsFunc(self,fileName):
        self.LoadSettings = QSettings(fileName, QSettings.IniFormat) #Gắn biến LoadSettings với class Qsetting có đối số là file được nhập vào (ứng với đối số dòng lệnh =1, còn đối số dòng lệnh =0 là của file chạy ứng dụng)
        self.setWindowTitle("A2GTPyt - "+os.path.basename(fileName).rstrip('ptq').rstrip('.')) # THÊM TÊN FILE VÀO SAU TÊN CỬA SỔ CHÍNH KHI MỞ TỪ FILE
        self.uic.HoTengd.setText(self.LoadSettings.value('HoTengd'))
        self.uic.Nhomgd.setText(self.LoadSettings.value('Nhomgd'))
        self.radiostatusT3=float(self.LoadSettings.value('radiostatusT3')) #QQ Phải gắn lại giá trị này sau khi load dữ liệu từ file nếu không mặc định nó sẽ lấy giá trị ở lần chọn trước đó 
        #QQ giống như lúc mới KĐ lại phần mềm nó sẽ không nhận diện được giá trị lựa chọn ban đầu mà phải gắn vào. Tương tự với các đối tượng lựa chọn như combobox
        if self.radiostatusT3==0:
            self.uic.T3Duoigd.setValue(float(self.LoadSettings.value('T3Duoigd')))
            self.uic.T3Trengd.setValue(float(self.LoadSettings.value('T3Trengd')))
            self.uic.T3Buocgd.setValue(float(self.LoadSettings.value('T3Buocgd')))
        else:
            self.uic.T3Chon1gd.setChecked(False)
            self.uic.T3Chon2gd.setChecked(True)
            self.uic.T3Listgd.setEnabled(True)
            self.uic.T3Duoigd.setDisabled(True)
            self.uic.T3Trengd.setDisabled(True)
            self.uic.T3Buocgd.setDisabled(True)
            self.uic.T3Listgd.setText(self.LoadSettings.value('T3Listgd'))
        self.radiostatusPi=float(self.LoadSettings.value('radiostatusPi'))
        if self.radiostatusPi==0:
            self.uic.PiDuoigd.setValue(float(self.LoadSettings.value('PiDuoigd')))
            self.uic.PiTrengd.setValue(float(self.LoadSettings.value('PiTrengd')))
            self.uic.PiBuocgd.setValue(float(self.LoadSettings.value('PiBuocgd')))
        else:
            self.uic.PiChon1gd.setChecked(False)
            self.uic.PiChon2gd.setChecked(True)
            self.uic.PiListgd.setEnabled(True)
            self.uic.PiDuoigd.setDisabled(True)
            self.uic.PiTrengd.setDisabled(True)
            self.uic.PiBuocgd.setDisabled(True)
            self.uic.PiListgd.setText(self.LoadSettings.value('PiListgd'))
        self.TipKomp=int(self.LoadSettings.value('TipKompgd'))
        self.uic.TipKompgd.setCurrentIndex(self.TipKomp)

        if self.TipKomp==2:
            self.uic.KPD_sentgd.setEnabled(True)
            self.uic.KPD_sentgd.setValue(float(self.LoadSettings.value('KPD_sentgd')))
        else:
            pass
        self.uic.MHgd.setText(self.LoadSettings.value('MHgd'))
        self.uic.THgd.setText(self.LoadSettings.value('THgd'))
        self.uic.DeltaT_Komgd.setText(self.LoadSettings.value('DeltaT_Komgd'))
        self.uic.DeltaT_VozOxlgd.setText(self.LoadSettings.value('DeltaT_VozOxlgd'))
        self.uic.T_ctgd.setText(self.LoadSettings.value('T_ctgd'))
        self.uic.Sigma_vxgd.setText(self.LoadSettings.value('Sigma_vxgd'))
        self.uic.Sigma_komgd.setText(self.LoadSettings.value('Sigma_komgd'))
        self.uic.Sigma_ksgd.setText(self.LoadSettings.value('Sigma_ksgd'))
        self.uic.Fi_cgd.setText(self.LoadSettings.value('Fi_cgd'))
        self.uic.KPD_ksgd.setText(self.LoadSettings.value('KPD_ksgd'))
        self.uic.KPD_VnutTgd.setText(self.LoadSettings.value('KPD_VnutTgd'))
        self.uic.h0_crgd.setText(self.LoadSettings.value('h0_crgd'))
        self.uic.g_otb_gd.setText(self.LoadSettings.value('g_otb_gd'))
        self.uic.g_utech_gd.setText(self.LoadSettings.value('g_utech_gd'))
        self.uic.alpha_gd.setText(self.LoadSettings.value('alpha_gd'))
        self.uic.k_ispolgd.setText(self.LoadSettings.value('k_ispolgd'))
        self.uic.Negd.setText(self.LoadSettings.value('Negd'))
        self.uic.Xgd.setText(self.LoadSettings.value('Xgd'))
        self.uic.KPD_vnTVgd.setText(self.LoadSettings.value('KPD_vnTVgd'))
        self.uic.KPD_redukgd.setText(self.LoadSettings.value('KPD_redukgd'))

    def openFileNameDialog(self): #Tạo hộp thoại mở 1 file
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog #Dùng toán tử hợp '|' để hợp các đối tượng của QFileDialog.Options() và QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Окрыть файл расчета", "","All Files (*);;Config file (*.rsk)", options=options) #Dấu ', _' có nghĩa là bỏ qua các giá trị sau và chỉ gắn biến 
        #fileName cho giá trị đầu tiên của  QFileDialog.getOpenFileName().

        if fileName: #In câu lệnh fileName khi nó được thực thi -> do đó có thể thay thế biểu thức ở đây bằng thao tác khác
            if fileName.endswith(".rsk"):
                try:
                    self.ResetSettings() #Mục đích để trả về giá trị mặc định trước khi load dữ liệu mới để tránh chồng chéo
                    self.LoadSettingsFunc(fileName)
                    self.WorkFile=2
                    self.fileNameOpen=fileName
                except:
                    self.ResetSettings() #Reset lại các giá trị vì 1 số biến bị định nghĩa lại trong try dù có lỗi
                    MessageBox.FalseOpen()
            else:        
                MessageBox.InvalidFormat()
        else:
            pass

    def saveFileDialog(self): #Tạo hộp thoại save file
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog #DontUseNativeDialog là phương thức tùy chọn không hiển thị hộp thoại gốc (mặc định của win)
        #bởi vì với win cũ thì hộp thoại gốc không hiển thị các tệp, tuy nhiên hiện nay hỗ trợ do đó có thể không cần dùng đến tùy chọn này
        #nhưng có thể sử dụng nó để đơn giản hóa hộp thoại. Ngoài ra các phương thức tùy chọn ntn phải gọi ra trước khi thay đổi thuộc tính của hộp thoại như bên dưới
        fileName, _ = QFileDialog.getSaveFileName(self,"Сохранить файл расчета","Расчет.rsk","All Files (*);;Config file (*.rsk)", options=options)
        #Cài đặt lưu file gồm các đối số: qWidget (chính là self), Tiêu đề cửa sổ lưu, tên file mặc định, hiển thị tất cả các file + thiết lập thông số loại file lưu dạng *.rsk
        if fileName:
            if fileName.endswith(".rsk"):
                pass
            else:
                fileName=f'{fileName}.rsk'
            self.WorkFile=3
            self.fileNameSave=fileName
            self.SaveSettingsFunc(self.fileNameSave)
            MessageBox.MessageBoxSave()
        else:
            pass

    def T3ChonRadioButton(self): #Tạo phương thức cho trạng thái nút chọn quyết định sự thay đổi của các đối tượng
        radioButton = self.sender() #sender() dùng để gọi ra đối tượng của sự kiện, ở đây là nút radiobutton được gọi
        #radioButton sử dụng như biến cục bộ trong mỗi phương thức để tránh xung đột giữa các phương thức của các nhóm radiobutton
        if radioButton.isChecked(): #Nếu không chọn kiểu nhập T3 thứ nhất thì sẽ ẩn và reset tất cả giá trị của nó về 0.00 đồng thời cho phép nhập ở lựa chọn còn lại
            #self.uic.PiTrengd.setUpdatesEnabled(True) #Cập nhật lại giá trị của QSpinbox về 0.00 khi không dùng setDisabled và setEnabled
            self.uic.T3Trengd.setValue(0.00) #Cập nhật lại giá trị của QSpinbox về 0.00 khi dùng setDisabled và setEnabled
            self.uic.T3Trengd.setDisabled(True) #Vô hiệu nhập ô giá trị
            self.uic.T3Duoigd.setValue(0.00)
            self.uic.T3Duoigd.setDisabled(True)
            self.uic.T3Buocgd.setValue(0.00)
            self.uic.T3Buocgd.setDisabled(True)
            self.uic.T3Listgd.setEnabled(True)
            self.radiostatusT3=1
            #self.uic.PiTrengd.hide() #Lựa chọn ẩn hộp thoại
        if not radioButton.isChecked():
            #self.uic.PiTrengd.setUpdatesEnabled(True) #Cập nhật lại giá trị của QSpinbox về 0.00 khi không dùng setDisabled và setEnabled
            self.uic.T3Trengd.setEnabled(True) #Kích hoạt nhập ô giá trị
            self.uic.T3Duoigd.setEnabled(True)
            self.uic.T3Buocgd.setEnabled(True)
            self.uic.T3Listgd.setText('')
            self.uic.T3Listgd.setDisabled(True)
            self.radiostatusT3=0
            #self.uic.PiTrengd.show() #Lựa chọn hiện hộp thoại nếu bên trên chọn ẩn
    def PiChonRadioButton(self): #Tạo phương thức cho trạng thái nút chọn
        radioButton = self.sender()
        if radioButton.isChecked():
            #self.uic.PiTrengd.setUpdatesEnabled(True) #Cập nhật lại giá trị của QSpinbox về 0.00 khi không dùng setDisabled và setEnabled
            self.uic.PiTrengd.setValue(0.00) #Cập nhật lại giá trị của QSpinbox về 0.00 khi dùng setDisabled và setEnabled
            self.uic.PiTrengd.setDisabled(True) #Vô hiệu nhập ô giá trị
            self.uic.PiDuoigd.setValue(0.00)
            self.uic.PiDuoigd.setDisabled(True)
            self.uic.PiBuocgd.setValue(0.00)
            self.uic.PiBuocgd.setDisabled(True)
            self.uic.PiListgd.setEnabled(True)
            self.radiostatusPi=1
            #self.uic.PiTrengd.hide() #Lựa chọn ẩn hộp thoại
        if not radioButton.isChecked():
            #self.uic.PiTrengd.setUpdatesEnabled(True) #Cập nhật lại giá trị của QSpinbox về 0.00 khi không dùng setDisabled và setEnabled
            self.uic.PiTrengd.setEnabled(True) #Kích hoạt nhập ô giá trị
            self.uic.PiDuoigd.setEnabled(True)
            self.uic.PiBuocgd.setEnabled(True)
            self.uic.PiListgd.setText('')
            self.uic.PiListgd.setDisabled(True)
            self.radiostatusPi=0
            #self.uic.PiTrengd.show() #Lựa chọn hiện hộp thoại nếu bên trên chọn ẩn
    def TipKompBox(self): #Tạo phương thức cho trạng thái chọn loại máy nén
        ComboBox=self.uic.TipKompgd.currentIndex()
        if ComboBox==2:
            self.uic.KPD_sentgd.setEnabled(True)
            self.TipKomp=2
        else:
            self.uic.KPD_sentgd.setValue(0.00)
            self.uic.KPD_sentgd.setDisabled(True)
            if ComboBox==0:
                self.TipKomp=0
            else:
                self.TipKomp=1
    def closeEvent(self, event: QtGui.QCloseEvent): #Bộ bắt sự kiện => trường hợp này sẽ chạy tự động khi gọi sự kiện đóng. Sự kiện 
        #đóng là sự kiện mặc định được tích hợp trong QMainWindow mà không cần định nghĩa được gắn với dấu X của cửa sổ màn hình hay Alt+F4
        self.settingspos.setValue('window position', self.pos())
        event.ignore() #Hủy sự kiện
        DialogClose.DialogClose() #Hiện hộp thoại
    def event(self, event): #Tạo hàm nhận sự kiến nhấn nút enter hoặc các mũi tên lên xuống sẽ chuyển đến ô nhập tiếp theo
        #Các nút trái phải không hoạt động trong Qt một phần vì tab Order của Qt hoạt động theo dạng cột thứ tự từ trên xuống, một phần
        #vì các sự kiện nhấn Qt.Key_Left và Qt.Key_Right không bắt được.
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter) or event.key()==Qt.Key_Down:
                self.focusNextChild()
            elif event.key()==Qt.Key_Up:
                self.focusPreviousChild()
            elif event.key()==Qt.Key_Left:
                self.focusPreviousChild()
        return super().event(event)
    def ThermalCycle(self,T3_polnoe,Pi_polnoe,TipKomp,KPD_sent,MH,TH,DeltaT_Kom,DeltaT_VozOxl,T_ct,Sigma_vx,Sigma_kom,Sigma_ks,Fi_c,KPD_ks,KPD_VnutT,h0_cr,g_otb_,g_utech_,alpha_,k_ispol,Ne,X,KPD_vnTV,KPD_reduk,folderNameSelect,UserName,UserGroup):
        '''T3_polnoe,Pi_polnoe,TipKomp,KPD_sent,MH,TH,DeltaT_Kom,DeltaT_VozOxl,T_ct,Sigma_vx,Sigma_kom,Sigma_ks,Fi_c,KPD_ks,KPD_VnutT,h0_cr,g_otb_,g_utech_,alpha_,k_ispol,Ne,X,KPD_vnTV,KPD_reduk,
                folderNameSelect,UserName,UserGroup=self.T3_polnoe,self.Pi_polnoe,self.TipKomp,self.KPD_sent,self.MH,self.TH,self.DeltaT_Kom,self.DeltaT_VozOxl,
                self.T_ct,self.Sigma_vx,self.Sigma_kom,self.Sigma_ks,self.Fi_c,self.KPD_ks,self.KPD_VnutT,self.h0_cr,self.g_otb_,
                self.g_utech_,self.alpha_,self.k_ispol,self.Ne,self.X,self.KPD_vnTV,self.KPD_reduk,self.folderNameSelect,self.UserName,self.UserGroup'''
        self.SetProgr=10
        for T3_pol in T3_polnoe:

            #Tạo các danh sách rỗng để ghi các dữ liệu cột cho file csv ở cuối vòng lặp
            ColumnPik,ColumnT2pol,ColumnC_pmiB,ColumnTg,ColumnTq,ColumnT4a,ColumnT4q,ColumnC_pmig,ColumnT5t,ColumnP3naP5,ColumnHor,ColumnHog,Columnalpha=[],[],[],[],[],[],[],[],[],[],[],[],[]
            ColumnZ,Columnqoxl,ColumnPioxl,ColumnHoxl_,ColumnKAPq,ColumnKAPoxl,ColumnKPDad,Columnlcv,Columngoxl_,ColumnC5_,ColumnGv,ColumnGg,ColumnNeud,ColumnCe=[],[],[],[],[],[],[],[],[],[],[],[],[],[]

            #Vòng lặp lớn bên trong là theo sự thay đổi hệ số tăng áp 
            for Pik_pol in Pi_polnoe:
                #1) Температура торможения воздуха на входе в компрессор (Nhiệt độ hãm của KK tại đầu vào MN)
                k=1.4
                Pi_d=(1+(k-1)*0.5*MH**2)**((k-1)/k)
                T1_pol=TH*(Pi_d)**((k-1)/k)

                #2) Температура торможения воздуха на выходе из компрессора (Nhiệt độ hãm của KK tại đầu ra từ MN)
                R_B=0.287
                C_pmsB0=1.006
                m_sB0=R_B/C_pmsB0

                if TipKomp==0:
                    TipKom='однокаскадный осевой компрессор'
                    KPD_k_ad=0.906-0.004*Pik_pol
                elif TipKomp==1:
                    TipKom='двух/трехкаскадный осевой компрессор'
                    KPD_k_ad=0.87-0.01*(Pik_pol-11)/7
                else:
                    TipKom='центробежный компрессор           КПДцент = '+str(KPD_sent)
                    KPD_k_ad=KPD_sent

                T2_pol0=T1_pol+(T1_pol/KPD_k_ad)*((Pik_pol)**m_sB0-1)
                m_sB=R_B/C_pmsB(T1_pol,T2_pol0)
                T2_pol=T1_pol+(T1_pol/KPD_k_ad)*((Pik_pol)**m_sB-1)
                while abs(T2_pol-T2_pol0)/T2_pol>0.001:
                    T2_pol0=T2_pol
                    m_sB=R_B/C_pmsB(T1_pol,T2_pol0)
                    T2_pol=T1_pol+(T1_pol/KPD_k_ad)*((Pik_pol)**m_sB-1)
                
                #3) Коэффициент избытка воздуха (Hệ số dư lượng KK)
                QpH,L0=44300,15
                t3_pol=T3_pol-273.15
                t2_pol=T2_pol-273.15
                i_top=0
                alpha=(QpH*KPD_ks-(1+L0)*Cpmi_al1(t3_pol)*t3_pol+L0*CpmiB(t3_pol)*t3_pol+i_top)/(L0*(CpmiB(t3_pol)*t3_pol-CpmiB(t2_pol)*t2_pol))

                #4) Относительный расход топлива (LL tương đối so với LL không khí thực tế đi vào buồng đốt)
                g_top=1/(alpha*L0)
                
                #5) Теоретическая температура в конце процесса расширения за реактивным соплом (Nhiệt độ lý thuyết ở cuối quá trình giãn nở sau loa phun phản lực)
                C_pmsg0=1.159
                m_sg0=R_g(alpha,L0)/C_pmsg0
                P5_delit_P3_pol=1/(Sigma_vx*Pi_d*Pik_pol*Sigma_ks*Sigma_kom)
                T5t0=T3_pol*(P5_delit_P3_pol)**m_sg0
                m_sg=R_g(alpha,L0)/C_pmsg(T5t0,T3_pol,alpha,L0)
                T5t=T3_pol*(P5_delit_P3_pol)**m_sg
                while abs(T5t-T5t0)/T5t>0.001:
                    T5t0=T5t
                    m_sg=R_g(alpha,L0)/C_pmsg(T5t0,T3_pol,alpha,L0)
                    T5t=T3_pol*(P5_delit_P3_pol)**m_sg
                
                #6) Изоэнтропийный перепад энтальпий, вычисленный по параметрам торможения перед первой ступенью турбины и по параметрам в потоке в конце процесса расширения за реактивным соплом.
                #Tính độ giảm thế nhiệt động đẳng entropy
                H0r=C_pmig(T5t,T3_pol,alpha,L0)*(T3_pol-T5t)

                #8) Температура торможения газа Т_4а* на выходе из турбины без учета охлаждения. Nhiệt độ hãm của khí tại đầu ra tuabin không tính đến làm mát
                Sigma_vix=0.97
                Cpg=1.159
                m_sg=R_g(alpha,L0)/Cpg
                P4_pol_delit_PH_m_sg=1/((Sigma_vix)**m_sg)
                T4a_pol=T3_pol-KPD_VnutT*(T3_pol-T5t*P4_pol_delit_PH_m_sg)

                #VÒNG LẶP TÍNH GẦN ĐÚNG T4a_pol:
                T4q_pol=T4a_pol #QQ gắn các giá trị để các vòng lặp đầu tiên luôn chạy
                T4a_pol0=0
                T4q_pol0=0
                svl=1
                while abs(T4a_pol-T4a_pol0)/T4a_pol>0.001:
                    T4a_pol0=T4a_pol
                    if svl!=1:
                        T4q_pol=T4a_pol*(1-q_oxl/(C_pmig(T_ct,T3_pol,alpha,L0)*Tq)) #QQ Ở các vòng lặp khác 1 (svl!=1) cần hiệu chỉnh lại T4q_pol theo giá trị T4a_pol đã hiệu chỉnh trong CT (24) sau đó chạy vòng lặp trong hiệu chỉnh T4q_pol
                    else:
                        pass
                    #VÒNG LẶP TÍNH GẦN ĐÚNG T4q_pol:
                    while abs(T4q_pol-T4q_pol0)/T4q_pol>0.001: #QQ Nếu thỏa mãn điều kiện thì sẽ bỏ qua vòng lặp này vào chuyển sang phần sau của vòng lặp lớn để hiệu chỉnh T4a_pol
                        T4q_pol0=T4q_pol
                        #9) Количество охлаждаемых венцов (số lượng vành cánh có làm mát chứ không phải số cấp có làm mát hay số cánh có làm mát) 
                        if T_ct==T3_pol or T_ct>T3_pol:
                            Z=0
                        else:
                            if T_ct<T4q_pol0:
                                Z0=2*C_pmig(T4q_pol0,T3_pol,alpha,L0)*(T3_pol-T4q_pol0)/h0_cr
                            else:
                                Z0=2*C_pmig(T_ct,T3_pol,alpha,L0)*(T3_pol-T_ct)/h0_cr
                            Z=round(Z0)
                        if T_ct<T3_pol and Z==0:
                            Z=1
                        else:
                            pass
                        #10) Общее удельное количество теплоты - tổng nhiệt lượng tỏa ra từ các thành phần có làm mát cho lượng công chất làm mát thực tế tham gia trao đổi nhiệt trên 1kg lưu lượng khí công tác trong các vành cánh có làm mát của PLT tuabin 
                        if Z==0:
                            q_oxl=0
                        elif T4q_pol0<T_ct:
                            a=1-(Z-1)*(T3_pol-T_ct)/(2*Z*(T3_pol-T_ct))
                            q_oxl=alpha_*C_pmig(T_ct,T3_pol,alpha,L0)*a*(T3_pol-T_ct)*Z
                        else:
                            a=1-(Z-1)*(T3_pol-T4q_pol0)/(2*Z*(T3_pol-T_ct))
                            q_oxl=alpha_*C_pmig(T_ct,T3_pol,alpha,L0)*a*(T3_pol-T_ct)*Z

                        #11) Температура охладителя (Nhiệt độ công chất làm mát)
                        Tv_pol=T2_pol
                        if Z==0:
                            T_oxl_pol=Tv_pol+0-DeltaT_VozOxl #DeltaT_Kom=0 khi số vành làm mát =0, nhưng vì nó thuộc điều kiện đầu bài nên không được gán biến ở đây sẽ làm thay đổi điều kiện trong các trường hợp khác
                        else:
                            T_oxl_pol=Tv_pol+DeltaT_Kom-DeltaT_VozOxl
                        #12) Относительный расход охладителя на охлаждение элементов проточной части газовой турбины 
                        #LL tương đối của công chất làm mát đến làm mát các TP của PLT tuabin khí\
                        C_pmioxl_Toxl_Tct=C_pmiB(T_oxl_pol,T_ct)
                        g_oxl_lop=q_oxl/(k_ispol*C_pmioxl_Toxl_Tct*(T_ct-T_oxl_pol))
                        
                        #13) Общий относительный расход охладителя. Tổn LL tương đối của công chất làm mát (so với LL không khí)
                        #Đặt B=goxl_p'+goxl_c'=A.(T3_pol-T_ct)/T3_pol. A=0,04...0,06
                        A=0.05
                        if Z==0:
                            B=0
                        else:
                            B=A*(T3_pol-T_ct)/T3_pol
                        g_oxl_=(g_oxl_lop*(1-g_otb_-g_utech_)*(1+g_top)+B)/(1+g_oxl_lop*(1+g_top))
                        
                        #14) Иэоэнтропийный перепад энтальпий на турбине генератора свободной энергии по параметрам торможения определяется по уравнений.
                        #Độ giảm eltanpy đẳng entropy trên tuabin sinh NL tự do theo các thông số dòng hãm
                        KPD_km=0.99
                        KPD_tm=0.99
                        alphaQ=1.03
                        KPD_t_eff=KPD_VnutT*KPD_tm#n*t эффективный КПД турбины
                        KPD_k=KPD_k_ad*KPD_km
                        m_sB=R_B/C_pmsB(T1_pol,T2_pol)
                        Xi=1-g_otb_-g_utech_-g_oxl_
                        H0g_pol=C_pmiB(T1_pol,T2_pol)*T1_pol*(Pik_pol**m_sB-1)/(KPD_k*KPD_t_eff*alphaQ*Xi*(1+g_top))
                            
                        #15) Средняя температура газа, при которой отводится теплота охлаждения. Nnhiệt độ trung bình của khí mà khi đó nhiệt lượng tỏa ra làm mát, có nghĩa là nhiệt lượng trước khi tỏa nhiệt cho vành làm mát
                        if Z==0:
                            Tq=T3_pol
                        elif T4q_pol0<T_ct:
                            a=1-(Z-1)*(T3_pol-T_ct)/(2*Z*(T3_pol-T_ct))
                            b=(1-a)*(1-(T3_pol-T_ct)*(Z+1)/(3*a*2*Z*(T3_pol-T_ct)))
                            Tq=T3_pol*(1-b*(T3_pol-T_ct)/T3_pol)
                        else:
                            a=1-(Z-1)*(T3_pol-T4q_pol0)/(2*Z*(T3_pol-T_ct))
                            b=(1-a)*(1-(T3_pol-T4q_pol0)*(Z+1)/(3*a*2*Z*(T3_pol-T_ct)))
                            Tq=T3_pol*(1-b*(T3_pol-T_ct)/T3_pol)

                        #16) Температура конца процесса расширения в турбине с охлаждением. Nhiệt độ cuối quá trình giãn nở trong tuabin có làm mát 
                        T4q_pol=T4a_pol0*(1-q_oxl/(C_pmig(T_ct,T3_pol,alpha,L0)*Tq))

                        #После определения T4q_pol необходимо вернуться к уточнению Z, q_охл, g_охл^лоп, g_охл^', Т_q.
                    
                    #17) Средняя температура газа, при которой охладитель вводится в проточную часть [3] (Nhiệt độ trung bình của khí khi công chất làm mát đi vào phần lưu thông và hòa trộn với phần khí tỏa nhiệt làm mát):
                    if Z==0:
                        Tg=Tq
                    elif T_ct<T4q_pol:
                        Tg=Tq-(T3_pol-T4q_pol)/Z
                    else:
                        Tg=Tq-(T3_pol-T_ct)/Z

                    #18) Степень расширения охладителя в турбине и реактивном сопле
                    KPD_T_poli=KPD_t_eff
                    m_sg_=R_g(alpha,L0)*KPD_T_poli/C_pmsg(Tg,T3_pol,alpha,L0)
                    Pi_oxl=(1/P5_delit_P3_pol)*((T3_pol/Tg)*(1-q_oxl/(C_pmig(T_ct,T3_pol,alpha,L0)*Tq)))**(-1/m_sg_)

                    #19) Коэффициент, характеризующий относительную потерю полезной работы вследствие охлаждения
                    if Z==0:
                        Xq=1
                    else:
                        Xq=1-T4a_pol0/Tq

                    #20) Коэффициент, характеризующий увеличение работы расширения охладителя за счет подвода теплоты системы охлаждения 
                    R_oxl=R_B
                    KPD_oxl_poli=KPD_t_eff
                    C_pmsoxl_T5t_Toxl=C_pmsB(T5t,T_oxl_pol)
                    if Z==0:
                        X_oxl=1
                    else:
                        m_soxl_=R_oxl*KPD_oxl_poli/(C_pmsoxl_T5t_Toxl)
                        X_oxl=1-Pi_oxl**(-m_soxl_)

                    #21) Работа расширения охладителя, определенная без учета его подогрева за счет теплоты 
                    m_soxl_=R_oxl*KPD_oxl_poli/(C_pmsoxl_T5t_Toxl)
                    g_oxl=g_oxl_/(Xi*(1+g_top))
                    C_pmioxl_T5t_Toxl=C_pmiB(T5t,T_oxl_pol)
                    H_oxl_=g_oxl*C_pmioxl_T5t_Toxl*T_oxl_pol*(1-(Pi_oxl**(-m_soxl_)))

                    #22) Удельная свободная энергия, отнесенная к расходу рабочего тела G_г. Năng lượng tự do riêng tỉ lệ với lưu lượng khí công tác tại đầu vào cấp thứ nhất của tuabin tự do
                    #Tính năng lượng tự do riêng so với LL khí công tác
                    l_sv=alphaQ*H0r+H_oxl_-(Xq-X_oxl)*q_oxl-H0g_pol

                    #23) Удельная свободная энергия, отнесенная к расходу воздуха на входе в компрессор Gв
                    #Tính năng lượng tự do riêng so với LL không khí
                    l_sv_=Xi*(1+g_top)*l_sv

                    #QQ Уточнение температуре газа за турбиной без учета охлаждения. Hiệu chỉnh T4a_pol trong phần đầu tính toán dành cho TVaD 
                    T4a_pol=T3_pol-(H0g_pol*KPD_VnutT+l_sv_*X*KPD_vnTV)/(C_pmig(T4a_pol0,T3_pol,alpha,L0))
                    svl+=1
                    T4q_pol0=T4q_pol #QQ định nghĩa lại giá trị T4q_pol0 để dùng khi chạy lại vòng lặp
                    
                #QQ TÍNH TOÁN CÁC THÔNG SỐ ĐẦU RA CỦA TVD HOẶC TVaD (CT từ 49-54)
                #Удельная эффективная мощность
                Ne_ud=X*l_sv_*KPD_vnTV*KPD_tm*KPD_reduk

                #Расход воздуха
                Gv=Ne/Ne_ud

                #Расход газа на входе в первую ступень турбины
                Gg=Gv*Xi*(1+g_top)

                #Расход топлива
                G_top=g_top*Gg

                #Удельный расход топлива по эффективной мощности
                Ce=3600*G_top/Ne

                #Скорость выхода потока газов из реактивного сопла
                C5=Fi_c*math.sqrt(2*(1-X)*l_sv_*1000)#Chuyển đơn vị l_sv sang J
                
                #Danh sách các tên cột ['ПИК','Т2*','С_рмив','Тg','Tq','Т4а*','Т4q*','С_рмиг','Т5t','Р3*/Р5','Нор','Ног*','АЛЬФА','Z','q_охл','ПИ_охл','Н\'_охл','КАП_q','КАП_охл','КПДАД','l\'_св','g\'_ охл','С5','Gв','Gг','Nеуд','Се']

                ColumnPik.append(Pik_pol)
                ColumnT2pol.append(round(T2_pol,1))
                ColumnC_pmiB.append(round(C_pmiB(T1_pol,T2_pol),4))
                ColumnTg.append(round(Tg,1))
                ColumnTq.append(round(Tq,1))
                ColumnT4a.append(round(T4a_pol,1))
                ColumnT4q.append(round(T4q_pol,1))
                ColumnC_pmig.append(round(C_pmig(T4q_pol,T3_pol,alpha,L0),4))
                ColumnT5t.append(round(T5t,1))
                ColumnP3naP5.append(round(1/P5_delit_P3_pol,2))
                ColumnHor.append(round(H0r,2))
                ColumnHog.append(round(H0g_pol,2))
                Columnalpha.append(round(alpha,2))
                ColumnZ.append(Z)
                Columnqoxl.append(round(q_oxl,2))
                ColumnPioxl.append(round(Pi_oxl,1))
                ColumnHoxl_.append(round(H_oxl_,2))
                ColumnKAPq.append(round(Xq,2))
                ColumnKAPoxl.append(round(X_oxl,2))
                ColumnKPDad.append(round(KPD_k_ad,3))
                Columnlcv.append(round(l_sv_,2))
                Columngoxl_.append(round(g_oxl_*100,1))
                ColumnC5_.append(round(C5,1))
                ColumnGv.append(round(Gv,2))
                ColumnGg.append(round(Gg,2))
                ColumnNeud.append(round(Ne_ud,2))
                ColumnCe.append(round(Ce,4))

            #GẮN GIÁ TRỊ ỨNG VỚI CÁC CỘT THÔNG SỐ

            RezultatT3df=pd.DataFrame()
            RezultatT3df['ПИК']=ColumnPik
            RezultatT3df['Т2*']=ColumnT2pol
            RezultatT3df['С_рмив']=ColumnC_pmiB
            RezultatT3df['Тg']=ColumnTg
            RezultatT3df['Tq']=ColumnTq
            RezultatT3df['Т4а*']=ColumnT4a
            RezultatT3df['Т4q*']=ColumnT4q
            RezultatT3df['С_рмиг']=ColumnC_pmig
            RezultatT3df['T5t']=ColumnT5t
            RezultatT3df['Р3*/Р5']=ColumnP3naP5
            RezultatT3df['Нор']=ColumnHor
            RezultatT3df['Ног*']=ColumnHog
            RezultatT3df['АЛЬФА']=Columnalpha
            RezultatT3df['Z']=ColumnZ
            RezultatT3df['q_охл']=Columnqoxl
            RezultatT3df['ПИ_охл']=ColumnPioxl
            RezultatT3df['Н\'_охл']=ColumnHoxl_
            RezultatT3df['КАП_q']=ColumnKAPq
            RezultatT3df['КАП_охл']=ColumnKAPoxl
            RezultatT3df['КПДАД']=ColumnKPDad
            RezultatT3df['l\'_св']=Columnlcv
            RezultatT3df['g\'_ охл']=Columngoxl_
            RezultatT3df['С5']=ColumnC5_
            RezultatT3df['Gв']=ColumnGv
            RezultatT3df['Gг']=ColumnGg
            RezultatT3df['Nеуд']=ColumnNeud
            RezultatT3df['Се']=ColumnCe

            self.ColumnNeudlist+=(ColumnNeud,)
            self.ColumnCelist+=(ColumnCe,)

            #XUẤT KẾT QUẢ RA FILE CSV CHO MỖI GIÁ TRỊ T3  
            if folderNameSelect!='NotSelect':
                result='Result'+str(T3_pol)+'K.csv'
                RezultatT3df.to_csv(folderNameSelect+'\\'+result,sep='\t',index=False)            
                InFileResult(T3_pol,Pi_polnoe,MH,Sigma_vx,KPD_VnutT,k_ispol,TH,Sigma_kom,h0_cr,Ne,DeltaT_Kom,Sigma_ks,g_otb_,X,DeltaT_VozOxl,Fi_c,g_utech_,
                    KPD_vnTV,T_ct,KPD_ks,alpha_,KPD_reduk,ColumnPik,ColumnT2pol,ColumnC_pmiB,ColumnTg,ColumnTq,ColumnT4a,ColumnT4q,ColumnC_pmig,ColumnT5t,
                    ColumnP3naP5,ColumnHor,ColumnHog,Columnalpha,ColumnZ,Columnqoxl,ColumnPioxl,ColumnHoxl_,ColumnKAPq,ColumnKAPoxl,ColumnKPDad,Columnlcv,
                    Columngoxl_,ColumnC5_,ColumnGv,ColumnGg,ColumnNeud,ColumnCe,TipKom,UserName,UserGroup,folderNameSelect)
            else:
                pass
            self.SetProgr+=5
            self.uic.progressBar.setValue(self.SetProgr)
        self.uic.progressBar.setValue(self.SetProgr+5)

A2GTEPyth = QtWidgets.QMainWindow()
main_win = MainWindow()
main_win.show()
try:
    sys.exit(app.exec_())
except:
    pass

#if __name__ == "__main__":
    
    #Gọi ra tất cả đối số dòng lệnh mà class QApplicationcation truyền cho file python đang chạy.
    #main_win = MainWindow() #Gắn biến chạy class MainWindow đã khởi tạo ở trên trùng với 1 thuộc tính của nó (ko bắt buộc chẳng qua nó cùng nghĩa nên đặt vậy)
    #main_win.show() #Hiển thị biến main_win cũng chính là class MainWindow với các đối số ban đầu được khai báo trong file giao diện và các sự kiện cùng kết quả

    #sys.exit(app.exec_()) 
    #Dừng ứng dụng khi app.exec_() có giá trị tức là phương thức .exec_() trả ra 1 giá trị khi có ngoại lệ là lệnh thoát (giá trị là 0
    #nghĩa là dừng bình thường) hoặc lỗi (các giá trị khác), nếu không thì các đối số dòng lệnh trong app sẽ luôn nằm trong vòng lặp đặt trong 'try' cho đến khi
    #nào chưa xuất hiện ngoại lệ (chuyển sang except).
    #Câu lệnh này cũng giúp định nghĩa lại thao tác thoát phần mềm của hệ thống (system) chỉ thực hiện khi có ngoại lệ (bấm tắt hoặc lỗi)
    #Nếu không có nó thì giao diện chỉ nháy lên rồi tắt vì không có 1 chức năng được định nghĩa để kiểm soát nó