from PyQt5 import QtCore


class CustomQAbstractNativeEventFilter(QtCore.QAbstractNativeEventFilter):
    def __init__(self):
        super(CustomQAbstractNativeEventFilter, self).__init__()

    def nativeEventFilter(self, QByteArray, sip_voidptr):
        print(QByteArray)
        return False
