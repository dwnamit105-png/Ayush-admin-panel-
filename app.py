from flask import Flask, render_template_string, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secretkey123"
DATABASE = "database.db"

# ---------------- DATABASE INIT ---------------- #

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS admin
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS keys
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  license_key TEXT,
                  approved INTEGER DEFAULT 0)''')

    # Always reset admin
    c.execute("DELETE FROM admin")
    c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "1234"))

    conn.commit()
    conn.close()

if not os.path.exists(DATABASE):
    init_db()
else:
    init_db()   # Force recreate admin every deploy

# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template_string("""
    <h2>Send License Key</h2>
    <form method="POST" action="/submit_key">
        <input name="key" placeholder="Enter License Key" required>
        <button type="submit">Submit</button>
    </form>
    <br>
    <a href="/login">Admin Login</a>
    """)

# ---------------- SUBMIT KEY ---------------- #

@app.route("/submit_key", methods=["POST"])
def submit_key():
    key = request.form["key"]

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO keys (license_key) VALUES (?)", (key,))
    conn.commit()
    conn.close()

    return "Key Submitted! Wait for approval."

# ---------------- ADMIN LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()

        if admin:
            session["admin"] = True
            return redirect("/admin")
        else:
            return "Wrong Admin Login ❌"

    return render_template_string("""
    <h2>Admin Login</h2>
    <form method="POST">
        <input name="username" placeholder="Username" required><br><br>
        <input name="password" type="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    """)

# ---------------- ADMIN PANEL ---------------- #

@app.route("/admin")
def admin_panel():
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM keys")
    keys = c.fetchall()
    conn.close()

    html = "<h2>Admin Panel</h2>"
    html += "<a href='/logout'>Logout</a><br><br>"

    for k in keys:
        status = "Approved ✅" if k[2] == 1 else "Pending ❌"
        html += f"""
        <p>
        {k[1]} - {status}
        """

        if k[2] == 0:
            html += f"<a href='/approve/{k[0]}'>Approve</a>"

        html += "</p><hr>"

    return html

# ---------------- APPROVE KEY ---------------- #

@app.route("/approve/<int:id>")
def approve_key(id):
    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE keys SET approved=1 WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
