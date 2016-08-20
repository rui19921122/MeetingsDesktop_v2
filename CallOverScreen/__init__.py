import ctypes
import os

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia

from FigureManage.check_figure import check_figure
from FigureManage.post_figure import post_figure
from .AccidentDisplay import AccidentDisplay
from .CallOverScreen import Ui_Form
from HttpRequest.requests import HttpRequest
from .StudyDisplay import StudyForm

try:
    from mainWindow import MainWindow
except:
    pass

from functools import partial
from .ScrapyDisplay.logic import ScrapyDisplay, ReCompile


class CallOverScreenWidget(QtWidgets.QWidget, Ui_Form):
    over = QtCore.pyqtSignal(int)
    figure_checked = QtCore.pyqtSignal(bytes)
    worker_data = QtCore.pyqtSignal(dict)

    def __init__(self, parent, data: dict):
        ''':type parent:MainWindow'''
        super(CallOverScreenWidget, self).__init__()
        self.is_end = False
        self.setParent(parent)
        print(data)
        self.data = data['data']
        self.call_over_id = data['pk']
        self.parent = parent
        self.setupUi(self)
        self.process_data()
        self.Back.clicked.connect(self.handleBack)
        self.Forward_2.clicked.connect(self.handleForward)
        self.set_up_devices()
        self.figure_checked.connect(partial(post_figure, self))
        self.worker_data.connect(lambda data: self.parent.warn.add_warn('{}已签到'.format(data['people'])))
        self.render_button(0, 2)
        try:
            self.figure_dll = ctypes.windll.JZTDevDll
        except:
            self.parent.warn.add_warn('指纹仪dll加载失败')

    def set_up_devices(self):
        def capture():
            if self.capture.isReadyForCapture():
                self.capture.capture()
            else:
                self.parent.warn.add_warn(self.capture.errorString() or '截取摄像头错误')

        if self.parent.device.current_audio:
            self.audio = QtMultimedia.QAudioRecorder()
            self.audio.setAudioInput(self.parent.device.current_audio.deviceName())
            settings = QtMultimedia.QAudioEncoderSettings()
            settings.setCodec('audio/amr')
            settings.setQuality(QtMultimedia.QMultimedia.HighQuality)
            self.audio_path = os.path.join(os.getcwd(), 'audio.wav')
            self.audio.setEncodingSettings(settings)
            self.audio.setOutputLocation(QtCore.QUrl.fromLocalFile(self.audio_path))
            self.audio.record()
        else:
            self.parent.warn.add_warn('未发现录音设备')
        if self.parent.device.current_camera:
            self.parent.device.camera_timer = QtCore.QTimer()
            self.camera = QtMultimedia.QCamera(self.parent.device.current_camera)
            self.camera.setCaptureMode(QtMultimedia.QCamera.CaptureViewfinder)
            self.camera.start()
            self.capture = QtMultimedia.QCameraImageCapture(self.camera)
            self.capture.setCaptureDestination(QtMultimedia.QCameraImageCapture.CaptureToFile)
            self.capture.capture()
            self.parent.device.camera_timer.timeout.connect(capture)
            self.capture.imageSaved.connect(self.image_captured)
            self.parent.device.camera_timer.start(10000)
        else:
            self.parent.warn.add_warn('未发现照相设备')
        if self.parent.device.figure != None:
            self.parent.device.figure_timer.timeout.connect(partial(check_figure, self))
            self.parent.device.figure_timer.start(4000)
        else:
            self.parent.warn.add_warn('未发现指纹仪设备，将不采集指纹')

    def image_captured(self, capture_id, data):
        res = HttpRequest(method='post', parent=self.parent,
                          url='api/v2/upload/call-over-image/{}'.format(self.call_over_id),
                          files={'file': open(data, 'rb')}
                          )
        res.failed.connect(lambda message: print(message))
        # res.success.connect(lambda _data: os.remove(data))
        res.start()

    def process_data(self):
        print(self.data)
        data = self.data
        classPlanData = data['class_plan']
        dayDetail = classPlanData['day_detail']
        if len(dayDetail) > 0:
            classPlan = QtWidgets.QTableWidget()
            classPlan.setColumnCount(4)
            classPlan.setHorizontalHeaderLabels(['序号', '名称', '内容', '涉及部门'])
            classPlan.horizontalHeader().setStretchLastSection(True)
            classPlan.verticalHeader().setVisible(False)
            width = self.parent.width()
            classPlan.setColumnWidth(0, int(width * 0.10))
            classPlan.setColumnWidth(1, int(width * 0.15))
            classPlan.setColumnWidth(2, int(width * 0.60))
            classPlan.setColumnWidth(3, int(width * 0.15))
            row_count = 0
            for i in dayDetail:
                publishDetail = i['publish_detail']
                row_count += len(publishDetail)
            classPlan.setRowCount(row_count)
            row = 0
            for i in dayDetail:
                publishDetail = i['publish_detail']
                if len(publishDetail) >= 1:
                    style_item = QtWidgets.QTableWidgetItem(i['style'])
                    classPlan.setItem(row, 1, QtWidgets.QTableWidgetItem(i['style']))
                    classPlan.setSpan(row, 1, row + len(publishDetail), 1)
                    classPlan.setItem(row, 3, QtWidgets.QTableWidgetItem(i['department']))
                    classPlan.setSpan(row, 3, row + len(publishDetail), 3)
                    for detail in publishDetail:
                        classPlan.setItem(row, 2, QtWidgets.QTableWidgetItem(detail['detail']))
                        classPlan.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
                        row += 1
            classPlan.resizeRowsToContents()
            self.DisplayLayout.addWidget(classPlan)
        else:
            pass
            # classPlan = QtWidgets.QLabel()
            # classPlan.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            # classPlan.setText('''''''<p style="font-size:24px">本日无班计划录入''')
        accident = data['accident']
        assert isinstance(accident, list)
        if len(accident) > 0:
            display_font = QtGui.QFont()
            display_font.setPixelSize(50)
            for i in accident:
                new = AccidentDisplay(accident.index(i), len(accident), i['content'], i['files'], display_font)
                self.DisplayLayout.addWidget(new)
        else:
            pass
            # accidentWidget = QtWidgets.QLabel()
            # accidentWidget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            # accidentWidget.setText('''''''<p style="font-size:24px">本日无文件通报</p>''')
            # self.DisplayLayout.addWidget(accidentWidget)
        scrapy = data['scrapy']
        _compile = ReCompile()
        for i in scrapy:
            new = ScrapyDisplay(title=i['title'], content=i['content'], _compile=_compile)
            self.DisplayLayout.addWidget(new)
        if self.DisplayLayout.count() == 0:
            accidentWidget = QtWidgets.QLabel()
            accidentWidget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            accidentWidget.setText('''''''<p style="font-size:24px">本日无班前预想</p>''')
            self.DisplayLayout.addWidget(accidentWidget)

    def handleBack(self):
        self.DisplayLayout.setCurrentIndex(self.DisplayLayout.currentIndex() - 1)
        self.render_button(self.DisplayLayout.currentIndex(), self.DisplayLayout.count())

    def end(self):
        def handle_audio_request_over_success(data):
            self.parent.warn.add_warn('录音文件上传完毕,现在可以关闭页面了')
            self.parent.can_close = True

        def handle_audio_request_over_failed(message):
            self.parent.warn.add_warn('未成功上传文件,{}'.format(message))
            self.parent.can_close = True

        try:
            self.camera.stop()
            self.parent.device.camera_timer.stop()
            self.parent.device.camera_timer.disconnect()
        except:
            pass
        if self.parent.device.current_audio and self.audio:
            self.audio.stop()
            self.parent.audio_request = HttpRequest(parent=self.parent,
                                                    url='api/v2/upload/call-over-audio/{}'.format(self.call_over_id),
                                                    method='post',
                                                    files={'file': open(self.audio_path, 'rb')})
            self.parent.audio_request.success.connect(handle_audio_request_over_success)
            self.parent.audio_request.failed.connect(handle_audio_request_over_failed)
            self.parent.warn.add_warn('开始上传录音文件，请不要关闭软件')
            self.parent.audio_request.start()
            self.parent.can_close = False
        if self.parent.device.figure_timer:
            self.parent.device.figure_timer.stop()
        res = HttpRequest(parent=self.parent, url='api/v2/call_over/end-call-over/', method='post')
        res.failed.connect(lambda message: self.parent.warn.add_warn(message))
        res.success.connect(lambda data: self.over.emit(self.call_over_id))
        res.start()

    def handleForward(self):
        if self.is_end:
            self.end()
        else:
            self.DisplayLayout.setCurrentIndex(self.DisplayLayout.currentIndex() + 1)
        self.render_button(self.DisplayLayout.currentIndex(), self.DisplayLayout.count())

    def render_button(self, index, length):
        if index <= 0:
            self.Back.setDisabled(True)
        else:
            self.Back.setDisabled(False)
        if index == length - 1:
            self.is_end = True
            self.Forward_2.setText("结束点名")
        else:
            self.Forward_2.setText("后一条")
            self.is_end = False

    def closeEvent(self, QCloseEvent):
        try:
            self.camera.stop()
            self.parent.device.camera_timer.stop()
            self.audio.stop()
        except:
            pass
