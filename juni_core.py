import openai
import os
import uuid

chats = {}

def send_single_message(system_message, message, creative=False):
    chat_id = init_chat(system_message)
    return send_message_to_chat(message, chat_id, creative)

def init_chat(system_message):
    chat_id = uuid.uuid4()
    push_message(system_message, "system", chat_id)
    return chat_id

def send_message_to_chat(message, chat_id, creative=False):
    push_message(message, "user", chat_id)
    response = send_prompt_to_gpt(chat_id, creative)
    push_message(response, "assistant", chat_id)
    return response

def push_message(message, role, chat_id):
    global chats
    
    if chat_id not in chats:
        chats[chat_id] = [{"role": role, "content": message}]
    else:
        chats[chat_id].append({"role": role, "content": message})

def send_prompt_to_gpt(chat_id, creative=False):
    global chats
    openai.api_key = os.environ.get('JUNI_OPENAI_KEY')

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=chats[chat_id],
        temperature=1.0 if creative else 0.0,
        max_tokens=7000,
        presence_penalty=0.0,
        frequency_penalty=0.0
    )

    return response.choices[0].message.content