# -*- coding: utf-8 -*-

from webserver.bottle import  route, run, template
import wellknownmsgs.AppStartedMsg

class WebServerController:
    '''Web服务器控制器'''

    def OnMsg_AppStartedMsg(self, msg:wellknownmsgs.AppStartedMsg.AppStartedMsg):

        @route('/hello/<name>')
        def index(name):
            return template('<b>Hello {{name}}</b>!', name=name)
            #return "hello,"+name

        run(host='localhost', port=8080)