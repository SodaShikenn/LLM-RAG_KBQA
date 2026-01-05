from helper import get_llm_embedding
from apps.dataset.milvus_models import DatasetMilvusModel
from apps.dataset.models import Segment
from config import *


def retrieve_related_texts(messages, params):
    # Concatenate recent conversation content
    input_str = ''
    for message in messages[-3:]:
        input_str += f"{message['role']}: {message['content']}\n\n"
    # Retrieve similar texts
    vector_resp = get_llm_embedding(input_str)
    query_vector = vector_resp.data[0].embedding
    expr = ' or '.join([f'dataset_id=={dataset_id}' for dataset_id in params['dataset_ids']])
    related_objs = DatasetMilvusModel.search([query_vector], TOP_K, expr, ['dataset_id', 'document_id', 'segment_id'])
    # Process data
    segment_ids = []
    for hits in related_objs:
        for hit in hits:
            for field_name in hit.fields:
                if field_name == 'segment_id':
                    segment_ids.append(hit.entity.get(field_name))
    # Query segments and concatenate content
    segments = Segment.query.filter(Segment.id.in_(segment_ids)).all()
    content = 'Please refer to the following content to answer the user\'s question:\n\n'
    for segment in segments:
        content += segment.content + '\n\n'
    # Insert retrieved content into messages
    new_message = {'role': 'system', 'content': content}
    last_message = messages.pop()
    messages.append(new_message)
    messages.append(last_message)
    return messages