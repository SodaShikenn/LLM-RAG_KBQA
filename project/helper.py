from config import *
from openai import OpenAI


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


def get_llm_chat(messages, model_name, stream=False):
    model = LLM_MODELS[model_name]
    client = OpenAI(
        base_url = model['base_url'],
        api_key = model['api_key']
    )
    response = client.chat.completions.create(
        model = model['model_name'],
        messages = messages,
        temperature = 0.7,
        stream = stream
    )
    return response


if __name__ == '__main__':
    # resp = get_llm_embedding('さよならくちびる')
    # print(resp)
    # print(len(resp.data[0].embedding))
    resp = get_llm_chat([
        {'role': 'user', 'content': '给我讲个笑话.'}
    ], 'qwen-max')
    print(resp)