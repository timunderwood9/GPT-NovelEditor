import json

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
