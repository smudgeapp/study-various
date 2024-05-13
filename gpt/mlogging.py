"""

Clear Window Extension
Version: 0.1

Author: Roger D. Serwy
        roger.serwy@gmail.com

Date: 2009-05-22

It provides "Clear Shell Window" under "Options"

Add these lines to config-extensions.def

[ClearWindow]
enable=1
enable_editor=0
enable_shell=1
[ClearWindow_cfgBindings]
clear-window=<Control-Key-l>


"""
import os

class ClearWindow:

    menudefs = [
        ('options', [None,
               ('Clear Shell Window', '<<clear-window>>'),
       ]),]
		 
    def __init__(self, editwin):
        self.editwin = editwin
        self.text = self.editwin.text
        self.text.bind("<<clear-window>>", self.clear_window)

    def clear_window2(self, event): # Alternative method
        # work around the ModifiedUndoDelegator
        text = self.text
        text.mark_set("iomark2", "iomark")
        text.mark_set("iomark", 1.0)
        text.delete(1.0, "iomark2 linestart")
        text.mark_set("iomark", "iomark2")
        text.mark_unset("iomark2")

        if self.text.compare('insert', '<', 'iomark'):
            self.text.mark_set('insert', 'end-1c')
        self.editwin.set_line_and_column()

    def clear_window(self, event):
        # remove undo delegator
        undo = self.editwin.undo
        self.editwin.per.removefilter(undo)

        # clear the window, but preserve current command
        self.text.delete(1.0, "iomark linestart")
        if self.text.compare('insert', '<', 'iomark'):
            self.text.mark_set('insert', 'end-1c')
        self.editwin.set_line_and_column()
 
        # restore undo delegator
        self.editwin.per.insertfilter(undo)


cls = ClearWindow(os.system)
cls.clear_window()
