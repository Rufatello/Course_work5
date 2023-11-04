import requests
import psycopg2
URL_COMPANY = 'https://api.hh.ru/employers/'
def get_load_vakansy():
    data = requests.get(f'{URL_COMPANY}', params={'per_page': 1}).json()
    return data
a=get_load_vakansy()
print(a)

