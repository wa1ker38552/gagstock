from collections import defaultdict
from datetime import datetime
from threading import Thread
from tqdm import tqdm
import requests
import time
import json

token = open('token.txt', 'r').read().strip()

def send_webhook(text):
    requests.post("https://discord.com/api/webhooks/1400947756175982712/1RHExGUJ47sma13HzY1zlxYeSemmIuHI3Xo5a0_nfsK7e9uKzYDdbcSDTqQ4EC6AD-mf", json={"content": text})

def fetch(url):
    return requests.get(url, headers={'Authorization': token}).json()

def refresh_updates():
    return fetch('https://discord.com/api/v9/channels/1358537163326881938/messages?limit=50')

def refresh_ids():
    r = fetch('https://discord.com/api/v9/guilds/1386133051381125170/onboarding')

    def parse_options(index, append=''):
        return {i['role_ids'][0]: i['title']+append for i in r['prompts'][index]['options']}
    
    seeds = parse_options(0, append=' Seed')
    gear = parse_options(1)
    egg = parse_options(2)

    seeds.update(gear)
    seeds.update(egg)

    # to be used in scraping demand
    with open('data/ids.json', 'w') as file:
        json.dump(seeds, file)
    return seeds

def update_chances(item_index):
    messages = []
    for i in tqdm(range(50)):
        if i == 0:
            url = 'https://discord.com/api/v9/channels/1386133052148944960/messages?limit=100'
        else:
            url = f'https://discord.com/api/v9/channels/1386133052148944960/messages?limit=100&before={messages[-1]["id"]}'
        messages.extend(fetch(url))
    messages.reverse()

    stock_chances = {
        'SeedStock': defaultdict(int),
        'Egg': defaultdict(int),
        'GearStock': defaultdict(int)
    }
    for message in messages:
        title = message['content'].split('\n')[0].split()[1]
        stock_data = message['content'].split('\n')[1:-1]
        stock_data = [i.replace('**', '').split()[1] for i in stock_data]
        stock_data = [i.replace('<@&', '')[:-1] for i in stock_data]
        
        for item in stock_data:
            stock_chances[title][item] += 1
        stock_chances[title]['NUM_UPDATES'] += 1

    data = {
        'SeedStock': {},
        'Egg': {},
        'GearStock': {}
    }
    for title in stock_chances:
        for i in stock_chances[title]:
            if i == 'NUM_UPDATES':
                data[title][i] = stock_chances[title][i]
            if str(i) in item_index:
                data[title][item_index[i]] = stock_chances[title][i]
    return data

def update_stock(item_index):
    r = fetch('https://discord.com/api/v9/channels/1386133052148944960/messages?limit=100')
    r.reverse()

    all_stock_data = {}
    for message in r:
        title = message['content'].split('\n')[0].split()[1]
        stock_data = message['content'].split('\n')[1:-1]
        stock_data = [i.replace('**', '').split() for i in stock_data]
        stock_data = [[int(i[0].replace('x', '')), i[1].replace('<@&', '')[:-1]] for i in stock_data]
        
        for i, item in enumerate(stock_data):
            if item[1] in item_index:
                stock_data[i][1] = item_index[item[1]]

        all_stock_data[title] = stock_data
        all_stock_data[title+'_timer'] = datetime.fromisoformat(message['timestamp']).timestamp()

    all_stock_data['last_updated'] = time.time()
    return all_stock_data

def update_ids_worker(interval=120):
    global item_index
    while True:
        time.sleep(interval)
        item_index = refresh_ids()

def refresh_chances(interval=600):
    # also refresh ids here
    global discord_chance_data, item_index, discord_chance_ld
    while True:
        time.sleep(interval)
        item_index = refresh_ids()
        discord_chance_data = update_chances(item_index)
        discord_chance_ld = time.time()

def update_discord_worker(interval=20):
    global discord_stock_data
    Thread(target=refresh_chances, daemon=True).start()
    while True:
        try:
            time.sleep(interval)
            discord_stock_data = update_stock(item_index)
        except Exception as e:
            send_webhook(str(e), 'Error from stock discord')

item_index = refresh_ids()
discord_stock_data = update_stock(item_index)
discord_chance_data = update_chances(item_index)
discord_chance_ld = time.time()