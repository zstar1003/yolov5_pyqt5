import os
import sys
import detect
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox

import detect_video


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_detect = QtCore.QTimer()
        self.setupUi(self)
        self.init_logo()  # 初始化logo
        self.init_slots()  # 初始化槽函数
        # 初始化属性
        self.file_path = None
        self.model_path = None
        self.result_path = "result"


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)  # 布局的左、上、右、下到窗体边缘的距离
        self.verticalLayout.setObjectName("verticalLayout")

        # 打开图片按钮
        self.pushButton_img = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_img.sizePolicy().hasHeightForWidth())
        self.pushButton_img.setSizePolicy(sizePolicy)
        self.pushButton_img.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_img.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.pushButton_img.setFont(font)
        self.pushButton_img.setObjectName("pushButton_img")
        self.verticalLayout.addWidget(self.pushButton_img, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)  # 增加垂直盒子内部对象间距

        # 加载模型按钮
        self.pushButton_model = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_model.sizePolicy().hasHeightForWidth())
        self.pushButton_model.setSizePolicy(sizePolicy)
        self.pushButton_model.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_model.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_model.setFont(font)
        self.pushButton_model.setObjectName("pushButton_model")
        self.verticalLayout.addWidget(self.pushButton_model, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)

        # 检测按钮
        self.pushButton_detect = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_detect.sizePolicy().hasHeightForWidth())
        self.pushButton_detect.setSizePolicy(sizePolicy)
        self.pushButton_detect.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_detect.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_detect.setFont(font)
        self.pushButton_detect.setObjectName("pushButton_detect")
        self.verticalLayout.addWidget(self.pushButton_detect, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)

        # 视频检测按钮
        self.pushButton_video_detect = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_video_detect.sizePolicy().hasHeightForWidth())
        self.pushButton_video_detect.setSizePolicy(sizePolicy)
        self.pushButton_video_detect.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_video_detect.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_video_detect.setFont(font)
        self.pushButton_video_detect.setObjectName("pushButton_video_detect")
        self.verticalLayout.addWidget(self.pushButton_video_detect, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(50)

        # 显示导出文件夹按钮
        self.pushButton_showdir = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_showdir.sizePolicy().hasHeightForWidth())
        self.pushButton_showdir.setSizePolicy(sizePolicy)
        self.pushButton_showdir.setMinimumSize(QtCore.QSize(150, 50))
        self.pushButton_showdir.setMaximumSize(QtCore.QSize(150, 50))
        self.pushButton_showdir.setFont(font)
        self.pushButton_showdir.setObjectName("pushButton_showdir")
        self.verticalLayout.addWidget(self.pushButton_showdir, 0, QtCore.Qt.AlignHCenter)

        # 右侧图片填充区域
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.label.setStyleSheet("border: 1px solid white;")  # 添加显示区域边框

        # 底部美化导航条
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YOLOv5目标检测系统"))
        self.pushButton_img.setText(_translate("MainWindow", "选择图片"))
        self.pushButton_model.setText(_translate("MainWindow", "选择模型"))
        self.pushButton_detect.setText(_translate("MainWindow", "目标检测"))
        self.pushButton_video_detect.setText(_translate("MainWindow", "视频检测"))
        self.pushButton_showdir.setText(_translate("MainWindow", "打开输出文件夹"))
        self.label.setText(_translate("MainWindow", "TextLabel"))

    def init_slots(self):
        self.pushButton_img.clicked.connect(self.load_img)
        self.pushButton_model.clicked.connect(self.select_model)
        self.pushButton_detect.clicked.connect(self.target_detect)
        self.pushButton_showdir.clicked.connect(self.show_dir)
        self.pushButton_video_detect.clicked.connect(self.video_detect)

    def init_logo(self):
        pix = QtGui.QPixmap('')  # 绘制初始化图片
        self.label.setScaledContents(True)
        self.label.setPixmap(pix)

    def load_img(self):
        print('打开图片')
        img_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "打开图片", "img", "All Files(*)")
        print(img_path)
        self.file_path = img_path
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
        self.label.setPixmap(pixmap)
        self.pushButton_img.setText(self.file_path.split('/')[-1])
        # 清空result文件夹内容
        for i in os.listdir(self.result_path):
            file_data = self.result_path + "/" + i
            os.remove(file_data)

    # 选择模型
    def select_model(self):
        model_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择模型", "weights", "Model files(*.pt)")
        self.model_path = model_path
        self.pushButton_model.setText(self.model_path[0].split('/')[-1])

    # 目标检测
    def target_detect(self):
        detect_size = 640
        if self.check_file():
            # 点击之后防止误触，禁用按钮
            self.pushButton_img.setEnabled(False)
            self.pushButton_model.setEnabled(False)
            self.pushButton_detect.setEnabled(False)
            self.thread = DetectionThread(self.file_path, self.model_path, detect_size)
            self.thread.start()
            # 子线程运行结束之后signal_done，主线程执行UI更新操作
            self.thread.signal_done.connect(self.flash_target)

    # 目标检测之前检查是否选择了数据和模型
    def check_file(self):
        if self.file_path is None:
            QMessageBox.information(self, '提示', '请先导入数据')
            return False
        if self.model_path is None:
            QMessageBox.information(self, '提示', '请先选择模型')
            return False
        return True

    # 刷新
    def flash_target(self):
        img_path = os.getcwd() + '/result/' + [f for f in os.listdir('result')][0]
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
        self.label.setPixmap(pixmap)
        # 刷新完之后恢复按钮状态
        self.pushButton_img.setEnabled(True)
        self.pushButton_model.setEnabled(True)
        self.pushButton_detect.setEnabled(True)

    # 显示输出文件夹
    def show_dir(self):
        path = os.getcwd() + '/' + 'result'
        os.system(f"start explorer {path}")

    # 检测视频
    def video_detect(self):
        print('打开视频')
        # print(self.label.size())  # (657, 554)
        video_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "打开视频", "video", "All Files(*)")
        self.Video_thread = VideoDetectionThread(self.label, video_path)
        self.Video_thread.start()


# DetectionThread子线程用来执行目标检测
class DetectionThread(QThread):
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self, file_path, model_path, detect_size):
        super(DetectionThread, self).__init__()
        self.file_path = file_path
        self.model_path = model_path
        self.detect_size = detect_size
        self.process = 0
        self.total = 0

    def run(self):
        # 目标检测
        detect.run(source=self.file_path, weights=self.model_path[0],
                   imgsz=(self.detect_size, self.detect_size))
        self.signal_done.emit(1)  # 发送结束信号


# DetectionThread子线程用来执行目标检测
class VideoDetectionThread(QThread):
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self, label, video_path):
        super(VideoDetectionThread, self).__init__()
        self.label = label
        self.video_path = video_path

    def run(self):
        # 目标检测
        detect_video.run(weights='weights/best.pt', source=self.video_path, show_label=self.label)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ui = Ui_MainWindow()
    # 设置窗口透明度
    # ui.setWindowOpacity(0.93)
    # 去除顶部边框
    # ui.setWindowFlags(Qt.FramelessWindowHint)
    # 设置窗口图标
    icon = QIcon()
    icon.addPixmap(QPixmap("./UI/icon.ico"), QIcon.Normal, QIcon.Off)
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())
