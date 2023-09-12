import json
from tiktoken import encoding_for_model
import math
import re

class Scene:
    def __init__(self, scene_text, llm_results):
        self.scene_text = scene_text
        self.llm_results = llm_results

    def to_dict(self):
        return {
            'scene_text': self.scene_text,
            'llm_results': self.llm_results
        }

class Chapter:
    def __init__(self):
        self.scenes = []

    def add_scene(self, scene):
        self.scenes.append(scene)

    def to_dict(self):
        return {
            'scenes': [scene.to_dict() for scene in self.scenes]
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

    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.get_attributes_as_dict(), file)

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

    def generate_chapters_by_splitting(self):
        chunks = self.split_text_into_chunks(self.raw_text)
        for chunk in chunks:
            scene = Scene(chunk, None)
            chapter = Chapter()
            chapter.add_scene(scene)
            self.add_chapter(chapter)
    
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
    
