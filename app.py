from flask import Flask, render_template_string, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "change_this_secret_key_123"

ADMIN_USERNAME = "99YU5H"
ADMIN_PASSWORD = "DWN"

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin Login</title>

<style>
*{
box-sizing:border-box;
margin:0;
padding:0;
}

body{
font-family:monospace;
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
top:50%;
left:50%;
min-width:100%;
min-height:100%;
width:auto;
height:auto;
transform:translate(-50%,-50%);
object-fit:cover;
z-index:-2;
filter: blur(1.5px) brightness(0.85);
}

/* Light Overlay */
body::before{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.25);
z-index:-1;
}

/* Mobile Fix */
@media (max-width:768px){
#bg-video{
width:100%;
height:100%;
object-fit:cover;
}
}

/* Glass Login Box */
.login-box{
background:rgba(0,0,0,0.55);
padding:30px;
border-radius:15px;
box-shadow:0 0 20px cyan;
text-align:center;
width:90%;
max-width:350px;
backdrop-filter: blur(3px);
}

h2{
color:cyan;
text-shadow:0 0 10px cyan;
margin-bottom:20px;
}

input{
width:100%;
padding:12px;
margin:10px 0;
border:none;
border-radius:8px;
background:rgba(0,0,0,0.6);
color:white;
box-shadow:0 0 10px cyan inset;
}

button{
width:100%;
padding:12px;
background:cyan;
border:none;
border-radius:8px;
font-weight:bold;
cursor:pointer;
}

.error{
color:red;
margin-top:10px;
}

.sound-msg{
position:absolute;
bottom:15px;
width:100%;
text-align:center;
font-size:12px;
opacity:0.9;
}
</style>
</head>

<body>

<video id="bg-video" autoplay loop muted playsinline>
<source src="/static/VID-20260215-WA0074.mp4" type="video/mp4">
</video>

<div class="login-box">
<h2>🔐 ADMIN PANEL</h2>
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
color:cyan;
margin-bottom:30px;
}
a{
display:block;
width:90%;
max-width:300px;
margin:15px auto;
padding:15px;
background:cyan;
color:black;
text-decoration:none;
border-radius:10px;
font-weight:bold;
}
.logout{
background:red;
color:white;
}
</style>
</head>
<body>

<h1>WELCOME ADMIN</h1>
<a href="/logout" class="logout">LOGOUT</a>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/dashboard")
        else:
            error = "Invalid Username or Password"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/")
    return render_template_string(DASHBOARD)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
