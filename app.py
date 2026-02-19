from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey123"

ADMIN_USERNAME = "99YU5H"
ADMIN_PASSWORD = "DWN"

# ================= PREMIUM LOGIN PAGE =================
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>AYUSH SHRIVASTAVA WEB - Admin Login</title>
<style>
body {
    margin:0;
    padding:0;
    font-family: 'Consolas', monospace;
    background: linear-gradient(45deg, #000000, #0f0f0f, #000000);
    background-size: 400% 400%;
    animation: bgAnimation 10s infinite alternate;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    color:white;
}

@keyframes bgAnimation {
    0% { background-position: left; }
    100% { background-position: right; }
}

.login-box {
    background: rgba(0,0,0,0.7);
    padding:40px;
    border-radius:15px;
    box-shadow: 0 0 20px cyan, 0 0 40px #00ffff;
    text-align:center;
    width:300px;
}

h2 {
    margin-bottom:20px;
    color:#00ffff;
    text-shadow:0 0 10px #00ffff, 0 0 20px #00ffff;
}

input {
    width:100%;
    padding:10px;
    margin:10px 0;
    border:none;
    border-radius:8px;
    outline:none;
    background:black;
    color:white;
    box-shadow:0 0 10px #00ffff inset;
}

button {
    width:100%;
    padding:10px;
    background:#00ffff;
    border:none;
    border-radius:8px;
    font-weight:bold;
    cursor:pointer;
    transition:0.3s;
}

button:hover {
    background:#00cccc;
    box-shadow:0 0 20px #00ffff;
}

.error {
    color:red;
    margin-top:10px;
}
</style>
</head>
<body>

<div class="login-box">
<h2>🔐 AYUSH SHRIVASTAVA WEB</h2>
<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">LOGIN</button>
</form>
<div class="error">{{ error }}</div>
</div>

</body>
</html>
"""

# ================= PREMIUM DASHBOARD =================
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
<title>AYUSH SHRIVASTAVA WEB - Dashboard</title>
<style>
body {
    background:black;
    color:white;
    font-family:monospace;
    text-align:center;
    padding:40px;
}

h1 {
    color:#00ffff;
    text-shadow:0 0 15px #00ffff, 0 0 30px #00ffff;
    margin-bottom:40px;
}

.btn {
    display:block;
    width:300px;
    margin:15px auto;
    padding:15px;
    background:#00ffff;
    color:black;
    text-decoration:none;
    border-radius:10px;
    font-weight:bold;
    transition:0.3s;
    box-shadow:0 0 20px #00ffff;
}

.btn:hover {
    background:#00cccc;
    transform:scale(1.05);
    box-shadow:0 0 40px #00ffff;
}

.logout {
    background:red;
    color:white;
    box-shadow:0 0 20px red;
}

.logout:hover {
    background:#cc0000;
    box-shadow:0 0 40px red;
}
</style>
</head>
<body>

<h1>💖 AYUSH SHRIVASTAVA WEB 💖</h1>

<a href="/convo-server" class="btn">🚀 CONVO SERVER</a>
<a href="/youtube-dl" class="btn">📥 YOUTUBE DOWNLOADER</a>
<a href="/logout" class="btn logout">🔓 LOGOUT</a>

</body>
</html>
"""

# ================= ROUTES =================
@app.route('/login', methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("home"))
        else:
            error = "Invalid Username or Password!"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route('/')
def home():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template_string(HTML_CONTENT)

@app.route('/convo-server')
def convo_server():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return "<h1 style='color:cyan;text-align:center;'>🚀 CONVO SERVER Activated!</h1>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
