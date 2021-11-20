import csv
from unidecode import unidecode
import json

# open the file in the write mode
new_file = open('members.csv', 'w', newline='', encoding="utf8")

# create the csv writer
writer = csv.writer(new_file)

header = ['username','user id','access hash','name','group','group id']
writer.writerow(header)

# Arquivo com a base de dados BR
with open('ibge_dados_2010_array.json', 'r', encoding='utf-8') as ibge_file:
    nomes_ibge_2010 = json.loads(ibge_file.read())

with open("members_no_filter.csv", encoding="utf8") as members_file:
    csv_reader = csv.reader(members_file)

    for line in csv_reader:
        try:

            if len(line[3]) <= 2:
                continue 

            nome_telegram = str(str(line[3]).lower())
            primeiro_nome_telegram = nome_telegram.strip().split(' ')[0]
            primeiro_nome_telegram_sem_acento = unidecode(primeiro_nome_telegram)
            
            if primeiro_nome_telegram_sem_acento not in nomes_ibge_2010:
                continue

            # write a row to the csv file
            writer.writerow(line)
        except:
            print("Erro ao ler nome")



# close the file
new_file.close()