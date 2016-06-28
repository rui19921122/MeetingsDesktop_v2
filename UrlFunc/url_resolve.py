host = 'http://127.0.0.1:8000/'


def parse_url(a: str,param=None):
    if a.endswith('/'):
        pass
    else:
        a = a + '/'
    if type(a) == 'string':
        return host + a
    else:
        return host + str(a)