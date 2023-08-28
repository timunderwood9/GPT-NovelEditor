import pyautogui
import interface
import threading
import time
import tkinter as tk

pyautogui.FAILSAFE = True

gui_thread = threading.Thread(target = interface.start_program)
gui_thread.start()
time.sleep(.05)

interface.loading_page.enter_project_title()

pyautogui.typewrite('Death in Solomnia')
pyautogui.typewrite(['enter'])

interface.loading_page2.load_input_page()
