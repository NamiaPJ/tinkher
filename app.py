from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import pickle
import os
from flask_bcrypt import Bcrypt
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "super_secret_key"

bcrypt = Bcrypt(app)

# ---------------- LOAD ML MODEL ---------------- #
# (Optional: Not used now, but keeping if needed later)
if os.path.exists("model/nutrition_model.pkl"):
    model = pickle.load(open("model/nutrition_model.pkl", "rb"))
else:
    model = None

# ---------------- DATABASE SETUP ---------------- #

def init_db():
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect("database/users.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ---------------- #

@app.route("/")
def home():
    if "user" in session:
        return render_template("dashboard.html")
    return redirect("/login")

# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = sqlite3.connect("database/users.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "Username already exists!"

    return render_template("register.html")

# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], password):
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid username or password"

    return render_template("login.html")

# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------------- ANALYZE ---------------- #

@app.route("/analyze", methods=["POST"])
def analyze():

    if "user" not in session:
        return redirect("/login")

    leafy = int(request.form["leafy"])
    fruits = int(request.form["fruits"])
    milk = int(request.form["milk"])
    eggs = int(request.form["eggs"])
    meat = int(request.form["meat"])
    pulses = int(request.form["pulses"])
    sunlight = int(request.form["sunlight"])

    # ---------------- DEFICIENCY CHECK ---------------- #

    deficiencies = []
    actions = []

    # Iron
    if leafy < 3:
        deficiencies.append("Iron Deficiency")
        actions.append("Increase spinach, broccoli, and leafy greens.")

    # Calcium
    if milk < 3:
        deficiencies.append("Calcium Deficiency")
        actions.append("Add milk, curd, cheese, or dairy daily.")

    # Vitamin D
    if sunlight < 15:
        deficiencies.append("Vitamin D Deficiency")
        actions.append("Get 20–30 minutes of sunlight exposure daily.")

    # Protein
    if meat < 2 and pulses < 2 and eggs < 2:
        deficiencies.append("Protein Deficiency")
        actions.append("Include eggs, pulses, chicken, or protein-rich foods.")

    # ---------------- SCORE ---------------- #

    score = 100 - (len(deficiencies) * 15)
    if score < 50:
        score = 50

    # ---------------- PERSONALIZED QUOTE ---------------- #

    if not deficiencies:
        quote = "🌟 Amazing! Your nutrition is well balanced. Keep maintaining this healthy lifestyle!"
    else:
        quote = f"⚡ You may have {', '.join(deficiencies)}. Improve your diet to stay healthy!"

    # Store for PDF
    session["last_score"] = score
    session["deficiencies"] = deficiencies
    session["actions"] = actions
    session["quote"] = quote

    return render_template("result.html",
                           overall=score,
                           deficiencies=deficiencies,
                           actions=actions,
                           quote=quote)

# ---------------- PDF DOWNLOAD ---------------- #

@app.route("/download")
def download():

    if "user" not in session:
        return redirect("/login")

    file_path = "nutrition_report.pdf"
    c = canvas.Canvas(file_path)

    c.drawString(100, 800, "Nutrition Health Report")
    c.drawString(100, 770, f"User: {session['user']}")
    c.drawString(100, 750, f"Overall Score: {session.get('last_score', 0)}")

    y = 720

    # Quote
    c.drawString(100, y, "Summary:")
    y -= 20
    c.drawString(120, y, session.get("quote", ""))
    y -= 30

    # Deficiencies
    deficiencies = session.get("deficiencies", [])
    if deficiencies:
        c.drawString(100, y, "Detected Deficiencies:")
        y -= 20
        for d in deficiencies:
            c.drawString(120, y, "- " + d)
            y -= 20

    # Actions
    actions = session.get("actions", [])
    if actions:
        y -= 10
        c.drawString(100, y, "Recommendations:")
        y -= 20
        for a in actions:
            c.drawString(120, y, "- " + a)
            y -= 20

    c.save()

    return send_file(file_path, as_attachment=True)

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)