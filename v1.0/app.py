
from flask import Flask, render_template, request, redirect, url_for,send_from_directory
from models import db, Budget, Player
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fantacalcio.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    budgets = Budget.query.all()
    return render_template('home.html', budgets=budgets)

@app.route('/set_budget', methods=['POST'])
def set_budget():
    for role in ['portieri', 'difensori', 'centrocampisti', 'attaccanti']:
        total_budget = request.form[f'{role}_budget']
        existing_budget = Budget.query.filter_by(role=role).first()
        if existing_budget:
            existing_budget.total_budget = total_budget
            existing_budget.remaining_budget = total_budget
        else:
            new_budget = Budget(role=role, total_budget=total_budget, remaining_budget=total_budget)
            db.session.add(new_budget)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/role/<role>', methods=['GET', 'POST'])
def role_page(role):
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        team = request.form['team']
        cost = int(request.form['cost'])
        budget = Budget.query.filter_by(role=role).first()
        budget.remaining_budget -= cost

        new_player = Player(name=name, surname=surname, role=role, team=team, cost=cost)
        db.session.add(new_player)
        db.session.commit()

    players = Player.query.filter_by(role=role).all()
    budget = Budget.query.filter_by(role=role).first()
    players_left = 3 if role == 'portieri' else 8 if role in ['difensori', 'centrocampisti'] else 6
    players_left -= len(players)
    avg_credit = budget.remaining_budget / players_left if players_left > 0 else 0

    return render_template('role_page.html', players=players, role=role, avg_credit=avg_credit, players_left=players_left)

@app.route('/export')
def export_to_excel():
    # Ottieni tutti i giocatori dal database
    players = Player.query.all()

    # Crea una lista di dizionari con i dati dei giocatori
    data = []
    for player in players:
        data.append({
            "Nome": player.name,
            "Cognome": player.surname,
            "Ruolo": player.role,
            "Squadra": player.team,
            "Crediti": player.cost
        })

    # Crea un DataFrame pandas
    df = pd.DataFrame(data)

    # Percorso per salvare il file Excel
    export_folder = os.path.join('static', 'downloads')
    os.makedirs(export_folder, exist_ok=True)
    file_name = 'lista_giocatori.xlsx'
    file_path = os.path.join(export_folder, file_name)

    # Salva il DataFrame in un file Excel
    df.to_excel(file_path, index=False)

    # Fornisci il file per il download
    return send_from_directory(directory=export_folder, path=file_name)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
