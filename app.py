from flask import Flask, request, redirect, session
import sqlite3
import os
import uuid
import hashlib

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "database.db"

# Background Image URL (Change if you want)
BG_IMAGE = "https://images.unsplash.com/photo-1508780709619-79562169bc64"

# ---------------- PASSWORD HASH ----------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- DATABASE SETUP ----------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  license_key TEXT,
                  approved INTEGER DEFAULT 0)''')

    c.execute('''CREATE TABLE IF NOT EXISTS admin
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT)''')

    c.execute("DELETE FROM admin")
    c.execute("INSERT INTO admin (username, password) VALUES (?, ?)",
              ("admin", hash_password("1234")))

    conn.commit()
    conn.close()

init_db()

# ---------------- COMMON STYLE ----------------

def page_style(content):
    return f"""
    <html>
    <head>
    <style>
    body {{
        background-image: url('{BG_IMAGE}');
        background-size: cover;
        background-position: center;
        font-family: Arial;
        color: white;
        text-align: center;
        margin-top: 100px;
        background-attachment: fixed;
    }}
    .box {{
        background: rgba(0,0,0,0.7);
        padding: 30px;
        border-radius: 15px;
        display: inline-block;
    }}
    input, button {{
        padding: 10px;
        margin: 5px;
        border-radius: 8px;
        border: none;
    }}
    button {{
        background: #00c6ff;
        color: white;
        cursor: pointer;
    }}
    a {{ color: #00ffcc; }}
    </style>
    </head>
    <body>
    <div class="box">
    {content}
    </div>
    </body>
    </html>
    """

# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])
        key = str(uuid.uuid4())[:8]

        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("INSERT INTO users (username,password,license_key,approved) VALUES (?,?,?,0)",
                      (username, password, key))
            conn.commit()
            conn.close()

            return page_style(f"""
            <h3>Registration Successful ✅</h3>
            <p>Your License Key: <b>{key}</b></p>
            <p>Send this key to Admin for approval.</p>
            <a href="/">Go to Login</a>
            """)
        except:
            return page_style("Username already exists ❌")

    return page_style("""
    <h2>Register</h2>
    <form method="POST">
    <input name="username" placeholder="Username" required><br>
    <input name="password" type="password" placeholder="Password" required><br>
    <button type="submit">Register</button>
    </form>
    <br>
    <a href="/">Login</a>
    """)

# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=? AND approved=1",
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return page_style("Not approved or wrong credentials ❌")

    return page_style("""
    <h2>Login</h2>
    <form method="POST">
    <input name="username" required><br>
    <input name="password" type="password" required><br>
    <button type="submit">Login</button>
    </form>
    <br>
    <a href="/register">Register</a>
    """)

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/")
    return page_style(f"""
    <h2>Welcome {session['user']} 👑</h2>
    <p>Your account is approved ✅</p>
    <a href="/logout">Logout</a>
    """)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- ADMIN LOGIN ----------------

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?",
                  (username, password))
        admin = c.fetchone()
        conn.close()

        if admin:
            session["admin"] = True
            return redirect("/admin_panel")
        else:
            return page_style("Wrong Admin Login ❌")

    return page_style("""
    <h2>Admin Login</h2>
    <form method="POST">
    <input name="username" required><br>
    <input name="password" type="password" required><br>
    <button type="submit">Login</button>
    </form>
    """)

# ---------------- ADMIN PANEL ----------------

@app.route("/admin_panel")
def admin_panel():
    if not session.get("admin"):
        return redirect("/admin")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, username, license_key, approved FROM users")
    users = c.fetchall()
    conn.close()

    html = "<h2>Admin Panel 🔐</h2><br>"

    for u in users:
        html += f"<b>{u[1]}</b> | Key: {u[2]} | "
        if u[3] == 0:
            html += f"<a href='/approve/{u[0]}'>Approve</a>"
        else:
            html += "Approved ✅"
        html += "<br><br>"

    html += "<br><a href='/admin_logout'>Logout</a>"
    return page_style(html)

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
