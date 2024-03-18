import os
import sys
import cv2
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox
import detect
import test_Fusion
from utils.myutil import file_is_pic, Globals


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_detect = QtCore.QTimer()
        self.radioButtons = []
        self.setupUi(self)
        self.init_logo()  # 初始化logo
        self.init_slots()  # 初始化槽函数
        self.file_path = None  # 数据路径
        self.model_path = None  # 模型路径
        self.file_suffix = None  # 文件后缀
        self.result_path = "result"  # 检测图片保存路径
        self.init_file()  # 初始化必要的文件夹


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

        # 导入图片按钮
        self.pushButton_img = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_img.sizePolicy().hasHeightForWidth())
        self.pushButton_img.setSizePolicy(sizePolicy)
        self.pushButton_img.setMinimumSize(QtCore.QSize(250, 80))
        self.pushButton_img.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        self.pushButton_img.setFont(font)
        self.pushButton_img.setObjectName("pushButton_img")
        self.verticalLayout.addWidget(self.pushButton_img, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(1)  # 增加垂直盒子内部对象间距

        # 导入图片按钮2
        self.pushButton_img2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_img2.sizePolicy().hasHeightForWidth())
        self.pushButton_img2.setSizePolicy(sizePolicy)
        self.pushButton_img2.setMinimumSize(QtCore.QSize(250, 80))
        self.pushButton_img2.setMaximumSize(QtCore.QSize(250, 80))
        self.pushButton_img2.setFont(font)
        self.pushButton_img2.setObjectName("pushButton_img2")
        self.verticalLayout.addWidget(self.pushButton_img2, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(1)  # 增加垂直盒子内部对象间距

        # 加载模型按钮
        self.pushButton_model = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_model.sizePolicy().hasHeightForWidth())
        self.pushButton_model.setSizePolicy(sizePolicy)
        self.pushButton_model.setMinimumSize(QtCore.QSize(250, 80))
        self.pushButton_model.setMaximumSize(QtCore.QSize(250, 80))
        self.pushButton_model.setFont(font)
        self.pushButton_model.setObjectName("pushButton_model")
        self.verticalLayout.addWidget(self.pushButton_model, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(1)

        # 融合按钮
        self.pushButton_merge = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_merge.sizePolicy().hasHeightForWidth())
        self.pushButton_merge.setSizePolicy(sizePolicy)
        self.pushButton_merge.setMinimumSize(QtCore.QSize(250, 80))
        self.pushButton_merge.setMaximumSize(QtCore.QSize(250, 80))
        self.pushButton_merge.setFont(font)
        self.pushButton_merge.setObjectName("pushButton_merge")
        self.verticalLayout.addWidget(self.pushButton_merge, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(1)

        # 检测按钮
        self.pushButton_detect = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_detect.sizePolicy().hasHeightForWidth())
        self.pushButton_detect.setSizePolicy(sizePolicy)
        self.pushButton_detect.setMinimumSize(QtCore.QSize(250, 80))
        self.pushButton_detect.setMaximumSize(QtCore.QSize(250, 80))
        self.pushButton_detect.setFont(font)
        self.pushButton_detect.setObjectName("pushButton_detect")
        self.verticalLayout.addWidget(self.pushButton_detect, 0, QtCore.Qt.AlignHCenter)

        # 切换按钮区域的布局
        self.toggleButtonLayout = QtWidgets.QGridLayout()
        # 定义按钮文本
        button_texts = ["可见光图像", "红外图像", "融合图像", "可见光检测", "红外检测", "融合检测"]
        # 创建六个小圆点切换按钮 (一列六行)，每个旁边有文字标记
        for i, text in enumerate(button_texts):
            # 创建单选按钮，并设置文本
            radioButton = QtWidgets.QRadioButton(text, self.centralwidget)
            self.radioButtons.append(radioButton)  # 添加到列
            # 应用样式表调整大小和增加padding
            radioButton.setStyleSheet("""
                 QRadioButton {
                     font-size: 20px; /* 调整字体大小 */
                     min-height: 50px; /* 最小高度 */
                     min-width: 120px; /* 最小宽度，包括文字和按钮 */
                     padding: 10px; /* 内边距 */
                     padding-left: 10px; /* 增加左边距以增强视觉效果 */
                     padding-right: 10px; /* 增加右边距以增强视觉效果 */
                 }
                 QRadioButton::indicator {
                     width: 20px; /* 单选按钮的圆点大小 */
                     height: 20px;
                 }
             """)
            # 将单选按钮添加到布局中，位置计算为：行 = i, 列 = 0
            if i > 1:
                radioButton.setEnabled(False)  # 禁用索引大于1的按钮
            self.toggleButtonLayout.addWidget(radioButton, i, 0, 1, 1, QtCore.Qt.AlignHCenter)

        # 为了使按钮组居中，我们在按钮组上方和下方添加拉伸因子
        self.toggleButtonLayout.setRowStretch(0, 1)  # 在第一行之前添加一个拉伸因子
        self.toggleButtonLayout.setRowStretch(len(button_texts) + 1, 1)  # 在最后一行之后添加一个拉伸因子
        # 将切换按钮区域的布局添加到verticalLayout中
        self.verticalLayout.addLayout(self.toggleButtonLayout)
        self.verticalLayout.addStretch(5)

        # 创建按钮水平布局
        self.buttonHorizontalLayout = QtWidgets.QHBoxLayout()
        # 设置水平布局的内边距
        self.buttonHorizontalLayout.setContentsMargins(35, 0, 35, 0)  # 左上右下
        # 设置布局中元素之间的间距
        self.buttonHorizontalLayout.setSpacing(0)  # 设置按钮之间的间距
        # 显示上一张按钮
        self.pushButton_up = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_up.sizePolicy().hasHeightForWidth())
        self.pushButton_up.setSizePolicy(sizePolicy)
        self.pushButton_up.setMinimumSize(QtCore.QSize(125, 80))
        self.pushButton_up.setMaximumSize(QtCore.QSize(125, 80))
        self.pushButton_up.setFont(font)
        # self.buttonHorizontalLayout.addWidget(self.pushButton_up, 0, QtCore.Qt.AlignHCenter)
        self.buttonHorizontalLayout.addWidget(self.pushButton_up)
        # 显示下一张按钮
        self.pushButton_down = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_down.sizePolicy().hasHeightForWidth())
        self.pushButton_down.setSizePolicy(sizePolicy)
        self.pushButton_down.setMinimumSize(QtCore.QSize(125, 80))
        self.pushButton_down.setMaximumSize(QtCore.QSize(125, 80))
        self.pushButton_down.setFont(font)
        self.buttonHorizontalLayout.addWidget(self.pushButton_down)
        self.verticalLayout.addLayout(self.buttonHorizontalLayout)

        # 显示导出文件夹按钮
        self.pushButton_showdir = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_showdir.sizePolicy().hasHeightForWidth())
        self.pushButton_showdir.setSizePolicy(sizePolicy)
        self.pushButton_showdir.setMinimumSize(QtCore.QSize(250, 80))
        self.pushButton_showdir.setMaximumSize(QtCore.QSize(250, 80))
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
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.label.setStyleSheet("border: 1px solid white;")  # 添加显示区域边框
        self.label.setScaledContents(True)
        self.label.setMinimumSize(QSize(1571, 963))
        self.label.setMaximumSize(QSize(1571, 963))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "RayNet图像融合检测系统"))
        self.pushButton_img.setText(_translate("MainWindow", "加载可见光图像"))
        self.pushButton_img2.setText(_translate("MainWindow", "加载红外图像"))
        self.pushButton_model.setText(_translate("MainWindow", "选择模型"))
        self.pushButton_merge.setText(_translate("MainWindow", "图像融合"))
        self.pushButton_detect.setText(_translate("MainWindow", "目标检测"))
        self.pushButton_up.setText(_translate("MainWindow", "上一张"))
        self.pushButton_down.setText(_translate("MainWindow", "下一张"))
        self.pushButton_showdir.setText(_translate("MainWindow", "打开输出文件夹"))
        self.label.setText(_translate("MainWindow", "TextLabel"))

    # 初始化槽函数
    def init_slots(self):
        self.pushButton_img.clicked.connect(self.load_source)
        self.pushButton_img2.clicked.connect(self.load_source)
        self.pushButton_model.clicked.connect(self.select_model)
        self.pushButton_detect.clicked.connect(self.target_detect)
        self.pushButton_showdir.clicked.connect(self.show_dir)
        self.pushButton_merge.clicked.connect(self.merge_enable)
        # 绑定QRadioButton的信号
        for radioButton in self.radioButtons:
            radioButton.toggled.connect(self.update_image_display)

    # 绘制LOGO
    def init_logo(self):
        pix = QtGui.QPixmap('')
        self.label.setScaledContents(True)
        self.label.setPixmap(pix)

    # 初始化创建保存文件夹
    def init_file(self):
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)

    # 加载图片
    def load_source(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "加载数据", "data", "All Files(*)")
        self.suffix = self.file_path.split(".")[-1]  # 读取后缀
        pixmap = QPixmap(self.file_path)
        pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
        self.label.setPixmap(pixmap)
        if self.file_path != "":
            self.pushButton_img.setText(self.file_path.split('/')[-1])
        # 清空result文件夹内容
        for i in os.listdir(self.result_path):
            file_data = self.result_path + "/" + i
            os.remove(file_data)

    # 选择模型
    def select_model(self):
        model_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择模型", "weights", "Model files(*.pt)")
        self.model_path = model_path
        if model_path[0] != "":
            self.pushButton_model.setText(self.model_path[0].split('/')[-1])

    # 目标检测
    # def target_detect(self):
    #     if self.check_file():
    #         # 点击之后防止误触，禁用按钮
    #         self.pushButton_img.setEnabled(False)
    #         self.pushButton_model.setEnabled(False)
    #         self.pushButton_detect.setEnabled(False)
    #         self.thread = DetectionThread(self.file_path, self.model_path, self.label)
    #         self.thread.start()
    #         # 子线程运行结束之后signal_done，主线程执行UI更新操作
    #         self.thread.signal_done.connect(self.flash_target)

    def update_image_display(self):
        if not self.file_path:
            return
        base_path, ext = os.path.splitext(self.file_path)
        # 检查哪个按钮被选中，并更新label显示对应的图片
        # 红外图像选中
        if self.radioButtons[1].isChecked():
            self.label.clear()
            infrared_path = f"{base_path}_inf{ext}"
            if os.path.exists(infrared_path):
                pixmap = QPixmap(infrared_path)
                scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled_pixmap)
            else:
                QMessageBox.warning(self, '警告', f'红外图像不存在: {infrared_path}')
        # 融合图像
        elif self.radioButtons[2].isChecked():
            self.label.clear()
            infrared_path = f"{base_path}_merge{ext}"
            if os.path.exists(infrared_path):
                pixmap = QPixmap(infrared_path)
                scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled_pixmap)
            else:
                QMessageBox.warning(self, '警告', f'融合图像不存在: {infrared_path}')
        # 可见光检测
        elif self.radioButtons[3].isChecked():
            self.label.clear()
            infrared_path = f"{base_path}_detect{ext}"
            if os.path.exists(infrared_path):
                pixmap = QPixmap(infrared_path)
                self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio))
            else:
                QMessageBox.warning(self, '警告', f'可见光检测图像不存在: {infrared_path}')
        # 红外检测
        elif self.radioButtons[4].isChecked():
            self.label.clear()
            infrared_path = f"{base_path}_inf_detect{ext}"
            if os.path.exists(infrared_path):
                pixmap = QPixmap(infrared_path)
                self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio))
            else:
                QMessageBox.warning(self, '警告', f'红外检测图像不存在: {infrared_path}')
        # 融合检测
        elif self.radioButtons[5].isChecked():
            self.label.clear()
            infrared_path = f"{base_path}_merge_detect{ext}"
            if os.path.exists(infrared_path):
                pixmap = QPixmap(infrared_path)
                self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio))
            else:
                QMessageBox.warning(self, '警告', f'融合图像检测不存在: {infrared_path}')
        # 可见光
        elif self.radioButtons[0].isChecked():
            self.label.clear()
            infrared_path = f"{base_path}{ext}"
            if os.path.exists(infrared_path):
                pixmap = QPixmap(infrared_path)
                self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio))
            else:
                QMessageBox.warning(self, '警告', f'可见光图像不存在: {infrared_path}')

    def merge_enable(self):
        self.radioButtons[2].setEnabled(True)
        self.thread = MergeThread()
        self.thread.start()


    def target_detect(self):
        for i in range(3, 6):
            self.radioButtons[i].setEnabled(True)

    # 目标检测之前检查是否选择了数据和模型
    def check_file(self):
        if self.file_path is None or self.file_path == "":
            QMessageBox.information(self, '提示', '请先导入数据')
            return False
        if self.model_path is None or self.model_path[0] == "":
            QMessageBox.information(self, '提示', '请先选择模型')
            return False
        return True

    # 摄像头检测之前检查是否选择了模型
    def check_model(self):
        if self.model_path is None or self.model_path[0] == "":
            QMessageBox.information(self, '提示', '请先选择模型')
            return False
        return True

    # 刷新
    def flash_target(self):
        if file_is_pic(self.suffix):
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
        path = os.path.join(os.getcwd(), 'result')
        os.system(f"start explorer {path}")

# DetectionThread子线程用来执行导入资源的目标检测
class DetectionThread(QThread):
    signal_done = pyqtSignal(int)  # 是否结束信号
    def __init__(self, file_path, model_path, label):
        super(DetectionThread, self).__init__()
        self.file_path = file_path
        self.model_path = model_path
        self.label = label
    def run(self):
        detect.run(source=self.file_path, weights=self.model_path[0], show_label=self.label, save_img=True)
        self.signal_done.emit(1)  # 发送结束信号

# MergeThread子线程用来执行导入资源的融合
class MergeThread(QThread):
    signal_done = pyqtSignal(int)  # 是否结束信号
    def __init__(self):
        super(MergeThread, self).__init__()

    def run(self):
        test_Fusion.main()
        self.signal_done.emit(1)  # 发送结束信号



if __name__ == '__main__':
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ui = Ui_MainWindow()
    # 设置窗口透明度
    ui.setWindowOpacity(0.93)
    # 设置窗口图标
    icon = QIcon()
    icon.addPixmap(QPixmap("./UI/icon.ico"), QIcon.Normal, QIcon.Off)
    ui.setWindowIcon(icon)
    # ui.show()
    ui.showMaximized()
    sys.exit(app.exec_())