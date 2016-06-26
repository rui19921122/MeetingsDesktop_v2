from PyQt5 import QtCore,QtNetwork


class DataStore():
    def __init__(self):
        self.settings = QtCore.QSettings('WuhuDongzhan', 'Meetings')
        self.data = {}
        self.session = QtNetwork.QNetworkAccessManager()
