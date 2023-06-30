  GNU nano 6.4                                          app.py                                                   
import re
from telethon import TelegramClient, events

# Dane uwierzytelniające API Telegram
api_id = '25214343'
api_hash = '0b51a5868f4d5184b6f4ab8a0c5ac4cd'

# ID kanału źródłowego i docelowego
source_channel_id = -1001783056428  # ID źródłowego kanału
target_channel_id = -1001978625110  # ID docelowego kanału
# Minimalna wartość "Drop Value"
min_drop_value = 15

# Tworzenie klienta Telegram
client = TelegramClient('session_name', api_id, api_hash)


@client.on(events.NewMessage(chats=source_channel_id))
async def handle_new_message(event):
    # Pobieranie treści wiadomości
    message_text = event.message.text

    # Wyszukiwanie wartości "Drop Value" za pomocą wyrażenia regularnego
    pattern = r'Drop value:\s*(\d+(?:\.\d+)?(?:,\d+)?%)'
    match = re.search(pattern, message_text)

    if match:
        drop_value_str = match.group(1)
        drop_value_str = drop_value_str.replace(',', '.')  # Zamiana przecinków na kropki
        try:
            drop_value = float(drop_value_str[:-1])
            if drop_value >= min_drop_value:
                # Kopiowanie wiadomości do docelowego kanału
                await client.send_message(target_channel_id, message_text)
        except ValueError:
            pass


# Uruchamianie klienta Telegram
with client:
    client.run_until_disconnected()



#drop 15% ustalon
