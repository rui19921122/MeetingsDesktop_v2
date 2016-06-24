from PyQt5 import QtCore


class DataStore():
    def __init__(self):
        self.settings = QtCore.QSettings('WuhuDongzhan', 'Meetings')
        self.data = {}
