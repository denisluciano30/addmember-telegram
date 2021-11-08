from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import json
from datetime import datetime, timedelta
import time
from unidecode import unidecode


logging.basicConfig(level=logging.WARNING)

def get_group(phone, api_id, api_hash):
    folder_session = 'session/'
    client = TelegramClient(folder_session + phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        print('Login fail, need to run init_session')
    else:
        join_group(client, phone)


def join_group(client, phone):
    print('getting data ' + phone)

    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    # group to join
    group_to_join = config['group_to_join']

    channel = client.get_entity(group_to_join)
    client(JoinChannelRequest(channel))

    time.sleep(10)

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

with open('numeros.json', 'r', encoding='utf-8') as f:
    numeros = json.loads(f.read())

indice_account = config['indice_account']
accounts = numeros['accounts'][indice_account]

for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    print(phone)
    get_group(phone, api_id, api_hash)