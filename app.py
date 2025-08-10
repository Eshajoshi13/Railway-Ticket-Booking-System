from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import config

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config.from_object(config)
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/schedule')
def schedule():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM trains")
    trains = cur.fetchall()
    cur.close()
    return render_template('schedule.html', trains=trains)

@app.route('/arrival')
def arrival():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM trains WHERE type = 'Arrival'")
    trains = cur.fetchall()
    cur.close()
    return render_template('arrival.html', trains=trains)

@app.route('/departure')
def departure():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM trains WHERE type = 'Departure'")
    trains = cur.fetchall()
    cur.close()
    return render_template('departure.html', trains=trains)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('add_train'))
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')

@app.route('/add', methods=['GET', 'POST'])
def add_train():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form['name']
        station = request.form['station']
        time = request.form['time']
        type_ = request.form['type']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO trains(name, station, time, type) VALUES (%s, %s, %s, %s)", (name, station, time, type_))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('schedule'))
    return render_template('add_train.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
