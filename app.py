from flask import Flask, render_template_string, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Simple hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Login Page Template
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:100px;">
    <h2>Admin Panel Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p style="color:red;">{{ error }}</p>
</body>
</html>
"""

# Dashboard Template
dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:50px;">
    <h1>Welcome Admin 👑</h1>
    <p>This is your Admin Dashboard</p>
    <a href="/logout">Logout</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/dashboard")
        else:
            error = "Invalid Credentials"
    return render_template_string(login_page, error=error)

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/")
    return render_template_string(dashboard_page)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
