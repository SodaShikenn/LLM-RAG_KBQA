from config import *
from openai import OpenAI
from config import *


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def segment_text(text, segment_length=500, overlap=100):
    """
    For unstructured documents without specific dividing lines, we'll use the simplest and most straightforward method: splitting them by word count.
    """
    segments = []
    start = 0
    while start < len(text):
        end = start + segment_length
        segments.append(text[start:end])
        start += segment_length - overlap
    return segments

def get_embedding_model():
    return EMBEDDING_MODELS[EMBEDDING_MODEL_NAME]

def get_llm_embedding(input):
    model = get_embedding_model()
    client = OpenAI(
        base_url = model['base_url'],
        api_key = model['api_key']
    )
    response = client.embeddings.create(
        model = model['model_name'],
        input = input,
        encoding_format = "float"
    )
    return response

if __name__ == '__main__':
    resp = get_llm_embedding('さよならくちびる')
    print(resp)
    print(len(resp.data[0].embedding))