import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from functools import partial
import json
from utility_functions import token_length
import create_project

def print_root_children():
    print(root.winfo_children())

def quit_program(event):
    root.quit()

def return_root_single_child():
    children = root.winfo_children()
    if len (children) == 0:
        print('There are no children')
    elif len (children) > 1:
        print('There is more than 1 child')
    else:
        return children[0]




def select_tab_by_label(label_text, notebook):
    for index, tab in enumerate(notebook.tabs()):
        if notebook.tab(tab, "text") == label_text:
            notebook.select(index)
            break

def destroy_widgets(master):
    for widget in master.winfo_children():
            widget.destroy()


class OnSubmit:
    
    def save_text(entered_text, data_label):
        json_data = {
            data_label: entered_text
        }

        with open('save_data.json', 'w') as file:
            json.dump(json_data, file)


    def title(frame, entry_box):
        title = entry_box.get()
        frame.pack_forget()
        return create_project.create_project(title)

    def text_box(frame, text_box):
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

class AutoHideScrollbar(tk.Scrollbar):
    def __init__(self, master, **kwargs):
        tk.Scrollbar.__init__(self, master, **kwargs)
        self.pack_forget()

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
        else:
            self.pack(side="right", fill="y")
        tk.Scrollbar.set(self, lo, hi)

class LoadingPage:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        new_project_button = tk.Button(self.frame, bd=5, text="New Project", command = self.enter_project_title)
        new_project_button.pack()
        load_button = tk.Button(self.frame, bd = 5, text="Load", command=self.load_main_interface)
        load_button.pack()
        exit_button = tk.Button(self.frame, bd = 5, text="Exit", command = self.exit_app)
        exit_button.pack()
        self.frame.pack()

    def load_main_interface(self):

        self.frame.pack_forget()
        MainInterface(self.frame.master)

    #This function takes the entered text and creates the new project
    def new_project(title, window, entry_box, event):
        global PROJECT
        title=entry_box.get()
        PROJECT = create_project.create_project(title)
        window.destroy()
        global loading_page2
        loading_page2 = LoadingPage2(root)

    def enter_project_title(self):
        entry_window = tk.Toplevel(root)
        entry_window.focus_set()

        label = tk.Label(entry_window, text='Title:')
        label.pack(side=tk.LEFT)
        entry_box = tk.Entry(entry_window, width=100)
        entry_box.pack(side=tk.LEFT)
        entry_box.bind("<Return>", partial(self.new_project, entry_window, entry_box))
        entry_box.focus_set()

    def exit_app(self):
        root.quit()

class LoadingPage2:
    def __init__(self, master):
        destroy_widgets(master)
        
        self.frame = tk.Frame(master)
        self.title = PROJECT.title
        title_label = self.create_title_label(self.title)
        
        input_details_button = tk.Button(self.frame, text='Input Novel Details', command=self.load_input_page)
        editing_button = tk.Button(self.frame, text='Use editing and summarization prompts', command=self.load_editing_page)
        blurb_writing_button = tk.Button(self.frame, text='Use Blurb Writing Prompts', command=self.load_blurb_page)
        
        title_label.pack()
        input_details_button.pack()
        editing_button.pack()
        blurb_writing_button.pack()
        self.frame.pack()

    def create_title_label(self, text):
        bold_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        return tk.Label(self.frame, text=text, font=bold_font, relief='ridge', borderwidth=10)
    
    def load_input_page(self):
        destroy_widgets(root)
        main_interface = MainInterface(root)
        main_interface.notebook.select(main_interface.input_frame)

    def load_editing_page(self):
        destroy_widgets(root)
        main_interface = MainInterface(root)
        main_interface.notebook.select(main_interface.editing_frame)

    def load_blurb_page(self):
        destroy_widgets(root)
        main_interface = MainInterface(root)
        main_interface.notebook.select(main_interface.blurb_frame)


class CustomTextBox:
    def __init__(self, master, property_name, text):
        self.frame = tk.Frame(master, borderwidth=5, relief=tk.RIDGE)
        self.frame.pack()

        self.property_name = property_name
        self.submitted_text = "Your text has been saved"
        self.submit_button_text = "Save"


        label = tk.Label(self.frame, text=text)
        label.pack()

        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.textbox = tk.Text(self.frame, height=5, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.textbox.yview)

        submit_button = tk.Button(self.frame, text=self.submit_button_text, command=self.submit_command)
        submit_button.pack()

    def submit_command(self):
        new_property_value = self.textbox.get("1.0", tk.END).strip() # Get text from Text widget
        global PROJECT
        setattr(PROJECT, self.property_name, new_property_value)

        destroy_widgets(self.frame)
        label = tk.Label(self.frame, text=self.submitted_text)
        label.pack()
    
    def change_submitted_text(self, new_text):
        self.submitted_text = new_text




class AddFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.canvas = tk.Canvas(self)
        # self.canvas.pack(side='left', fill = 'both', expand = True)
        # self.scrollbar = AutoHideScrollbar(self.canvas, orient='vertical', command = self.canvas.yview)

        # self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # self.inner_frame = tk.Frame(self.canvas)
        # self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        # self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # self.inner_frame.bind("<Button-1>", lambda e: self.canvas.focus_set())
        # self.canvas.bind("<FocusIn>", lambda e: print("Canvas got focus"))



        self.pack()
        self.title = PROJECT.title
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), foreground="black")

    
    def create_title(self, text):
        label = ttk.Label(self, text=text, style="Title.TLabel")
        label.pack()

    #Note: While when I click on the textbox, the window stops moving, sometimes
    #while the window is selected the textbox also scrolls if the mouse cursor is over 
    #it. This should be corrected later, but doesn't seem like an essential part of an MVP
    #My best guess it that this driven by the scrollbar built into Tkinter's textbox class
    #and that would need to be turned off and on in the relevant functions. 
    def activate_window_scrollbar(self, event):
        self.canvas.bind_all("<MouseWheel>", self.mouse_scroll)
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Text):
                widget.unbind("<MouseWheel>")
        self.canvas.focus_set()

    def deactivate_window_scrollbar(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def bind_activate_window_scrollbar_to_textbox_labels(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for sub_widget in widget.winfo_children():
                    if isinstance (sub_widget, tk.Label):
                        sub_widget.bind("<Button-1>", self.activate_window_scrollbar)
                
    #CHANGE/ WARNING: A clearly ugly solution to getting the font for the default label, that also
        #makes the code more rigid because it doesn't respond to changes in font
    def label_word_wrapper(self, text, max_width = 500):
        label = tk.Label(self)
        font = tkFont.Font(font=label.cget("font"))
        label.destroy()
        words = text.split()
        wrapped_lines = []
        line = ""
        for word in words:
            temp_line = line + " " + word if line else word
            if font.measure(temp_line) <= max_width:
                line = temp_line
            else:
                wrapped_lines.append(line)
                line=word
        wrapped_lines.append(line)
        return "\n".join(wrapped_lines)


class EditorFrame(AddFrame):
    def __init__(self, master):
        super().__init__(master)        
        if not api_key:
            api_entry_box = CustomTextBox(self.frame, 'api_key', "Enter your OpenAI API key")

        self.prompt = CustomTextBox(self.frame, 'current_prompt', 'Curent Prompt for ChatGPT')
        #self.gpt4_toggle = radio button and label
        
        DIVIDED = False
        
        if DIVIDED:
            self.break_into_sections_box()
        else:
            self.display_current_project()


    def display_current_project(self):
        self.outer_project_frame = tk.Frame(self)
        self.outer_project_frame.pack()
        title = tk.Label(self.outer_project_frame, text='Your Current Project')
        title.pack()
        frame = tk.Frame()
        #frame interior
        self.create_buttons()

    def create_buttons(self):
        #run_all_button 
        #download_responses_to_txt_button
        #save_project_button
        pass

    def break_into_sections_box(self):
        #create frame
        
        #create submit button

        #create 'Chapter as divider toggle'
        DIVIDED = True
        pass

class BlurbFrame(AddFrame):
    pass
    

class InputFrame(AddFrame):
    def __init__ (self, master):
        super().__init__(master)
        self.create_title(text = f'Enter the details of {self.title}')

        label_texts = self.fetch_label_texts()
        # self.project_text = CustomTextBox(self.inner_frame, 'project_text', label_texts['project_text'])
        self.project_text = CustomTextBox(self, 'project_text', label_texts['project_text'])
        
        # self.key_information = CustomTextBox(self.inner_frame, 'key_information', label_texts['key_information'])
        self.key_information = CustomTextBox(self, 'key_information', label_texts['key_information'])
        self.key_information.change_submitted_text('Your key information has been saved.')
        
        # self.reviews = CustomTextBox(self.inner_frame, 'reviews', label_texts['reviews'])
        self.reviews = CustomTextBox(self, 'reviews', label_texts['reviews'])
        self.reviews.change_submitted_text('Your example reviews have been saved.')

        # self.blurbs = CustomTextBox(self.inner_frame, 'sample_blurbs', label_texts['sample_blurbs'])
        self.blurbs = CustomTextBox(self, 'sample_blurbs', label_texts['sample_blurbs'])
        self.blurbs.change_submitted_text('Your example blurbs have been saved.')

    def fetch_label_texts(self):
        label_texts = {}
        label_texts['project_text'] = 'Enter the text for your project here'
        label_texts['key_information'] = self.label_word_wrapper('OPTIONAL: Put important information about the novel here. You likely will only realize something needs to be here after seeing what chatGPT writes about your novel. Experiment to see what works best.')
        label_texts['reviews'] = self.label_word_wrapper('OPTIONAL: Put reviews of novels in your genre here. ChatGPT will later use it to identify key features of books in it that readers like. This can be used to improve the editing suggestions and optimize the blurb.')
        label_texts['sample_blurbs'] = self.label_word_wrapper('OPTIONAL: Put examples of blurbs from books in your genre so that chatGPT can use their example to generate a better blurb for you. This only is used for blurb writing.')
        return label_texts

class MainInterface:
    def __init__(self, master) -> None:
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        self.editing_frame = EditorFrame(self.notebook)
        self.blurb_frame = ttk.Frame(self.notebook)
        self.input_frame = InputFrame(self.notebook)

        self.notebook.add(self.input_frame, text="Input Novel")
        self.notebook.add(self.editing_frame, text="Editing and Summarization")
        self.notebook.add(self.blurb_frame, text='Create Blurbs')

def start_program():
    global PROJECT, root, loading_page, loading_page2, api_key
    PROJECT = None
    api_key = None
    root = tk.Tk()
    root.title('GPT Writing Tools')
    loading_page = LoadingPage(root)
    root.geometry("800x600+100+50")
    root.bind_all('<Control-q>', quit_program)
    root.mainloop()

if __name__ == '__main__':
    start_program()