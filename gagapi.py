from scrape_discord import update_discord_worker
from scrape_discord_demand import get_demand
from scrape_roblox import scrape_thumbnails
from scrape_discord import refresh_updates
from flask import render_template
from threading import Thread
from flask import Response
from flask import request
from flask import Flask
import scrape_discord
import requests
import copy
import json
import time

app = Flask(__name__)
version = '1.2.0'

game_updates = refresh_updates()
game_thumbnails = scrape_thumbnails(7436755782)
discord_demand = get_demand()
discord_demand_lu = time.time()
exploiter_worker_data = json.load(open('test.json', 'r'))
full_data = exploiter_worker_data
image_cache = {}

def send_webhook(text):
    requests.post("https://discord.com/api/webhooks/1400947756175982712/1RHExGUJ47sma13HzY1zlxYeSemmIuHI3Xo5a0_nfsK7e9uKzYDdbcSDTqQ4EC6AD-mf", json={"content": text})

def update_discord_demand(interval=120):
    global discord_demand, discord_demand_lu
    while True:
        time.sleep(interval)
        discord_demand = get_demand()
        discord_demand_lu = time.time()

def update_game_updates(interval=600):
    global game_updates
    while True:
        time.sleep(interval)
        game_updates = refresh_updates()

def update_game_thumbnails(interval=600):
    global game_thumbnails
    while True:
        time.sleep(interval)
        game_thumbnails = scrape_thumbnails(7436755782)

def create_lookups(data):
    lookup = {}
    for item in data:
        lookup[item['name']] = item
    return lookup

def combine_data(discord, lookup):
    data = []
    for i in discord:
        item = {
            'name': i[1],
            'stock': i[0]
        }
        if i[1] in lookup:
            # copy just to be safe
            c = copy.copy(lookup[i[1]])
            del c['name']
            try: del c['stock'] # eggs don't have stock
            except KeyError: pass
            item.update(c)
        data.append(item)
    return data

def concatenate_data(interval=1):
    global full_data
    while True:
        try:
            # create lookups
            egg_lookup = create_lookups(exploiter_worker_data['eggs']['data'])
            gear_lookup = create_lookups(exploiter_worker_data['gear']['data'])
            seed_lookup = create_lookups(exploiter_worker_data['seed']['data'])

            full_data = {
                'cosmetics': exploiter_worker_data['cosmetics'],
                'eggs': {
                    'data': combine_data(scrape_discord.discord_stock_data['Egg'], egg_lookup),
                    'timer': int(1800-(time.time()-scrape_discord.discord_stock_data['Egg_timer'])) # exploiter_worker_data['eggs']['timer']
                },
                'gear': {
                    'data': combine_data(scrape_discord.discord_stock_data['GearStock'], gear_lookup),
                    'timer': int(300-(time.time()-scrape_discord.discord_stock_data['GearStock_timer'])) #exploiter_worker_data['gear']['timer']
                },
                'seed': {
                    'data': combine_data(scrape_discord.discord_stock_data['SeedStock'], seed_lookup),
                    'timer': int(300-(time.time()-scrape_discord.discord_stock_data['SeedStock_timer'])) #exploiter_worker_data['seed']['timer']
                },
                'last_updated': exploiter_worker_data['last_updated'] if exploiter_worker_data['last_updated'] > scrape_discord.discord_stock_data['last_updated'] else scrape_discord.discord_stock_data['last_updated']
            }
        except Exception as e:
            send_webhook(f'{str(e)} ERROR')
        time.sleep(interval)


@app.route('/')
def app_index():
    return render_template('index.html', version=version, thumbnail=game_thumbnails[0])

@app.route('/stock')
def app_stock():
    return render_template('stock.html')

@app.route('/chances')
def app_chances():
    return render_template('chances.html')

@app.route('/demand')
def app_demand():
    return render_template('demand.html')

@app.route('/proxy/<assetid>')
def proxy(assetid):
    if assetid in image_cache:
        url = image_cache[assetid]
    else:
        url = requests.get(f'https://thumbnails.roblox.com/v1/assets?assetIds={assetid}&returnPolicy=PlaceHolder&size=110x110&format=webp').json()['data'][0]['imageUrl']
        image_cache[assetid] = url
    return Response(requests.get(url).content, content_type="image/png")

# interal API routes
@app.route('/api/chances')
def api_chances():
    return {
        'data': scrape_discord.discord_chance_data,
        'last_updated': scrape_discord.discord_chance_ld
    }

@app.route('/api/demand')
def api_demand():
    return {
        'data': discord_demand,
        'last_updated': discord_demand_lu
    }

@app.route('/api/updates')
def api_updates():
    return game_updates

# Actual API routes for public API
@app.route('/api/data')
def api_data():
    return full_data

@app.route('/api/last_updated')
def api_last_updated():
    return {'data': full_data['last_updated']}

@app.route('/api/seeds')
def api_seeds():
    return {'data': full_data['seed']['data']}

@app.route('/api/eggs')
def api_eggs():
    return {'data': full_data['eggs']['data']}

@app.route('/api/gears')
def api_gears():
    return {'data': full_data['gear']['data']}

@app.route('/api/cosmetics')
def api_cosmetics():
    return {'data': full_data['cosmetics']['data']}

@app.route('/api/upload', methods=['POST'])
def api_upload():
    global exploiter_worker_data
    exploiter_worker_data = request.json
    with open('test.json', 'w') as file:
        json.dump(exploiter_worker_data, file)
    return {'success': True}

Thread(target=update_discord_worker, daemon=True).start()
Thread(target=concatenate_data, daemon=True).start()
Thread(target=update_game_thumbnails, daemon=True).start()
Thread(target=update_game_updates, daemon=True).start()
Thread(target=update_discord_demand, daemon=True).start()

app.run(host='0.0.0.0', port=5008)
