from telethon import TelegramClient, connection
import logging
from telethon import sync, TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusOffline, UserStatusRecently, UserStatusLastMonth, \
    UserStatusLastWeek
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
        get_data_group(client, phone)


def get_data_group(client, phone):
    print('getting data ' + phone)
    chats = []
    last_date = None
    chunk_size = 200

    query = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))

    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    # group source
    group_source_id = config['group_source']

    get_data_user(client, group_source_id)


def get_data_user(client, group_id):

    all_participants = client.get_participants(group_id, aggressive=True)
    results = []
    today = datetime.now()
    last_week = today + timedelta(days=-7)
    last_month = today + timedelta(days=-30)
    path_file = 'data/user/' + phone + "_" + str(group_id) + '.json'
    

    for user in all_participants:

        # Número mínimo caracteres nome
        if numero_minimo_caracteres_nome != None:
            if len(user.first_name) <= numero_minimo_caracteres_nome:
                continue 
        
        # Caso vá adicionar para grupos gringos não fazer sentido deixar isso aqui
        if apenas_ddd_55:
            if user.phone != None and user.phone[0:1] != '55':
                continue
        
        # Verificando a última vez online se é >= a data nas configurações
        # TO-DO (Fazer a checagem por aqui, assim já filtra para não verificar no add)

        #verificando se é um nome que contém na base do ibge
        if checar_base_ibge:
            
            nome_telegram = str(str(user.first_name).lower())
            primeiro_nome_telegram = nome_telegram.strip().split(' ')[0]
            primeiro_nome_telegram_sem_acento = unidecode(primeiro_nome_telegram)
            
            if primeiro_nome_telegram_sem_acento not in nomes_ibge_2010:
                continue
        
        try:
            if isinstance(user.status, UserStatusRecently):
                date_online_str = 'online'
            else:
                if isinstance(user.status, UserStatusLastMonth):
                    date_online = last_month
                if isinstance(user.status, UserStatusLastWeek):
                    date_online = last_week
                if isinstance(user.status, UserStatusOffline):
                    date_online = user.status.was_online

                date_online_str = date_online.strftime("%Y%m%d")
            tmp = {
                'user_id': str(user.id),
                'access_hash': str(user.access_hash),
                'username': str(user.username),
                'first_name': str(user.first_name),
                "date_online": date_online_str
            }
            results.append(tmp)
        except:
            print("Error get user")
    with open(path_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

# Arquivo com a base de dados BR
with open('ibge_dados_2010_array.json', 'r', encoding='utf-8') as f:
    nomes_ibge_2010 = json.loads(f.read())

## Parametros do bot
from_date_active = config['from_date_active']
checar_base_ibge = config['checar_base_ibge']
apenas_ddd_55 = config['apenas_ddd_55']
numero_minimo_caracteres_nome = config['numero_minimo_caracteres_nome']

accounts = config['accounts']

folder_session = 'session/'

for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']
    print(phone)
    get_group(phone, api_id, api_hash)