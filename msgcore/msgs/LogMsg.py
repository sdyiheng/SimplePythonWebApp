"""日志消息"""


class LogMsg(object):
    '''日志消息'''

    def __init__(self, category, detailInfo):
        self._Category = category
        self._DetailInfo = detailInfo

    @property
    def DetailInfo(self):
        return self._DetailInfo


