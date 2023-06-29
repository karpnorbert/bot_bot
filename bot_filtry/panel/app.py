from telethon import TelegramClient, events

# Dane uwierzytelniające API Telegram
api_id = '25214343'
api_hash = '0b51a5868f4d5184b6f4ab8a0c5ac4cd'
# ID kanałów
source_channel_id = -1001783056428  # ID źródłowego kanału
target_channel_id = -1001978625110  # ID docelowego kanału

# Tworzenie klienta Telegram
client = TelegramClient('session_name', api_id, api_hash)


@client.on(events.NewMessage(chats=source_channel_id))
async def handle_new_message(event):
    # Pobieranie treści wiadomości
    message_text = event.message.text

    # Kopiowanie wiadomości do docelowego kanału
    await client.send_message(target_channel_id, message_text)


# Uruchamianie klienta Telegram
with client:
    client.run_until_disconnected()
