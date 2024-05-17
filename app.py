from flask import Flask, render_template, redirect, url_for, request, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    credits = db.Column(db.Integer, nullable=False, default=0)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    event = db.relationship('Event', backref=db.backref('reservations', lazy=True))

# Crée la base de données et les tables si elles n'existent pas
if not os.path.exists('site.db'):
    with app.app_context():
        db.create_all()

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.context_processor
def inject_user():
    return dict(user=g.user)

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=16)
        credits = 100  # Par exemple, chaque utilisateur commence avec 100 crédits
        new_user = User(username=username, password=password, credits=credits)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        if user.credits >= event.price:
            user.credits -= event.price
            new_reservation = Reservation(user_id=user.id, event_id=event.id)
            db.session.add(new_reservation)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('event.html', event=event)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        new_event = Event(name=name, description=description, price=price)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_event.html')

@app.route('/my_reservations')
def my_reservations():
    if not g.user:
        return redirect(url_for('login'))
    reservations = Reservation.query.filter_by(user_id=g.user.id).all()
    return render_template('my_reservations.html', reservations=reservations)

if __name__ == '__main__':
    app.run(debug=True)
