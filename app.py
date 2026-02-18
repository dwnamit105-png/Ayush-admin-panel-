from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import os
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = "change_this_secret"

DATABASE = "database.db"

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    license_key TEXT,
                    approved INTEGER DEFAULT 0
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )''')

    # Default Admin
    c.execute("SELECT * FROM admin WHERE username='admin'")
    if not c.fetchone():
        admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO admin (username,password) VALUES (?,?)",
                  ("admin", admin_pass))

    conn.commit()
    conn.close()

init_db()

# ---------------- HASH FUNCTION ----------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- USER REGISTER ----------------

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])
        key = str(uuid.uuid4())[:8]

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username,password,license_key) VALUES (?,?,?)",
                      (username,password,key))
            conn.commit()
        except:
            return "Username already exists"
        conn.close()

        return f"Your Key: {key} <br>Send this key to Admin for approval."

    return '''
    <h2>Register</h2>
    <form method="POST">
    <input name="username" placeholder="Username" required><br><br>
    <input name="password" type="password" placeholder="Password" required><br><br>
    <button type="submit">Register</button>
    </form>
    '''

# ---------------- USER LOGIN ----------------

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=? AND approved=1",
                  (username,password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Not approved or wrong credentials"

    return '''
    <h2>Login</h2>
    <form method="POST">
    <input name="username" required><br><br>
    <input name="password" type="password" required><br><br>
    <button type="submit">Login</button>
    </form>
    <br>
    <a href="/register">Register</a>
    '''

# ---------------- USER DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/")
    return f"Welcome {session['user']} 👑 <br><a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- ADMIN PANEL ----------------

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?",
                  (username,password))
        admin = c.fetchone()
        conn.close()

        if admin:
            session["admin"] = True
            return redirect("/admin_panel")
        else:
            return "Wrong admin login"

    return '''
    <h2>Admin Login</h2>
    <form method="POST">
    <input name="username"><br><br>
    <input name="password" type="password"><br><br>
    <button type="submit">Login</button>
    </form>
    '''

@app.route("/admin_panel")
def admin_panel():
    if not session.get("admin"):
        return redirect("/admin")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id,username,license_key,approved FROM users")
    users = c.fetchall()
    conn.close()

    html = "<h2>Admin Panel</h2><ul>"
    for u in users:
        status = "Approved" if u[3]==1 else f"<a href='/approve/{u[0]}'>Approve</a>"
        html += f"<li>{u[1]} - {u[2]} - {status}</li>"
    html += "</ul><a href='/admin_logout'>Logout</a>"
    return html

@app.route("/approve/<int:user_id>")
def approve(user_id):
    if not session.get("admin"):
        return redirect("/admin")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE users SET approved=1 WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return redirect("/admin_panel")

@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect("/admin")

# ---------------- RUN ----------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
