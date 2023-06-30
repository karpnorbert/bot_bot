import csv
import pandas as pd
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


# Funkcja obsługująca nowe wiadomości
def handle_message(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = message.chat_id
    text = message.text
    print("received")

    # Przykładowa logika analizy wiadomości
    parts = text.split('\n')

    if len(parts) < 6:
        print("Niepoprawny format wiadomości")
        return

    league = parts[0].strip()
    team_names = parts[1].strip()
    pick_info = parts[2].strip()

    # Sprawdź, czy linia zawiera oczekiwane dane
    dropping_line = ""
    trend = ""

    for part in parts[3:]:
        if '↓↓↓' in part:
            if 'home' in part:
                trend = "↓↓↓ (home)"
            elif 'away' in part:
                trend = "↓↓↓ (away)"
            dropping_line = part.split(':')[1].strip()
            break

    print("League:", league)
    print("Team Names:", team_names)
    print("Pick:", pick_info)
    print("Dropping Line:", dropping_line)
    print("Trend:", trend)

    # Oblicz różnicę procentową
    try:
        dropping_line = float(dropping_line.replace(",", "."))
        previous_dropping_line = pd.read_excel('raport.xlsx')['Dropping Line'].iloc[-1]
        percentage_change = (dropping_line - previous_dropping_line) / previous_dropping_line * 100
    except (FileNotFoundError, IndexError, ValueError):
        percentage_change = None

    print("Percentage Change:", percentage_change)

    # Zapisz dane do pliku Excel
    data = {'Liga': [league], 'Nazwa drużyn': [team_names], 'Pick': [pick_info],
            'Dropping Line': [dropping_line], 'Trend': [trend], 'Percentage Change': [percentage_change]}
    df = pd.DataFrame(data)

    try:
        existing_data = pd.read_excel('raport.xlsx')
        updated_data = pd.concat([existing_data, df], ignore_index=True)
        updated_data.to_excel('raport.xlsx', index=False)
    except FileNotFoundError:
        df.to_excel('raport.xlsx', index=False)

    print("Raport zapisany")


# Konfiguracja i uruchomienie bota
def main():
    # Ustawienia bota
    bot_token = '6299109186:AAFLAV7gGBJsVLQKWV7J_b7ufe8I8Hrn2AU'
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
