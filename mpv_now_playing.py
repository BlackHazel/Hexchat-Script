#!/usr/bin/env python
# -*- coding: utf-8 -*-
#https://github.com/hexchat/documentation/blob/master/script_python.rst
#Reset: '\0F'
#Bold: '\02'
#Color: '\03'
#Hidden: '\10'
#Underline: '\37'
#Original Attributes: '\17'
#Reverse Color: '\26'
#Beep: '\07'
#Italics: '\35' (2.10.0+)
#1.1
#Update for latest MPV
#https://docs.python.org/2.3/whatsnew/section-slices.html
#
#Updated version of https://github.com/kuehnelth/xchat_mpv_np/blob/master/xchat_mpv_np_windows.py

__module_name__ = "mpv now playing"
__module_version__ = "2.0"
__module_description__ = "Displays mpv info"
__author__ = "BlackHazel"

import hexchat
import ctypes, ctypes.wintypes
 
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

titles = []
MAX_PATH = 260

def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        if buff.value.endswith(" - mpv"):
            titles.append(buff.value[:-10])
    return True

def mpv_np(caller, callee, helper):
    global titles
    titles = []
    EnumWindows(EnumWindowsProc(foreach_window), 0)

    if len(titles) > 0:
        hexchat.command("me is now playing \x02\x036%s\x0F" % titles[0])
    else:
        print("mpv is not runnung")
    return hexchat.EAT_ALL

help_string = "Usage: /mpv"
hexchat.hook_command(
    "mpv",
    mpv_np,
    help = help_string
)

print(help_string)
