from PyQt5 import QtGui,QtCore,QtWidgets
from .AccidentDisplay import Ui_Form
class AccidentDisplay(QtWidgets.QWidget, Ui_Form):
    def __init__(self, index, count, content, files, font):
        super(AccidentDisplay, self).__init__()
        self.setupUi(self)
        self.TextLabel.setText('规章文件、事故案例学习(第{},共{}条)'.format(index + 1, count))
        self.Content.setText(content)
        self.Content.setFont(font)
        if len(files) == 0:
            pass
        else:
            for file in files:
                widget = QtWidgets.QListWidgetItem()
                widget.setText(file['filename'])
                widget.setData(0, file['filename'])
                widget.setData(1, file['file'])
                self.listWidget.addItem(widget)
            self.listWidget.doubleClicked.connect(self.handleClicked)

    def handleClicked(self, item):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(item.data(1)))

