from PyQt5 import QtCore, QtGui, QtWidgets
from HttpRequest.requests import HttpRequest
from .over import Ui_Form

try:
    from mainWindow import MainWindow
except:
    pass


class OverCallWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent, id):
        '''
        :type parent:MainWindow
        :param parent:
        '''
        super(OverCallWidget, self).__init__()
        self.setParent(parent)
        self.setupUi(self)
        self.parent = parent
        self.id = id
        self.pushButton.clicked.connect(self.submit_note)
        self.textEdit.textChanged.connect(self.handle_text_edit_change)

    def submit_note(self):
        def handle_success(data):
            self.parent.warn('提交备注成功')
            self.textEdit.setDisabled(True)
            self.pushButton.setDisabled(True)

        text = self.textEdit.toPlainText()
        request = HttpRequest(url='api/v2/call_over/call-over-note/{}/'.format(self.id),
                              parent=self.parent,
                              method='post',
                              data={'data': text})
        request.failed.connect(lambda message: self.parent.warn.add_warn(message))
        request.success.connect(handle_success)
        request.start()

    def handle_text_edit_change(self):
        text = self.textEdit.toPlainText()
        if len(text) == 0:
            self.pushButton.setDisabled(True)
        else:
            self.pushButton.setDisabled(False)
