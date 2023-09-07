import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x400")  # Set window width to be wider than textboxes

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        

        self.frame = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.yview)
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.update_window_size)
        self.canvas.bind_all("<MouseWheel>", self.mouse_scroll)
        self.canvas.bind("<Button-1>", self.focus_out_textbox)  # Focus out when clicking on canvas
        self.frame.bind("<Button-1>", self.focus_out_textbox)  # Focus out when clicking on frame


        for i in range(20):
            label = tk.Label(self.frame, text=f"Label {i+1}")
            label.pack()
            label.bind("<Button-1>", self.focus_out_textbox)  # Focus out when clicking on label

            text_box = tk.Text(self.frame, width=50, height=10)
            text_box.pack()
            text_box.bind("<FocusIn>", self.focus_in_textbox)
            text_box.bind("<FocusOut>", self.focus_out_textbox)

    def update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_window_size(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def mouse_scroll(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")

    def focus_in_textbox(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        event.widget.bind("<MouseWheel>", lambda e: self.scroll_textbox(e, event.widget))

    def focus_out_textbox(self, event):
        self.canvas.bind_all("<MouseWheel>", self.mouse_scroll)
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Text):
                widget.unbind("<MouseWheel>")


    def scroll_textbox(self, event, widget):
        widget.yview_scroll(-1*(event.delta//120), "units")



if __name__ == "__main__":
    app = App()
    app.mainloop()
