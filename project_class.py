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
    def __init__(self, title, author = None):
        self.title = title
        self.author = author
        self.project_text = ""
        self.chapters = []

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'chapters': [chapter.to_dict() for chapter in self.chapters]
        }

    def save(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file)

    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            novel = Project(data['title'], data['author'])
            for chapter_data in data['chapters']:
                chapter = Chapter()
                for scene_data in chapter_data['scenes']:
                    scene = Scene(scene_data['scene_text'], scene_data['llm_results'])
                    chapter.add_scene(scene)
                novel.add_chapter(chapter)
            return novel
