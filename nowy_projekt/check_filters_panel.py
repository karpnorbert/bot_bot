import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/add_criteria', methods=['GET', 'POST'])
def add_criteria():
    if request.method == 'POST':
        liga = request.form['liga']
        market = request.form['market']

        # Zapisywanie kryteriów filtrowania (np. do pliku, bazy danych)
        # Przykładowo:
        with open(os.path.join(os.path.dirname(__file__), 'panel/kryteria.txt'), 'a') as file:
            file.write(f"Liga: {liga}, Market: {market}\n")

        return 'Kryteria zostały dodane'
    return render_template('add_criteria.html')

if __name__ == '__main__':
    app.run(debug=True)
