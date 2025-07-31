import requests


r = requests.get('https://www.gamersberg.com/api/grow-a-garden/stock', headers={
    'Referrer': 'https://www.gamersberg.com/grow-a-garden/stock',
    'Origin': 'https://www.gamersberg.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Priority': 'u=1, i',
    'Cookie': '_lr_env_src_ats=false; _lr_sampling_rate=0; last_session_day=s%3A2025-07-02.hVjai9NWOutoqIQCCZ1w6Fg0JZTPLyvv9OLrElaVaQY; _lr_retry_request=true; cumulative_time=s%3A0.123.bPaAVY0lKrTEIB45hfAd1rW0jhdbDIRpOwOpT3JT%2BBA; session_start=s%3A1751483521843.dfOkBtVazn7XTjAk6xDJ%2FjwS9VeZx1b4s8ZOBoFQPZs'
})
print(r.json())