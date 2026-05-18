


import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "wordle_secret_key_999"

WORDS = ["FLASK", "SMART", "WORLD", "SPACE", "CLOUD", "MOUSE", "LOGIC", "CYBER"]

def check_guess(guess, secret):
    result = []
    for i in range(5):
        char = guess[i]
        if char == secret[i]:
            result.append((char, 'correct'))
        elif char in secret:
            result.append((char, 'present'))
        else:
            result.append((char, 'absent'))
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'secret_word' not in session:
        session['secret_word'] = random.choice(WORDS)
        session['attempts'] = []
        session['game_over'] = False
        session['won'] = False

    error = None

    if request.method == 'POST' and not session['game_over']:
        guess = request.form.get('guess', '').upper().strip()

        if len(guess) != 5 or not guess.isalpha():
            error = "Η λέξη πρέπει να έχει ακριβώς 5 γράμματα!"
        else:
            checked = check_guess(guess, session['secret_word'])
            
            attempts = session['attempts']
            attempts.append(checked)
            session['attempts'] = attempts

            if guess == session['secret_word']:
                session['game_over'] = True
                session['won'] = True
            elif len(session['attempts']) >= 6:
                session['game_over'] = True

    return render_template('index.html', 
                           attempts=session['attempts'], 
                           game_over=session['game_over'], 
                           won=session['won'], 
                           secret_word=session['secret_word'],
                           error=error)

@app.route('/reset')
def reset():
    session.pop('secret_word', None)
    session.pop('attempts', None)
    session.pop('game_over', None)
    session.pop('won', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
