from app.myai import model


def crate_new_chat_session(history=[]):
    chat_session = model.start_chat(history=history)
    return chat_session