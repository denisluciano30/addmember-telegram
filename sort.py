import json
from datetime import datetime, timedelta
import time

# importing pandas module 
import numpy as np

# Arquivo com a base de dados BR
with open('ibge.json', 'r', encoding='utf-8') as f:
    nomes_ibge_2010 = json.loads(f.read())

nomes = np.array(nomes_ibge_2010)

nomes_list = nomes.tolist()

nomes_sorted = np.sort(nomes_list, kind='quick sort')


a = 10