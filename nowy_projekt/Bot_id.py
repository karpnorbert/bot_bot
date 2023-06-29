from telethon.sync import TelegramClient

api_id = '25214343'
api_hash = '0b51a5868f4d5184b6f4ab8a0c5ac4cd'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

for dialog in client.get_dialogs():
    if dialog.is_channel:
        print(f"Channel name: {dialog.name}  ID: {dialog.id}")

client.disconnect()
