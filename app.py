from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="user_db"
    )

@app.route('/index')
def index():
    return render_template('index1.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `email` = %s AND `password` = %s", (email, password))
    users = cursor.fetchall()
    db.close()

    if len(users) > 0:
        return redirect('/index')
    else:
        return redirect('/login')

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('uname')
        email = request.form.get('uemail')
        password = request.form.get('upassword')

        # Check if any of the form fields are empty
        if not name or not email or not password:
            return "All fields are required. Please go back and fill in all fields."

        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute("INSERT INTO `users` (`name`, `email`, `password`) VALUES (%s, %s, %s)", (name, email, password))
            db.commit()
            return "User registered successfully"
        except mysql.connector.Error as err:
            db.rollback()  # Rollback in case of error
            return f"Error: {err}"
        finally:
            db.close()
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

