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