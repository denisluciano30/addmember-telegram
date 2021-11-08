from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek
import json
from datetime import datetime, timedelta
import time

logging.basicConfig(level=logging.WARNING)


def get_group(phone, api_id, api_hash):
    folder_session = 'session/'
    client = TelegramClient(folder_session + phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        print('Login fail, need to run init_session')
    else:
        get_data_group(client, phone)


def get_data_group(client, phone):
    print('getting data ' + phone)
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    query = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(query.chats)
    for chat in chats:
        try:
            if chat.megagroup is not None and chat.access_hash is not None:
                groups.append(chat)
        except:
            continue

    results = []
    for group in groups:
        try:
            tmp = {
                'group_id': str(group.id),
                'access_hash': str(group.access_hash),
                'title': str(group.title),
            }
            results.append(tmp)

        except Exception as e:
            print(e)
            print('error save group')
    with open('data/group/' + phone + '.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

with open('numeros.json', 'r', encoding='utf-8') as f:
    numeros = json.loads(f.read())

indice_account = config['indice_account']
accounts = numeros['accounts'][indice_account]

folder_session = 'session/'

for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    print(phone)
    get_group(phone, api_id, api_hash)
    