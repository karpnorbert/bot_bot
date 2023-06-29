from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import pandas as pd
from datetime import datetime, timedelta

api_id = '25214343'
api_hash = '0b51a5868f4d5184b6f4ab8a0c5ac4cd'
channel_id = -1001783056428

client = TelegramClient('session_name', api_id, api_hash)
client.start()

# Wczytaj istniejące dane z pliku
existing_data = pd.read_csv('stare_dane.csv')  # Zmień na 'stare_dane.xlsx' jeśli używasz formatu Excel

# Pobierz wcześniejsze wiadomości z kanału
channel_entity = client.get_entity(channel_id)
messages = client(GetHistoryRequest(
    peer=channel_entity,
    limit=100,  # Limit pobieranych wiadomości na żądanie
    offset_date=None,
    offset_id=0,
    max_id=0,
    min_id=0,
    add_offset=0,
    hash=0
))

data = []

for message in messages.messages:
    if message.message:
        text = message.message

        parts = text.split('\n')

        if len(parts) < 6:
            print("Niepoprawny format wiadomości")
            continue

        league = parts[0].strip()
        team_names = parts[1].strip()
        pick_info = parts[2].strip()

        dropping_line = ""
        trend = ""

        for part in parts[3:]:
            if '↓↓↓' in part:
                if 'home:' in part:
                    trend = "↓↓↓ (home)"
                elif 'away:' in part:
                    trend = "↓↓↓ (away)"
                dropping_line = part.split(':')[1].strip()
                break

        data.append({
            'Liga': league,
            'Nazwa drużyn': team_names,
            'Pick': pick_info,
            'Dropping Line': dropping_line,
            'Trend': trend
        })

# Połącz nowe dane z istniejącymi danymi
df = pd.concat([existing_data, pd.DataFrame(data)], ignore_index=True)

# Zapisz dane do pliku CSV lub Excel
df.to_csv('stare_dane.csv', index=False)
df.to_excel('stare_dane.xlsx', index=False)

client.disconnect()
