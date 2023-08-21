import tkinter as tk
from tkinter import ttk

def on_submit():
    pass

root = tk.Tk()
root.title('GPT Writing Tools')

root.geometry("800x600+100+50")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

notebook.add(frame1, text="Input")
notebook.add(frame2, text="Archive Display")

label1 = tk.Label(frame1, text="Input your title here")
label1.pack()

title = tk.Entry(frame1, )
title.pack()

title_submit_button = tk.Button(frame1, text='Save', command=on_submit)
title_submit_button.pack()

novel_text_frame = tk.Frame(frame1)
novel_text_frame.pack()

label2 = tk.Label(novel_text_frame, text="Input your novel here")
label2.pack()

novel_text_scrollbar = tk.Scrollbar(novel_text_frame)
novel_text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

novel_text = tk.Text(novel_text_frame, height = 5, wrap=tk.WORD, yscrollcommand=novel_text_scrollbar.set)
novel_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

novel_text_scrollbar.config(command=novel_text.yview)

submit_button = tk.Button(frame1, text = 'Save', command=on_submit)
submit_button.pack()

label2 = tk.Label(frame2, text="Here is the data in your loaded novel")
label2.pack()

root.mainloop()