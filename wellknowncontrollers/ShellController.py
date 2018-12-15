class ShellController:
    '''Shell控制器'''

    def OnShellCmdLine(self, cmdline):
        '''命令行'''
        if cmdline == "q":
            exit()