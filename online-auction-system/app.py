from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def index():
    db = get_db()
    auctions = db.execute("SELECT * FROM auctions").fetchall()
    return render_template("index.html", auctions=auctions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        db.commit()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)).fetchone()
        if user:
            session['user'] = u
            return redirect('/')
    return render_template("login.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        end_time = datetime.now() + timedelta(minutes=2)

        db = get_db()
        db.execute("INSERT INTO auctions (title, price, end_time) VALUES (?, ?, ?)",
                   (title, price, end_time))
        db.commit()
        return redirect('/')
    return render_template("create_auction.html")

@app.route('/bid/<int:id>', methods=['POST'])
def bid(id):
    bid_amount = int(request.form['bid'])
    db = get_db()
    auction = db.execute("SELECT * FROM auctions WHERE id=?", (id,)).fetchone()

    if bid_amount > auction[2]:
        end_time = datetime.strptime(auction[3], "%Y-%m-%d %H:%M:%S.%f")

        # Anti-sniping
        if (end_time - datetime.now()).seconds < 30:
            end_time += timedelta(seconds=30)

        db.execute("UPDATE auctions SET price=?, end_time=? WHERE id=?",
                   (bid_amount, end_time, id))
        db.commit()

    return redirect('/')

app.run(debug=True)