from flask import Flask, render_template_string, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = "super_secure_secret_key_change_this"

ADMIN_USERNAME = "99YU5H"
ADMIN_PASSWORD = "DWN"

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AYUSH SHRIVASTAVA WEB - Admin Login</title>

<style>
*{
box-sizing:border-box;
margin:0;
padding:0;
}

body{
font-family:'Consolas',monospace;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
color:white;
overflow:hidden;
background:black;
}

/* Background Video */
#bg-video{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
object-fit:cover;
z-index:-2;
filter: blur(4px) brightness(0.6);
}

/* Overlay */
body::before{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.5);
z-index:-1;
}

.login-box{
background:rgba(0,0,0,0.75);
padding:30px;
border-radius:15px;
box-shadow:0 0 25px #00ffff;
text-align:center;
width:90%;
max-width:350px;
}

h2{
color:#00ffff;
text-shadow:0 0 15px #00ffff;
margin-bottom:20px;
font-size:20px;
}

input{
width:100%;
padding:12px;
margin:10px 0;
border:none;
border-radius:8px;
background:black;
color:white;
font-size:14px;
box-shadow:0 0 10px #00ffff inset;
}

button{
width:100%;
padding:12px;
background:#00ffff;
border:none;
border-radius:8px;
font-weight:bold;
cursor:pointer;
font-size:14px;
transition:0.3s;
}

button:hover{
background:#00cccc;
box-shadow:0 0 20px #00ffff;
}

.error{
color:red;
margin-top:10px;
font-size:13px;
}

.sound-msg{
position:absolute;
bottom:15px;
width:100%;
text-align:center;
font-size:12px;
opacity:0.8;
}
</style>
</head>

<body>

<video id="bg-video" autoplay loop muted playsinline>
<source src="{{ url_for('static', filename='bg.mp4') }}" type="video/mp4">
</video>

<div class="login-box">
<h2>🔐 AYUSH SHRIVASTAVA WEB</h2>
<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">LOGIN</button>
</form>
<div class="error">{{ error }}</div>
</div>

<div class="sound-msg">Tap anywhere to enable sound 🔊</div>

<script>
const video = document.getElementById("bg-video");

document.body.addEventListener("click", function() {
    video.muted = false;
    video.play();
}, { once: true });
</script>

</body>
</html>
"""

DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard</title>

<style>
body{
background:black;
color:white;
font-family:monospace;
text-align:center;
padding:40px;
}

h1{
color:#00ffff;
text-shadow:0 0 20px #00ffff;
margin-bottom:30px;
}

.btn{
display:block;
width:90%;
max-width:300px;
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

.btn:hover{
background:#00cccc;
transform:scale(1.05);
}

.logout{
background:red;
color:white;
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

@app.route("/login", methods=["GET","POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/")
        else:
            error = "Invalid Username or Password!"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route("/")
def home():
    if not session.get("admin"):
        return redirect("/login")
    return render_template_string(DASHBOARD)

@app.route("/convo-server")
def convo():
    if not session.get("admin"):
        return redirect("/login")
    return "<h1 style='color:cyan;text-align:center;'>🚀 CONVO SERVER Activated!</h1>"

@app.route("/youtube-dl")
def yt():
    if not session.get("admin"):
        return redirect("/login")
    return "<h1 style='color:cyan;text-align:center;'>📥 YouTube Downloader Page</h1>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
