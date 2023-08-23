import tiktoken

encoding = tiktoken.encoding_for_model('gpt-4')

def token_length(text):
    return len(encoding.encode(text))

