import json

from PyQt5 import QtCore

import requests
from PyQt5.QtCore import QThread, QMutex
import mainWindow
from PyQt5.QtNetwork import QNetworkReply
import pdb
from UrlFunc.url_resolve import parse_url



class HttpRequest(QThread):
    success = QtCore.pyqtSignal(dict)
    failed = QtCore.pyqtSignal(str)

    def __init__(self, parent, url: str, method, data=None, files=None):
        super(HttpRequest, self).__init__()
        self.setParent(parent)
        self.method = method
        self.data = data
        self.session = parent.session
        self.url = parse_url(url)
        self.files = files

    def run(self):
        mutex = QMutex()
        mutex.lock()
        try:
            if self.method == 'post':
                response = self.session.post(self.url, data=self.data, files=self.files)
            elif self.method == 'get':
                response = self.session.get(self.url)
            elif self.method == 'delete':
                response = self.session.delete(self.url)
            else:
                raise Exception('不正确的方法')
            if response.status_code >= 300:
                try:
                    data = response.json()
                    if 'non_field_errors' in data:
                        error_message = data['non_field_errors']
                    else:
                        error_message = data.get('error', '未知错误')
                    message = '网络请求错误，错误码为{}，原因为{}'.format(response.status_code, error_message)
                    self.failed.emit(message)
                except:
                    print(response.text)
            else:
                data = response.json()
                self.success.emit(data)
        except requests.Timeout as error:
            self.failed.emit('网络请求错误，超时，请检查网络连接')
        except BaseException as error:
            print('BaseException'.format(error))
            self.failed.emit(str(error.args))
        finally:
            mutex.unlock()
            self.deleteLater()
