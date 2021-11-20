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
import csv

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

    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())


    group_source_id = config['group_source']

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
            if chat.megagroup is not None and chat.access_hash is not None and group_source_id == chat.id:
                group = chat
        except:
            continue

    get_data_user(client, group)


def get_data_user(client, group):

    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())

    all_participants = client.get_participants(group.id, aggressive=True)
    results = []
    today = datetime.now()
    last_week = today + timedelta(days=-7)
    last_month = today + timedelta(days=-30)
    path_file = 'data/user/' + phone + "_" + str(group.id) + '.json'

    # open the file in the write mode
    new_file = open('members.csv', 'w', newline='', encoding="utf8")
    
    # create the csv writer
    writer = csv.writer(new_file)

    header = ['username','user id','access hash','name','group','group id']
    writer.writerow(header)

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

            if config['from_date_active'] == 'online' and date_online_str != 'online':
                continue
            
            if date_online_str  != 'online' and int(date_online_str) < int(config['from_date_active']):
                continue

            line = []
            line.append(str(user.username))
            line.append(str(user.id))
            line.append(str(user.access_hash))
            line.append(str(user.first_name))
            line.append(str(group.title))
            line.append(str(group.id))


            writer.writerow(line)
        
        except:
            print("Error get user")

    # close the file
    new_file.close()


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


with open('numeros.json', 'r', encoding='utf-8') as f:
    numeros = json.loads(f.read())

indices_account = config['indices_account']
accounts = []

for indice in indices_account:
	accounts_indice = numeros['accounts'][indice]
	accounts = accounts + accounts_indice

folder_session = 'session/'

time_get_group = config['time_get_group']

account_to_get_data = config['account_to_get_data']

api_id = account_to_get_data['api_id']
api_hash = account_to_get_data['api_hash']
phone = account_to_get_data['phone']

print(phone)
get_group(phone, api_id, api_hash)
    