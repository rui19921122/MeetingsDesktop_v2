from PyQt5 import QtGui, QtWidgets, QtCore
from .ui import Ui_Form
import re


class ReCompile():
    def __init__(self):
        self.pattern = re.compile(r'【.*?(?=【|$)'
                                  , re.MULTILINE | re.DOTALL)

    def findall(self, string):
        result = self.pattern.findall(string)
        return result


class ScrapyDisplay(QtWidgets.QWidget, Ui_Form):
    def __init__(self, title: str, content: str, _compile: ReCompile):
        super(ScrapyDisplay, self).__init__()
        self.setupUi(self)
        self.title.setText(title)
        results = _compile.findall(string=content)
        text = ''
        for result in results:
            text += '<p style="text-size:12px">{}</p>'.format(result)
        self.textBrowser.setText(text)
