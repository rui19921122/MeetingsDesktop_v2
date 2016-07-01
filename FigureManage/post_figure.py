from HttpRequest.requests import HttpRequest


def post_figure(widget, value: bytes):
    res = HttpRequest(url='api/v2/call_over/post-figure/',
                      data={'number': widget.parent.data['attend_table_number'],
                            'figure_data': value.decode('utf-8')},
                      method='post', parent=widget.parent)
    res.failed.connect(lambda message: widget.parent.warn.add_warn(message))
    res.start()
