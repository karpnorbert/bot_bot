import logging
from flask import Flask, render_template, request
from telethon.sync import TelegramClient
from telethon.tl.types import Message
import asyncio

app = Flask(__name__)

# Dane uwierzytelniające API Telegram
api_id = '25214343'
api_hash = '0b51a5868f4d5184b6f4ab8a0c5ac4cd'

# ID kanału źródłowego i docelowego
source_channel_id = -1001783056428  # ID źródłowego kanału
target_channel_id = -1001978625110  # ID docelowego kanału

# Konfiguracja logów
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_criteria', methods=['GET', 'POST'])
def add_criteria():
    if request.method == 'POST':
        drop_value = int(request.form['drop_value']) if request.form['drop_value'] else 0

        # Zapisywanie kryterium filtrowania (np. do pliku, bazy danych)
        with open('kryterium.txt', 'w') as file:
            file.write(f"Procentowa wartość: {drop_value}\n")

        # Uruchamianie funkcji filtrowania i kopiowania wiadomości w nowej pętli zdarzeń asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(filter_and_copy_messages(drop_value))
        loop.close()

        return 'Kryterium zostało dodane i bot został uruchomiony'

    return render_template('add_criteria.html')

async def filter_and_copy_messages(drop_value):
    # Tworzenie klienta Telegram
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Pobieranie wiadomości z kanału źródłowego i filtrowanie na podstawie kryterium
        async for message in client.iter_messages(source_channel_id):
            if not isinstance(message, Message):
                continue

            # Filtrowanie na podstawie kryterium
            if getattr(message, 'drop_value', 0) >= drop_value:
                logging.debug(f"Przekazywanie wiadomości: {message.text}")
                print(f"Przekazywanie wiadomości: {message.text}")

                await client.forward_messages(target_channel_id, [message])
                logging.debug(f"Skopiowano wiadomość do docelowego kanału: {message.text}")
                print(f"Skopiowano wiadomość do docelowego kanału: {message.text}")

@app.route('/send_test_message')
def send_test_message():
    asyncio.run(send_test_message_async())
    return 'Wiadomość testowa została wysłana na docelowy kanał'

async def send_test_message_async():
    # Tworzenie klienta Telegram
    async with TelegramClient('session_name', api_id, api_hash) as client:
        message = await client.send_message(target_channel_id, 'Testowa wiadomość')
        logging.debug(f"Wysłano testową wiadomość: {message.text}")
        print(f"Wysłano testową wiadomość: {message.text}")

if __name__ == '__main__':
    app.run(debug=True)
