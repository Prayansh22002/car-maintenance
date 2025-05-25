from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def get_db_connection():
    return psycopg2.connect(config.DATABASE_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users (email, password, first_name, last_name, contact_number, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (email, password, first_name, last_name, contact_number, address))
            conn.commit()
            flash('Registration successful!')
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash('Email already exists.')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Optional: one-time route to initialize DB
@app.route('/initdb')
def initdb():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            contact_number VARCHAR(100),
            address VARCHAR(255)
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()
    return "Database initialized!"



if __name__ == '__main__':
    app.run(debug=True)
