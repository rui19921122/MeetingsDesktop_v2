import sys
from PyQt5 import QtCore, QtWidgets

from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager, QNetworkCookieJar
from PyQt5.QtCore import QUrl
import json
from UrlFunc.url_resolve import parse_url


class Fetch():
    data = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        self.session = QNetworkAccessManager(parent)
        self.cookies = QNetworkCookieJar()
        self.parent = parent
        self.session.setCookieJar(self.cookies)

    def base_handler(self, reply: QNetworkReply):
        try:
            response = json.loads(str(reply.readAll(), encoding='utf-8'))
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        except:
            self.parent.warn.add_warn("Http解析错误")
            return
        if reply.error() != QNetworkReply.NoError:
            self.handler_error(response, status_code)
        else:
            self.data.emit(response)

    def get(self, url, param=None):
        url = QtCore.QUrl(parse_url(url, param))
        request = QNetworkRequest(url)
        reply = self.session.get(request)
        return reply

    def post(self, url, param=None, data=None, json=True):
        if isinstance(data, dict):
            f = ''
            for i in data:
                f += '{}={}&'.format(i, data[i])
            data = f[:-1]
        byte_data = QtCore.QByteArray()
        byte_data.append(data)
        url = QtCore.QUrl(parse_url(url, param))
        request = QNetworkRequest(url)
        if json:
            request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json')
        reply = self.session.post(request, byte_data)
        return reply

    def handler_error(self, response, status_code):
        if isinstance(response, dict):
            message = response.get('error', 'unknown')
            self.parent.warn.add_warn('网络请求错误，错误码为{},原因为{}'.format(status_code, message))
