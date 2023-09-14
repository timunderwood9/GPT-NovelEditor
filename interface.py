import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from functools import partial
import json
from utility_functions import token_length
import create_project

def wrap_with_font(font, text, max_width = 600):
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

def quit_program(event):
    root.quit()

def select_tab_by_label(label_text, notebook):
    for index, tab in enumerate(notebook.tabs()):
        if notebook.tab(tab, "text") == label_text:
            notebook.select(index)
            break

def destroy_widgets(master):
    for widget in master.winfo_children():
            widget.destroy()

def deactivate_window_scrollbar(event):
    root.unbind_all("<MouseWheel>")


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
        PROJECT.divided = False
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

#currently defined to only take 'textbox' and 'entrybox' as types.
class CustomTextBox:
    def __init__(self, master, property_name, label_text, widget_type = 'textbox', submitted_text = "Your entry has been saved:\n{}", default_text=None):
        self.frame = tk.Frame(master, borderwidth=5, relief=tk.RIDGE)
        self.frame.pack()

        self.label_text = label_text
        self.property_name = property_name
        self.submitted_text = submitted_text
        self.widget_type = widget_type
        self.submit_button_text = "Save"
        self.default_text=default_text

        self.build_inner_widgets()

    def deactivate_window_scrollbar(self, event):
        root.unbind_all("<MouseWheel>")

    def submit_command(self):
        if self.widget_type == 'textbox':
            new_property_value = self.textbox.get("1.0", tk.END).strip() # Get text from Text widget
        elif self.widget_type == 'entrybox':
            new_property_value = self.entrybox.get()

        global PROJECT
        setattr(PROJECT, self.property_name, new_property_value)

        destroy_widgets(self.frame)
        #Limiting the length of the printed portion of the entry and adding a '...' for formatting reasons
        if len(new_property_value) > 200: new_property_value_string = new_property_value[0:200] + '...'
        else: new_property_value_string = new_property_value

        self.label = tk.Label(self.frame, height=5, text = self.submitted_text.format(new_property_value_string))
        self.label.pack(side=tk.LEFT)

        self.edit_button = tk.Button(self.frame, text = 'Edit', command=self.edit_command)
        self.edit_button.pack(side=tk.LEFT)
    
    def edit_command(self):
        destroy_widgets(self.frame)

        self.build_inner_widgets()

    def build_inner_widgets(self):
        self.label = tk.Label(self.frame, text=self.label_text)
        self.label.pack()

        if self.widget_type == 'textbox':
            self.textbox = tk.Text(self.frame, height=5, wrap=tk.WORD)
            self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.textbox.bind("<FocusIn>", deactivate_window_scrollbar)

        elif self.widget_type == 'entrybox':
            self.entrybox = tk.Entry(self.frame, width=40)
            self.entrybox.pack(side=tk.LEFT)

        elif self.widget_type == 'Text':
            self.text = tk.Text (self.frame, height=5, wrap='word')
            self.text.insert('1.0', self.default_text)
            self.text.configure(state='disabled')
            self.text.pack(side=tk.LEFT)


        else: print('Widget type not defined')

        submit_button = tk.Button(self.frame, text=self.submit_button_text, command=self.submit_command)
        submit_button.pack()

    
    def change_submitted_text(self, new_text):
        self.submitted_text = new_text

class PromptDisplayBox:
    def __init__(self, master, prompt_text = "You are a developmental editor with years of experience in helping writers create bestselling novels, you will rate the following scene and then provide concrete and specific advice on how to make it more emotionally powerful, compelling, and evocative.") -> None:
        self.property = 'current_prompt'
        self.default_prompt = prompt_text
        self.current_prompt = prompt_text        

        self.frame = tk.Frame(master)
        self.frame.pack()
        self.label = tk.Label(self.frame, text = 'Your Current Prompt')
        self.label.pack()
        self.generate_prompt_display(self.current_prompt)

    def generate_prompt_display(self, prompt_text):
        self.prompt_display = tk.Text(self.frame, height = 5, wrap = 'word')
        self.prompt_display.pack()
        self.prompt_display.insert('1.0', prompt_text)
        self.prompt_display.configure(state='disabled')
        
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack()

        self.edit_button = tk.Button(self.button_frame, text='Edit', command=self.on_edit_press)
        self.edit_button.pack(side = tk.LEFT)
    
    def on_edit_press(self):
        self.prompt_display.configure(state='normal')
        self.edit_button.pack_forget()
        self.save_button = tk.Button(self.button_frame, text = 'Save', command=self.on_save)
        self.reset_button = tk.Button(self.button_frame, text = 'Reset Prompt', command=self.on_reset)
        self.save_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)

    def on_save(self):
        self.prompt_display.configure(state='disabled')
        self.current_prompt = self.prompt_display.get('1.0', 'end-1c')

        self.save_button.pack_forget()
        self.reset_button.pack_forget()
        self.edit_button.pack(side=tk.LEFT)
        if not self.current_prompt == self.default_prompt:
            self.reset_button.pack()

    def on_reset(self):
        self.edit_button.pack_forget()
        self.reset_button.pack_forget()
        self.save_button.pack(side=tk.LEFT)
        self.reset_button.pack(side=tk.LEFT)
        self.prompt_display.configure(state='normal')
        self.prompt_display.delete('1.0', 'end')
        self.prompt_display.insert('1.0', self.default_prompt)

class AddFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side='left', fill = 'both', expand = True)

        self.scrollbar = tk.Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(fill='y', side='right')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0,0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.update_scrollregion)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.canvas.bind("<Configure>", self.update_window_size)
        self.frame.bind("<Button-1>", self.activate_window_scrollbar)  # Focus out when clicking on frame

        self.title = PROJECT.title
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), foreground="black")
        
    def mouse_scroll(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")

    def update_scrollregion(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_window_size(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def create_title(self, text):
        label = ttk.Label(self.frame, text=text, style="Title.TLabel")
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
        return wrap_with_font(font, text, max_width)



class EditorFrame(AddFrame):
    def __init__(self, master):
        super().__init__(master)
        global PROJECT
        self.divided = PROJECT.divided
            
        if not api_key:
            self.api_entry_box = CustomTextBox(self.frame, 'api_key', 'Please enter your OpenAI api key here', widget_type='entrybox', submitted_text='We will use {} as the API key')

        self.prompt = PromptDisplayBox(self.frame)
        self.create_gpt4_toggle()
        if not self.divided: 
            self.break_into_sections_box()
        else: 
            self.display_current_project()

    def update_gpt4_flag(self):
        global button_exists
        PROJECT.gpt4_flag = 0
        PROJECT.gpt4_flag = self.gpt4_flag.get()
        print(PROJECT.gpt4_flag)

        if PROJECT.gpt4_flag and not self.button_exists == True:
            text="Note: GPT-4 costs 20 times as much per token. Experiment to make sure you like the results before using it extensively"
            customFont = tkFont.Font(family="Helvetica", size=10, weight="bold")
            wrapped_text = self.label_word_wrapper(text)

            self.gpt_buttons_label = tk.Label(self.toggle_frame, text = wrapped_text,
                    font=customFont,
                    fg="red")
            self.gpt_buttons_label.pack(side=tk.BOTTOM)
            self.button_exists = True

    def create_gpt4_toggle(self):
        self.toggle_frame = tk.Frame(self.frame)
        self.toggle_frame.pack()
        self.inner_toggle_frame = tk.Frame(self.toggle_frame)
        self.inner_toggle_frame.pack()

        self.gpt4_flag = tk.IntVar()
        self.gpt4_flag.set(0)
        self.button_exists = False


        self.gpt_turbo_button = tk.Radiobutton(self.inner_toggle_frame, variable = self.gpt4_flag, command= self.update_gpt4_flag, text='GPT-3.5', value=0)
        self.gpt_4_button = tk.Radiobutton(self.inner_toggle_frame, variable=self.gpt4_flag, command=self.update_gpt4_flag, text= 'GPT-4', value=1)
        self.gpt_turbo_button.pack(side=tk.LEFT)
        self.gpt_4_button.pack(side=tk.LEFT)

    def break_into_sections_box(self):
        self.divide_frame= tk.Frame(self.frame)
        self.divide_frame.pack()
        label = tk.Label(self.divide_frame, text = self.label_word_wrapper("We still need to break this project into sections small enough to be sent to GPT. You can break the text up at each capitalized 'Chapter'. Otherwise everything will be divided into equally sized sections with an overlap of fifty characters. This is how chapters will be divided also."))
        label.pack()

        self.chapter_divider_flag = tk.BooleanVar()
        self.chapter_divider_flag.set(False)

        self.divide_text_buttons_frame = tk.Button(self.divide_frame)
        self.divide_text_buttons_frame.pack()

        check_button = tk.Checkbutton(self.divide_text_buttons_frame, variable=self.chapter_divider_flag, command=self.set_chapter_divider_flag)
        check_button.pack(side=tk.LEFT)

        submit_button = tk.Button(self.divide_text_buttons_frame, text='Split your text into sections', command=self.submit_break_into_sections)
        submit_button.pack(side=tk.LEFT)        

    def set_chapter_divider_flag(self):
        self.chapter_divider_value = self.chapter_divider_flag.get()
        print (self.chapter_divider_value)

    def submit_break_into_sections(self):
        PROJECT.divided = True
        self.divide_frame.destroy()
        self.display_current_project()
        

    def display_current_project(self):
        print(PROJECT.divided)
        self.outer_project_frame = tk.Frame(self.frame)
        self.outer_project_frame.pack()
        title = tk.Label(self.outer_project_frame, text='Your Current Project')
        title.pack()
        inner_frame = tk.Frame(self.outer_project_frame, relief='raised', borderwidth=10)
        label = tk.Label(inner_frame, text='placeholder')
        inner_frame.pack()
        label.pack()
        self.create_buttons()


    def create_buttons(self):
        button_frame = tk.Frame(self.frame)
        button_frame.pack()
        self.run_all_button = tk.Button(button_frame, text = 'Run on all sections', command=self.run_all)
        self.download_responses_to_txt_button = tk.Button(button_frame, text = 'Save as .txt file', command=self.download_responses_to_txt)
        self.save_project_button = tk.Button(button_frame, text = 'Save Project', command=self.save_project)
        
        self.run_all_button.pack(side=tk.LEFT)
        self.download_responses_to_txt_button.pack(side=tk.LEFT)
        self.save_project_button.pack(side=tk.LEFT)

    def run_all (self):
        pass

    def download_responses_to_txt(self):
        pass

    def save_project(self):
        pass


class BlurbFrame(AddFrame):
    pass
    

class InputFrame(AddFrame):
    def __init__ (self, master):
        super().__init__(master)
        self.create_title(text = f'Enter the details of {self.title}')

        label_texts = self.fetch_label_texts()
        self.project_text = CustomTextBox(self.frame, 'project_text', label_texts['project_text'])
        
        #Section headings that will be used for later features but I've dropped from my
        #minimum viable product version
        self.key_information = CustomTextBox(self.frame, 'key_information', label_texts['key_information'])
        self.key_information.change_submitted_text('Your key information has been saved.')
        
        self.reviews = CustomTextBox(self.frame, 'reviews', label_texts['reviews'])
        self.reviews.change_submitted_text('Your example reviews have been saved.')

        self.blurbs = CustomTextBox(self.frame, 'sample_blurbs', label_texts['sample_blurbs'])
        self.blurbs.change_submitted_text('Your example blurbs have been saved.')

        self.test_scrolling = CustomTextBox(self.frame, 'not_relevant', 'This box is just here for testing purposes')
        
        self.bind_activate_window_scrollbar_to_textbox_labels()

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
    global PROJECT, root, loading_page, loading_page2, api_key, WARNING_FONT
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