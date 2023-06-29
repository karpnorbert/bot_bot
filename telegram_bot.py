from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler

# Funkcja obsługująca nowe wiadomości
def handle_message(bot: Bot, update: Update):
    message = update.message
    chat_id = message.chat_id
    text = message.text

    # Przykładowa logika analizy wiadomości
    # Tutaj można umieścić kod do analizy i przetwarzania wiadomości

    # Zapisz wiadomość do pliku CSV
    with open('messages.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([chat_id, text])

# Konfiguracja i uruchomienie bota
def main():
    # Ustawienia bota
    bot_token = 'YOUR_BOT_TOKEN'
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Rejestracja obsługi wiadomości
    message_handler = MessageHandler(Filters.text, handle_message)
    dispatcher.add_handler(message_handler)

    # Uruchomienie bota
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
