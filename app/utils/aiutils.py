from app.myai import model
from app.myai import topicModel

def crate_new_chat_session(history=[]):
    chat_session = model.start_chat(history=history)
    return chat_session

def get_topic(chat_history):
    response = topicModel.generate_content(chat_history)
    return response.text