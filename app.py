from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# HOME
@app.route("/")
def home():
    conn = get_db()
    reviews = conn.execute("SELECT * FROM reviews").fetchall()
    conn.close()
    return render_template("index.html", reviews=reviews)

# PACKAGES
@app.route("/package/<name>")
def package_detail(name):
    for p in all_packages:
        if p["name"].lower() == name.lower():
            return render_template("package_detail.html", package=p)
    return "Package not found"
    
   all_packages = [
    {
        "name":"Goa",
        "price":"15000",
        "image":"goa.jpg",
        "itinerary":[
            "Day 1: Arrival & Beach visit",
            "Day 2: Water sports & sightseeing",
            "Day 3: Shopping & departure"
        ],
        "inclusions":"Hotel, Breakfast, Transport",
        "exclusions":"Flights, Personal expenses",
        "facilities":"Free WiFi, Pool, AC Rooms"
    },

    {
        "name":"Manali",
        "price":"18000",
        "image":"manali.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Snow activities",
            "Day 3: Solang Valley",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Meals, Transport",
        "exclusions":"Flights",
        "facilities":"Heater, Mountain View"
    }
]
    if search:
        filtered = [p for p in all_packages if search.lower() in p["name"].lower()]
    else:
        filtered = all_packages

    return render_template("packages.html", packages=filtered)

# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        conn = get_db()
        conn.execute("INSERT INTO users(name,email,password) VALUES (?,?,?)",
                     (request.form["name"], request.form["email"], request.form["password"]))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                            (request.form["email"], request.form["password"])).fetchone()
        conn.close()

        if user:
            session["user"] = user["name"]
            return redirect("/")
        else:
            return "Invalid Login"
    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# BOOKING
@app.route("/booking", methods=["GET","POST"])
def booking():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        conn = get_db()
        conn.execute("INSERT INTO bookings(name,package,date) VALUES (?,?,?)",
                     (session["user"], request.form["package"], request.form["date"]))
        conn.commit()
        conn.close()
        return render_template("success.html")
    return render_template("booking.html")

# CONTACT
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        conn = get_db()
        conn.execute("INSERT INTO messages(name,message) VALUES (?,?)",
                     (request.form["name"], request.form["message"]))
        conn.commit()
        conn.close()
        return "Message Sent!"
    return render_template("contact.html")

# REVIEWS
@app.route("/review", methods=["POST"])
def review():
    conn = get_db()
    conn.execute("INSERT INTO reviews(name,review) VALUES (?,?)",
                 (session.get("user","Guest"), request.form["review"]))
    conn.commit()
    conn.close()
    return redirect("/")

# ADMIN LOGIN
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Invalid Admin Login"
    return render_template("admin_login.html")

# ADMIN DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/admin")

    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    bookings = conn.execute("SELECT * FROM bookings").fetchall()
    messages = conn.execute("SELECT * FROM messages").fetchall()
    conn.close()

    return render_template("admin.html", users=users, bookings=bookings, messages=messages)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 