"消息总线，消息发送（等待），控制器注册"
# -*- coding: utf-8 -*-
from inspect import signature
from utils.threadpool import  *
import queue

__all__ = ["Post", "PostAndWait", "Register", "UnRegister"]

channels = {}

asyncMsgHandleThreadPool = ThreadPool(5)

class msgHandler(object):
    '''消息处理器'''
    def __init__(self, msgTypeName, async_, handlerMethod):
        ''''''
        self._msgTypeName = msgTypeName
        self._async = async_
        self._handlerMethod = handlerMethod
        self._asyncTasks =  queue.Queue()# queue()

    def handle(self, msg, async_):
        '''处理消息'''
        if not async_:
            #同步处理
            self._handlerMethod(msg)

        elif self._asyncTasks.empty():
            #如果为空的话
            self._asyncTasks.put_nowait(msg)
            tasks = makeRequests(msgHandler.handleAsync,[self] )
            [asyncMsgHandleThreadPool.putRequest(req) for req in tasks]

        else:
            self._asyncTasks.put_nowait(msg)

    @classmethod
    def handleAsync(cls, _msgHandler):
        '''异步处理'''
        #print(_msgHandler)

        while(not _msgHandler._asyncTasks.empty()):
            msg = _msgHandler._asyncTasks.get()
            _msgHandler._handlerMethod(msg)


class msgChannel():
    '''消息通道'''

    def __init__(self):
        self._channelName = ""
        self._msgHandlerMap = {}

    @property
    def channelName(self):
        return self._channelName

    @property
    def msgHandlers(self):
        return self._msgHandlerMap

    def addMsgHandler(self, msgType, handlerMethod, async_):
        '''添加消息处理喊出'''
        if not self._msgHandlerMap.__contains__(msgType):
            self._msgHandlerMap[msgType] = []

        # print(type(msgType))
        # print(type(handlerMethod))

        handlers = self._msgHandlerMap[msgType]
        handlers.append(msgHandler(msgType, async_, handlerMethod))
        #print(handlers)
    #
    # @classmethod
    # def syncCall(cls, handlerMethod):
    #     ''''''
    #     def wrapper(*args, **kargs):
    #         return handlerMethod(args, kargs)
    #
    #     return wrapper;
    #
    # @classmethod
    # def asyncCall(cls, handlerMethod):
    #     ''''''
    #     def wrapper(*args, **kargs):
    #         return handlerMethod(args, kargs)
    #
    #     return wrapper;

    def handleMsg(self, msg, async_):
        '''处理消息'''
        msgType = type(msg)
        #print(msgType)
        msgTypeName = msgType.__module__+'.'+msgType.__qualname__
        #print(msgTypeName)

        if not self._msgHandlerMap.__contains__(msgTypeName):
            return

        for handler in self._msgHandlerMap[msgTypeName]:
            handler.handle(msg, async_)


def Post(msg, channel=""):
    """PostMessage"""
    if not channels.__contains__(channel):
        return

    channel = channels[channel];
    channel.handleMsg(msg, True)


def PostAndWait(msg, channel=""):
    """PostAndWait"""
    if not channels.__contains__(channel):
        return

    channel = channels[channel];
    channel.handleMsg(msg, False)


def Register(controller, channelName=""):
    """消息类型注册"""
    for f in dir(controller):

        # 判断是否函数
        m = getattr(controller, f)

        if not callable(m):
            continue

        isOnMsg_ = f.startswith("OnMsg_")
        isOnMsgA_ = f.startswith("OnMsgA_")
        if not isOnMsg_ and not isOnMsgA_:
            continue

        sig = signature(m)
        if sig.parameters.__len__() != 1:
            continue

        msgTypeName = ""
        for p in sig.parameters:
            # print(type(sig.parameters[p]))
            # print(sig.parameters[p].name)
            # print(sig.parameters[p].annotation.__module__+'.'+sig.parameters[p].annotation.__qualname__)#annotation.__module__+'.'+annotation.__qualname__
            msgTypeName = sig.parameters[p].annotation.__module__+'.'+sig.parameters[p].annotation.__qualname__
            #print(msgTypeName)

        if msgTypeName == "":
            continue

        if not channels.__contains__(channelName):
            channels[channelName] = msgChannel()

        channel = channels[channelName];
        #print(channel)
        channel.addMsgHandler(msgTypeName, m, isOnMsgA_)


def UnRegister(controller, channel=""):
    """消息类型注销"""



