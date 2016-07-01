from .Display import Ui_DisplayWorker
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork, QtMultimedia
from Warn import widget
from collections import OrderedDict
from functools import partial
from HttpRequest.requests import HttpRequest
import ctypes
from .DeviceDialog import DeviceDialog
from HttpRequest.requests import HttpRequest
from FigureManage.post_figure import post_figure
from FigureManage.check_figure import check_figure
from Login import LoginForm

try:
    import yaml
except:
    pass


class AlignHCenterTableItem(QtWidgets.QTableWidgetItem):
    def __init__(self, text):
        super(AlignHCenterTableItem, self).__init__()
        self.setText(text)
        self.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)


class DisplayWorkerForm(QtWidgets.QWidget, Ui_DisplayWorker):
    figure_checked = QtCore.pyqtSignal(bytes)
    _begin_call_over = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(DisplayWorkerForm, self).__init__()
        self.setupUi(self)
        self.parent = parent
        self.refresh_worker_status()
        self.pushButton.setDisabled(True)
        self.pushButton.clicked.connect(self.handle_refresh_clicked)
        self.pushButton_2.clicked.connect(self.show_device_dialog)
        self.parent.data['worker_status'] = OrderedDict()
        self.tableWidget.setRowCount(0)
        self.pushButton.setStyleSheet('border-color:gray')
        self.BeginButton.clicked.connect(self.BeginButtonClicked)
        self.figure_checked.connect(partial(post_figure, self))
        try:
            self.figure_dll = ctypes.windll.JZTDevDll
        except:
            self.parent.warn.add_warn('指纹仪dll加载失败')
        self.set_up_device()

    def BeginButtonClicked(self):
        message_box = QtWidgets.QMessageBox.warning(self.parent, '警告', '锁定点名表后将无法修改出勤人员，确定么',
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if message_box == QtWidgets.QMessageBox.Yes:
            res = HttpRequest(parent=self.parent,
                              url='api/v2/call_over/lock-call-over-person/',
                              method='post',
                              data={'number': self.parent.data['attend_table_number']})
            res.success.connect(self.begin_call_over)
            res.failed.connect(lambda message: self.parent.warn.add_warn(message))
            res.start()

    def begin_call_over(self, data):
        self.parent.data['lock'] = True
        self.render_start_button()

    def show_device_dialog(self):
        dialog = DeviceDialog(self.parent)
        dialog.show()

    def set_up_device(self):
        """
        设置设备状态,强制重新绑定指纹计时器
        :return:
        """
        audio_device_info = QtMultimedia.QAudioDeviceInfo()
        camera_device_info = QtMultimedia.QCameraInfo()
        if len(audio_device_info.availableDevices(
                QtMultimedia.QAudio.AudioInput
        )) >= 1:
            self.parent.device.audio_devices = audio_device_info.availableDevices(
                QtMultimedia.QAudio.AudioInput)
            if not self.parent.device.current_audio or not self.parent.device.current_audio in \
                    self.parent.device.audio_devices:
                self.parent.device.current_audio = audio_device_info.defaultInputDevice()
            self.set_device_error_message(None, 'audio')
        else:
            self.parent.device.current_audio = None
            self.set_device_error_message('未发现有效的录音设备', 'audio')
        if len(camera_device_info.availableCameras(
        )) >= 1:
            self.parent.device.camera_devices = camera_device_info.availableCameras(
            )
            if not self.parent.device.current_camera or not self.parent.device.current_camera in self.parent.device.camera_devices:
                self.parent.device.current_camera = camera_device_info.defaultCamera()
            self.set_device_error_message(None, 'camera')
        else:
            self.parent.device.current_camera = None
            self.set_device_error_message('未发现有效的照相设备', 'camera')
        if self.figure_dll and self.figure_dll.FPIDevDetect() >= 0:
            '''如果重新发现指纹仪,且考勤表已锁定，则重新绑定timer'''
            self.render_start_button()
            self.set_device_error_message(None, 'figure')
            self.parent.device.figure = self.figure_dll.FPIDevDetect()
            if not self.parent.device.figure_timer:
                self.parent.device.figure_timer = QtCore.QTimer()
        else:
            self.set_device_error_message("未发现有效的指纹仪采集设备", 'figure')
            self.parent.device.figure = False

    def refresh_worker_status(self):
        request = HttpRequest(parent=self.parent, url='api/v2/call_over/get-call-over-person/', method='get')
        request.success.connect(self.handle_refresh_data_arrive)
        request.failed.connect(lambda message: self.parent.warn.add_warn(message))
        request.start()

    def handle_refresh_data_arrive(self, data: dict):
        """
        当刷新的数据到达时，处理数据，并将刷新按钮复原
        :param data:
        :return:
        """
        # print(yaml.dump(data))
        origin = self.parent.data.get('lock', False)
        if 'attend' in data:
            self.parent.data['lock'] = data['attend']['lock']
            persons = data['attend']['person']
            self.parent.data['attend_table_number'] = data['attend']['id']
            if self.parent.data['lock']:
                '''
                如果表未锁定，因可能存在增删人员情况，故重新渲染整个页面
                '''
                for i in persons:
                    if i['id'] in self.parent.data['worker_status']:
                        lines = self.parent.data['worker_status'][i['id']]
                        lines[0].setText(i['worker'])
                        lines[1].setText(i['position'])
                        lines[2].setText('是' if i['study'] else '否'),
                        lines[3].setText(self.render_data(i['checked'])),
                    else:
                        self.parent.data['worker_status'][i['id']] = [
                            AlignHCenterTableItem(i['worker']),
                            AlignHCenterTableItem(i['position']),
                            AlignHCenterTableItem('是' if i['study'] else '否'),
                            AlignHCenterTableItem(self.render_data(i['checked'])),
                        ]
                        row = self.tableWidget.rowCount()
                        self.tableWidget.setRowCount(row + 1)
                        for index, d in enumerate(self.parent.data['worker_status'][i['id']]):
                            self.tableWidget.setItem(row, index, d)
            else:
                self.tableWidget.setRowCount(0)
                self.parent.data['worker_status'] = {}
                for i in persons:
                    self.parent.data['worker_status'][i['id']] = [
                        AlignHCenterTableItem(i['worker']),
                        AlignHCenterTableItem(i['position']),
                        AlignHCenterTableItem('是' if i['study'] else '否'),
                        AlignHCenterTableItem(self.render_data(i['checked'])),
                    ]
                    row = self.tableWidget.rowCount()
                    self.tableWidget.setRowCount(row + 1)
                    for index, d in enumerate(self.parent.data['worker_status'][i['id']]):
                        self.tableWidget.setItem(row, index, d)
            self.render_start_button(origin=origin)
        else:
            self.parent.warn.add_warn('数据解析错误，{}'.format(data))
        self.pushButton.setDisabled(False)

    def render_start_button(self, origin=False):
        if self.parent.data.get('lock', False):
            try:
                self.BeginButton.disconnect()
            except:
                pass
            if self.parent.device.figure != None:
                if origin:
                    pass
                else:
                    '''重新绑定timer，以确保可以绑定到指纹仪事件'''
                    try:
                        self.parent.device.figure_timer.stop()
                        self.parent.device.figure_timer.disconnect()
                    except:
                        pass
                    finally:
                        self.parent.warn.add_warn('已开始采集指纹', type='success')
                        self.parent.device.figure_timer.timeout.connect(partial(check_figure, self))
                        self.parent.device.figure_timer.start(1500)
            else:
                self.parent.warn.add_warn('未发现指纹仪设备，无法采集指纹')
            self.label_2.setText('点击开始点名按钮将会进入点名界面，届时仍可采集指纹，但会被标记为迟到')
            self.BeginButton.setText('开始点名')
            self.BeginButton.clicked.connect(self.begin_)
        else:
            '''不存在由lock界面变为unlock的情况'''
            pass

    def begin_(self):
        '''
        开始正式点名
        :return:
        '''
        self._begin_call_over.emit()

    def closeEvent(self, QCloseEvent):
        try:
            self.parent.device.figure_timer.disconnect()
        except:
            pass
        print('要关闭了')

    def render_data(self, data: str):
        if data:
            return data.split('T')[-1]
        else:
            return '未打点'

    def set_device_error_message(self, data, style):
        self.parent.device.error_message[style] = data
        has_error = False
        # 设备错误列表中是否有错误信息
        for i in self.parent.device.error_message:
            if self.parent.device.error_message[i]:
                has_error = True
        if has_error:
            self.pushButton_2.setToolTip('''
                <div style="font-size: 21px">
                <p>{}</p><p>{}</p><p>{}</p>
                <p>您可以点击此按钮查看或设置相关情况</p>
    </div>
            '''.format(
                self.parent.device.error_message['audio'] or '',
                self.parent.device.error_message['camera'] or '',
                self.parent.device.error_message['figure'] or '',
            ))
            self.pushButton_2.setStyleSheet('border-color:red')
        else:
            self.pushButton_2.setToolTip('''
                <div style="font-size: 21px">
                <p>设备检测正常，您可以点击此按钮查看或设置相关情况</p>
    </div>
            '''
                                         )
            self.pushButton_2.setStyleSheet('border-color:gray')

    def handle_refresh_clicked(self):
        '''
        请求数据，并将刷新按钮禁用
        :return:
        '''
        self.pushButton.setDisabled(True)
        self.refresh_worker_status()

    @staticmethod
    def set_table_width(table):
        '''
        设置table控件的列宽
        :return:
        '''
        assert isinstance(table, QtWidgets.QTableWidget)
        column_number = table.columnCount()
        single_width = table.width() / column_number
        for i in range(0, column_number):
            table.setColumnWidth(i, single_width)

    def resizeEvent(self, QResizeEvent):
        DisplayWorkerForm.set_table_width(self.tableWidget)
