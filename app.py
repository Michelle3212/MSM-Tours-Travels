from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
import random
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# ================= EMAIL CONFIG =================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'msmtoursandtravels2026@gmail.com'
app.config['MAIL_PASSWORD'] = 'thixyxqdkhcqfmoq'

mail = Mail(app)

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= OTP STORE =================
otp_store = {}

# ================= PACKAGES =================
all_packages = [
    {"name":"Kerala Boathouse","slug":"kerala-boathouse","price":"25000","image":"boathouse.jpg"},
    {"name":"Dubai","slug":"dubai","price":"60000","image":"dubai.jpg"},
    {"name":"Maldives","slug":"maldives","price":"90000","image":"maldives.jpg"}
]

# ================= HOME =================
@app.route("/")
def home():
    conn = get_db()
    reviews = conn.execute("SELECT * FROM reviews").fetchall()
    conn.close()
    return render_template("index.html", reviews=reviews)

# ================= SEND OTP =================
@app.route("/send-otp", methods=["GET","POST"])
def send_otp():
    if request.method == "POST":
        email = request.form["email"]

        otp = str(random.randint(100000,999999))
        otp_store[email] = otp

        msg = Message("MSM Tours OTP",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f"Your OTP is {otp}"

        mail.send(msg)

        return render_template("verify_otp.html", email=email)

    return render_template("send_otp.html")

# ================= VERIFY OTP =================
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    email = request.form["email"]
    user_otp = request.form["otp"]

    if otp_store.get(email) == user_otp:
        session["verified_email"] = email
        return redirect("/set-password")
    else:
        return "Invalid OTP"

# ================= SET PASSWORD =================
@app.route("/set-password", methods=["GET","POST"])
def set_password():
    if request.method == "POST":
        name = request.form["name"]
        password = generate_password_hash(request.form["password"])
        email = session.get("verified_email")

        conn = get_db()
        conn.execute("INSERT INTO users(name,email,password) VALUES (?,?,?)",
                     (name,email,password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("set_password.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?",
                            (request.form["email"],)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], request.form["password"]):
            session["user"] = user["name"]
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")

# ================= BOOKING =================
@app.route("/booking", methods=["GET","POST"])
def booking():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        package = request.form["package"]
        date = request.form["date"]
        message = request.form["message"]

        conn = get_db()
        conn.execute("""
        INSERT INTO bookings(name,email,phone,package,date,message)
        VALUES (?,?,?,?,?,?)
        """,(name,email,phone,package,date,message))
        conn.commit()
        conn.close()

        # EMAIL TO ADMIN
        msg = Message("New Booking",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])

        msg.body = f"""
New Booking!

Name: {name}
Email: {email}
Phone: {phone}
Package: {package}
Date: {date}
Message: {message}
"""

        mail.send(msg)

        return render_template("success.html", name=name, package=package, date=date)

    return render_template("booking.html", packages=all_packages)

# ================= ADMIN =================
@app.route("/admin-login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return render_template("admin_login.html", error="Invalid")

    return render_template("admin_login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    bookings = conn.execute("SELECT * FROM bookings").fetchall()
    conn.close()

    return render_template("admin.html", users=users, bookings=bookings)

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)  