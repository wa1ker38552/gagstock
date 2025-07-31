from collections import defaultdict
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import json
import time

token = open('token.txt', 'r').read().strip()

def fetch(url):
    return requests.get(url, headers={'Authorization': token}).json()


def get_pets():
    r = requests.get('https://growagarden.fandom.com/wiki/Pets')
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all('div', attrs={'class': 'wikia-gallery-item'})
    pets = []
    for i in items:
        links = i.find_all('a')
        if len(links) >= 2:
            link = links[1]
            if '/wiki/' in link['href']:
                name = link.get_text()
                if '(' in name:
                    name = name.split('(')[0][:-1]
                pets.append(name.strip().lower())

    return pets

def get_demand():
    pets = get_pets()
    demand_data = {} # json.load(open('data/demand_data.json', 'r'))
    last_id = None
    for i in tqdm(range(10)):
        if not last_id:
            url = 'https://discord.com/api/v9/channels/1365731632534917141/messages?limit=100'
        else:
            url = f'https://discord.com/api/v9/channels/1365731632534917141/messages?limit=100&before={last_id}'

        r = fetch(url)
        last_id = r[-1]['id']
        for item in r:
            counter = []
            for p in pets:
                if p in item['content'].lower():
                    counter.append(p)
            counter = list(set(counter))
            for item in counter:
                if item in demand_data:
                    demand_data[item] += 1
                else:
                    demand_data[item] = 1

    # with open('data/demand_data.json', 'w') as file:
    #     json.dump(demand_data, file)

    if 'bee' in demand_data: del demand_data['bee']
    threshold = max(list(demand_data.values()))
    display_list = [[key, round((demand_data[key]/threshold) * 10, 2), demand_data[key]] for key in demand_data]
    display_list.sort(key=lambda x: x[1])
    return display_list[::-1]
