from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager
from PyQt5.QtCore import QUrl


class Fetch():
    def __init__(self, session: QNetworkAccessManager, url: QUrl, method: str=None, data=None, header=None
                 , handle: bool = False):
        request = QNetworkRequest()
        request.setUrl(url)
        if method == 'delete':
            response = session.deleteResource(request)
        elif method == 'post':
            response = session.post(request)
        else:
            # 此时method为get
            response = session.get(request)
        assert isinstance(response,QNetworkReply)
        session.finished.connect(self.handle)
        response.close()

    def handle(self,reply:QNetworkReply):
        print(1)


if __name__ == '__main__':
    f = Fetch(session=QNetworkAccessManager(),url=QUrl('http://127.0.0.1:8000/api/v2/auth/login/'))
