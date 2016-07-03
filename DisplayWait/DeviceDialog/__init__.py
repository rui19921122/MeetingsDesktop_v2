from PyQt5 import QtWidgets
from . import dialog
import mainWindow


class DeviceDialog(QtWidgets.QDialog, dialog.Ui_Dialog):
    def __init__(self, parent):
        super(DeviceDialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self._refresh_form()
        self.RefreshButton.clicked.connect(self.RefreshButtonClicked)
        self.OkButton.clicked.connect(self.OkButtonClicked)

    def _refresh_form(self):
        self.LineEdit.setText('正常' if self.parent.device.figure==False else '异常')
        try:
            self.AudioComboBox.disconnect()
        except:
            pass
        self.AudioComboBox.clear()
        if len(self.parent.device.audio_devices) >= 1:
            for i in self.parent.device.audio_devices:
                self.AudioComboBox.addItem(i.deviceName())
            self.AudioComboBox.setCurrentIndex(
                self.parent.device.audio_devices.index(self.parent.device.current_audio))
        else:
            self.AudioComboBox.addItem('无录音设备')
            self.AudioComboBox.setCurrentIndex(1)
            self.AudioComboBox.setDisabled(True)

        # 初始化
        try:
            self.CameraComboBox.disconnect()
        except:
            pass
        self.CameraComboBox.clear()
        if len(self.parent.device.camera_devices) >= 1:
            for i in self.parent.device.camera_devices:
                self.CameraComboBox.addItem(i.deviceName())
            self.CameraComboBox.setCurrentIndex(
                self.parent.device.camera_devices.index(self.parent.device.current_camera))
        else:
            self.CameraComboBox.addItem('无照相设备')
            self.CameraComboBox.setCurrentIndex(0)
            self.CameraComboBox.setDisabled(True)

    def RefreshButtonClicked(self):
        self.parent.centralWidget().set_up_device()
        self._refresh_form()

    def OkButtonClicked(self):
        self.parent.device.current_audio = self.parent.device.audio_devices[self.AudioComboBox.currentIndex()]
        self.parent.device.current_camera = self.parent.device.camera_devices[self.CameraComboBox.currentIndex()]
        self.close()
