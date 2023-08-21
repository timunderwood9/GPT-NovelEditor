import tkinter as tk
from tkinter import ttk
from functools import partial
from manage_inputs import token_length

class OnSubmit:
    def title():
        pass
    def text_entry(frame, text_box):
        entered_text = text_box.get("1.0", tk.END)
        text_token_length = token_length(entered_text)
        for widget in frame.winfo_children():
            widget.pack_forget()
        new_label = tk.Label(frame, text= "We've saved your text")
        new_label.pack()
        new_label2 = tk.Label(frame, text=f"The text is {text_token_length} tokens long")
        new_label2.pack()

        edit_button = tk.Button(frame, text='Edit', command=restore_frame)
        edit_button.pack() 


def restore_frame(frame):
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

title_frame = tk.Frame(frame1)
title_frame.pack()

label1 = tk.Label(title_frame, text="Input your title here")
label1.pack()

title = tk.Entry(title_frame, width=100)
title.pack(side=tk.LEFT)

title_submit_button = tk.Button(title_frame, text='Save', command=OnSubmit.title)
title_submit_button.pack(side=tk.RIGHT)

novel_text_frame = tk.Frame(frame1, borderwidth=5, relief=tk.RIDGE)
novel_text_frame.pack()

label2 = tk.Label(novel_text_frame, text="Input your novel here")
label2.pack()

novel_text_scrollbar = tk.Scrollbar(novel_text_frame)
novel_text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

novel_text = tk.Text(novel_text_frame, height = 5, wrap=tk.WORD, yscrollcommand=novel_text_scrollbar.set)
novel_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

novel_text_scrollbar.config(command=novel_text.yview)

submit_button = tk.Button(novel_text_frame, text = 'Save', command=partial(OnSubmit.text_entry, novel_text_frame, novel_text))
submit_button.pack()

label2 = tk.Label(frame2, text="Here is the data in your loaded novel")
label2.pack()

root.mainloop()