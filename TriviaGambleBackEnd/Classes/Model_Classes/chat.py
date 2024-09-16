
# return model obj for firestore db

def get_chat_obj_for_firestore_db():
    return {
        "messages": [{
            "text":'Start the chat...',
            "player": "",
            "id": ""
        }]
    }