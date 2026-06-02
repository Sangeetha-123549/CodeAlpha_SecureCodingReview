from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secure_key_123"

# ---------------- STORAGE ----------------
users = {}

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

# create uploads folder automatically
os.makedirs("uploads", exist_ok=True)


# ---------------- CHECK FILE TYPE ----------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- HOME FIX (404 FIX) ----------------
@app.route("/")
def home():
    return redirect("/register")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            msg = "User already exists ❌"
        else:
            users[username] = generate_password_hash(password)
            return redirect("/login")

    return render_template("register.html", msg=msg)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect("/dashboard")
        else:
            msg = "Invalid credentials ❌"

    return render_template("login.html", msg=msg)


# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    msg = ""

    if request.method == "POST":
        file = request.files["file"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            msg = "File uploaded successfully ✅"
        else:
            msg = "Invalid file type ❌"

    return render_template("dashboard.html", user=session["user"], msg=msg)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)