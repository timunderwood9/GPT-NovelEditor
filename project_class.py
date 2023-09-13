import json
from tiktoken import encoding_for_model
import math
import openai

class Section:
    def __init__(self, section_text, llm_results, name):
        self.name = name
        self.section_text = section_text
        self.llm_results = llm_results

    def to_dict(self):
        return {
            'scene_text': self.section_text,
            'llm_results': self.llm_results
        }

class Chapter:
    def __init__(self, name):
        self.sections = []
        self.name = name

    def add_section(self, section):
        self.sections.append(section)

    def to_dict(self):
        return {
            'scenes': [section.to_dict() for section in self.sections]
        }

class Project:
    def __init__(self, **kwargs):
        self.chapters = []
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def chapters_to_dict(self):
        return {
            'chapters': [chapter.to_dict() for chapter in self.chapters]
        }
    
    def get_attributes_as_dict(self):
        return vars(self)

    def save(self, to_default_path = True):
        if to_default_path == False:
            filename = self.open_save_dialogue()
        #should I be using a join function of some sort?
        #Check again how to get the right path to the save file in the save folder
        #else: filename = self.title + '.json'
        with open(filename, 'w') as file:
            json.dump(self.get_attributes_as_dict(), file)
    
    @staticmethod
    def open_save_dialogue():
        pass

    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return Project(**data)

            
            # for chapter_data in data['chapters']:
            #     chapter = Chapter()
            #     for scene_data in chapter_data['scenes']:
            #         scene = Scene(scene_data['scene_text'], scene_data['llm_results'])
            #         chapter.add_scene(scene)
            #     novel.add_chapter(chapter)
    
    def split_text_into_chunks(self, text, max_chunk_size=2000, overlap=40):
        chunks = []
        index = 0
        encoded_text = self.encode_text(text)
        number_of_sections = 1
        if len(encoded_text) > max_chunk_size:
            number_of_sections = math.ceil(len(encoded_text)/(max_chunk_size+overlap))
        chunk_size = math.ceil(len(encoded_text)/ number_of_sections) + overlap

        while index < len(encoded_text):
            decoded_chunk= self.decode_text(encoded_text[index:index+chunk_size])
            chunks.append(decoded_chunk)
            index += chunk_size - overlap

        return chunks

    #this will take the whole raw text and return a list of sections
    def split_chapter(self, text):
        chunks = self.split_text_into_chunks(text)
        for chunk in chunks:
            scene = Section(chunk, None)
            chapter = Chapter()
            chapter.add_section(scene)
            self.add_chapter(chapter)
    
    def generate_chapter_list(self):
        #code to get the chapter texts based on the chapter divider
        #code to name the chapters
        #code to name the scenes
        pass

    def split_all_chapters(self):
        pass

    def send_section_to_GPT(self, section):
        text = section.section_text
        model = 'gpt-3.5-turbo'
        if self.gpt4_flag:
            model = 'gpt-4'

        section.llm_results = openai.ChatCompletion.create(
            model = model,
            messages = [
                {"role" : "system", "content" : self.current_prompt},
                {"role" : "system", "content" : text}
            ]
        )
        print(model)

    def send_all_sections_to_GPT(self):
        for chapter in self.chapters:
            for section in chapter.sections:
                self.send_section_to_GPT(section)
                self.send_message_to_GUI(section)
    
    #Placeholder: I'm pretty sure print will not let me do what I want
    def send_message_to_GUI(section):
        print(section.name)

    #right now going to do a pdf instead, but I think this option should be there eventually
    def create_txt_for_download(self):
        pass

    def create_pdf_of_gpt_outputs(self):
        pdf_text = []
        for chapter in self.chapters:
            for section in chapter.sections:
                heading = self.make_bold(section.name + ':\n')
                self.add_to_pdf(heading)
                text += section.llm_results + '\n'
                self.add_to_pdf(text)
        pdf = self.create_pdf(pdf_text)
        self.open_save_dialogue(pdf)

    def make_bold(self, text):
        pass

    @staticmethod
    def create_project(project_title=None):
        if project_title == None:
            project_title = 'project'
        project = Project()
        project.title = project_title
        return project
    

    def encode_text(self, text):
        return encoding_for_model('gpt-4').encode(text)

    def decode_text(self, text):
        return encoding_for_model('gpt-4').decode(text)
    
