#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from wellknowncontrollers.LogController import *
from wellknowncontrollers.ShellController import *
from webserver.WebServerController import *
import wellknown
import wellknownmsgs
from wellknownmsgs.AppStartedMsg import *
import time

from msgcore.msgbus import *
from wellknownmsgs.AppStartingMsg import AppStartingMsg


def read_app_info():
    '''读取应用配置信息'''


def register():
    '''注册控制器'''
    Register(LogController())
    Register(WebServerController())


def startup():
    '''应用入口函数'''

    shellController = ShellController()
    Register(shellController)

    #生成应用信息
    appInfo = read_app_info()

    #注册控制器
    register()

    #应用启动消息
    appStartingMsg = AppStartingMsg()
    PostAndWait(appStartingMsg)
    if appStartingMsg.ErrorMsg != "" :
        print("AppStartingError", appStartingMsg.ErrorMsg)
        return

    Post(AppStartedMsg())

    time.sleep(1)
    print("App Started.")
    while True:
        cmdline = input(">>")
        shellController.OnShellCmdLine(cmdline)

if __name__ == "__main__":
    startup()
