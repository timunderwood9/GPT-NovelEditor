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

pyautogui.typewrite('The Missing Prince')
pyautogui.typewrite(['enter'])

with open ('test_novel.txt', 'r', encoding='utf-8') as f:
    text = f.read()

interface.PROJECT.project_text = text
interface.loading_page2.load_input_page()


