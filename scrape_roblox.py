import requests

def scrape_thumbnails(gid):
    r = requests.get(f'https://games.roblox.com/v2/games/{gid}/media').json()['data']
    payload = []
    for item in r:
        payload.append({
            'format': 'webp',
            'requestId': f'{item["imageId"]}::Asset:768x432:webp:regular:0',
            'size': '768x432',
            'targetId': item['imageId'],
            'token': '',
            'type': 'Asset'
        })

    r = requests.post('https://thumbnails.roblox.com/v1/batch', json=payload).json()['data']
    return [i['imageUrl'] for i in r]