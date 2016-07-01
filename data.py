from PyQt5 import QtCore, QtNetwork, QtMultimedia


class DataStore():
    def __init__(self):
        self.settings = QtCore.QSettings('WuhuDongzhan', 'Meetings')
        self.data = {}
        self.session = QtNetwork.QNetworkAccessManager()


class DeviceInfo():
    def __init__(self):
        self.audio_devices = []  # type: list[QtMultimedia.QAudioDeviceInfo]
        self.current_audio = None  # type: QtMultimedia.QAudioDeviceInfo
        self.camera_devices = []  # type:list[QtMultimedia.QCameraInfo]
        self.current_camera = None  # type: QtMultimedia.QCameraInfo
        self.error_message = {'camera': None, 'audio': None, 'figure': None}
        self.figure = None  # 指纹仪设备，记录指纹仪编号，当为False时为不可采集指纹，其他时候均为可采集，判断时注意判别
        self.figure_timer = None # type: QtCore.QTimer