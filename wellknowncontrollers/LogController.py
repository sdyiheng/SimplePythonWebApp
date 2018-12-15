"""日志控制器"""
from msgcore.msgs.LogMsg import *

#print(__name__)

#__all__ = ["LogController"]

class LogController():

    def __init__(self):
        ''''''
        #self.OnMsg_AppStartedMsg

    def OnMsg_AppStartedMsg(self, msg:LogMsg):

        print("Received A Msg", msg.DetailInfo)
        pass

