# -*- coding: utf-8 -*-


class Response(object):

    def __init__(self, **kw):
        for k, v in kw.iteritems():
            setattr(self, k, v)


class RequestsMock(object):

    def __init__(self, status, url):
        self.status = status
        self.url = url
        self.done = False

    def get(self, url):
        kw = {
            'content': "Ok",
            'cookies': None,
            'ok': self.status < 400,
            'status_code': self.status,
            'url': url,
        }

        if self.url == url:
            self.done = True
            return Response(**kw)
