from HttpRequest.requests import HttpRequest
from functools import partial


def post_figure(widget, value: bytes, need_refresh=False):
    '''
    need_refresh 请不要乱用
    :param widget:
    :param value:
    :param need_refresh:
    :return:
    '''
    res = HttpRequest(url='api/v2/call_over/post-figure/',
                      data={'number': widget.parent.data['attend_table_number'],
                            'figure_data': value.decode('utf-8')},
                      method='post', parent=widget.parent)
    res.failed.connect(lambda message: widget.parent.warn.add_warn(message))
    try:
        res.success.connect(lambda data: widget.worker_data.emit(data))
    except:
        pass
    res.start()
