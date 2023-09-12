from tiktoken import encoding_for_model
import project_class

def encode_text(text):
    return encoding_for_model('gpt-4').encode(text)

def decode_text(text):
    return encoding_for_model('gpt-4').decode(text)

def create_project(project_title):
    if project_title == None:
        project_title = 'project'
    return project_class.Project(project_title)

def split_text_into_chunks(text, max_chunk_size=2000, overlap=40):
    chunks = []
    index = 0
    encoded_text = encode_text(text)
    while index < len(encoded_text):
        decoded_chunk=decode_text(encoded_text[index:index+chunk_size])
        chunks.append(decoded_chunk)
        index += chunk_size - overlap
    return chunks

def generate_chapters_by_splitting(project, text):
    chunks = split_text_into_chunks(text)
    for chunk in chunks:
        scene = project_class.Scene(chunk, None)
        chapter = project_class.Chapter()
        chapter.add_scene(scene)
        project.add_chapter(chapter)

        
    
