from pynput.keyboard import Key, Controller
import win32api
from win32con import *
import webbrowser

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

keyboard = Controller()

def swipe(orientation):
    if(orientation == "Swipe Right"):
        keyboard.press(Key.alt)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    elif(orientation == "Swipe Left"):
        keyboard.press(Key.alt)
        keyboard.press(Key.shift)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    elif(orientation == "Done Swipe"):
        keyboard.release(Key.alt)
        keyboard.release(Key.shift)
    elif(orientation == "Tab Left"):
        keyboard.press(Key.ctrl)
        keyboard.press(Key.shift)
        keyboard.press(Key.tab)
        keyboard.release(Key.ctrl)
        keyboard.release(Key.shift)
        keyboard.release(Key.tab)
    elif(orientation == "Tab Right"):
        keyboard.press(Key.ctrl)
        keyboard.press(Key.tab)
        keyboard.release(Key.ctrl)
        keyboard.release(Key.tab)

def scroll(up):
    if(up > 0):
        win32api.mouse_event(MOUSEEVENTF_WHEEL, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], int(up*90), 0)
    elif(up < 0):
        win32api.mouse_event(MOUSEEVENTF_WHEEL, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], int(up*90), 0)

def mouse(x, y):
    # win32api.SetCursorPos((x, y))
    pos = win32api.GetCursorPos()
    win32api.SetCursorPos((pos[0] + x, pos[1] - y))

def press(command):
    if(command == "Left Click"):
        win32api.mouse_event(MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(MOUSEEVENTF_LEFTUP,0,0)
        print('Left Click')
    if(command == "Close Tab"):
        keyboard.press(Key.ctrl)
        keyboard.press('w')
        keyboard.release(Key.ctrl)
        keyboard.release('w')
    if(command == "Open Window"):
        webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open("chrome://newtab")
        

def volume(v):
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    print(volume.GetMasterVolumeLevel())
    # print(volume.GetVolumeRange())
    volume.SetMasterVolumeLevel(v, None)