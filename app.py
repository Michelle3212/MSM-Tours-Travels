from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/packages")
def packages():
    return render_template("packages.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        conn.execute("INSERT INTO users(name,email,password) VALUES (?,?,?)",
                     (name,email,password))
        conn.commit()
        conn.close()

        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                            (email,password)).fetchone()
        conn.close()

        if user:
            return redirect("/packages")
        else:
            return "Invalid Login"

    return render_template("login.html")

@app.route("/booking", methods=["GET","POST"])
def booking():
    if request.method == "POST":
        name = request.form["name"]
        package = request.form["package"]
        date = request.form["date"]

        conn = get_db()
        conn.execute("INSERT INTO bookings(name,package,date) VALUES (?,?,?)",
                     (name,package,date))
        conn.commit()
        conn.close()

        return "Booking Confirmed! MSM Tours will contact you soon."

    return render_template("booking.html")

@app.route("/contact", methods=["GET","POST"])
def contact(): 
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]

        conn = get_db()
        conn.execute("INSERT INTO messages(name,message) VALUES (?,?)",
                     (name,message))
        conn.commit()
        conn.close()

        return "Message Sent!"

    return render_template("contact.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)