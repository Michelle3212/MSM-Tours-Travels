from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= PACKAGES =================
all_packages = [
    {"name":"Kerala Boathouse","slug":"kerala-boathouse","price":"25000","image":"boathouse.jpg",
     "itinerary":["Day 1: Arrival","Day 2: Houseboat","Day 3: Departure"],
     "inclusions":"Houseboat, Meals","exclusions":"Flights","facilities":"Luxury Boat"},

    {"name":"Dubai","slug":"dubai","price":"60000","image":"dubai.jpg",
     "itinerary":["Day 1: Arrival","Day 2: City Tour","Day 3: Safari"],
     "inclusions":"Hotel","exclusions":"Flights","facilities":"Luxury Stay"},

    {"name":"Maldives","slug":"maldives","price":"90000","image":"maldives.jpg",
     "itinerary":["Day 1: Arrival","Day 2: Resort","Day 3: Water Sports"],
     "inclusions":"Resort","exclusions":"Flights","facilities":"Private Beach"}
]

# ================= HOME =================
@app.route("/")
def home():
    conn = get_db()
    reviews = conn.execute("SELECT * FROM reviews").fetchall()
    conn.close()
    return render_template("index.html", reviews=reviews)

# ================= PACKAGES =================
@app.route("/packages")
def packages():
    search = request.args.get("search")

    if search:
        filtered = [p for p in all_packages if search.lower() in p["name"].lower()]
    else:
        filtered = all_packages

    return render_template("packages.html", packages=filtered)

# ================= PACKAGE DETAIL =================
@app.route("/package/<slug>")
def package_detail(slug):
    for p in all_packages:
        if p["slug"] == slug:
            return render_template("package_detail.html", package=p)
    return "Package not found"

# ================= REGISTER =================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        conn = get_db()

        hashed_pw = generate_password_hash(request.form["password"])

        conn.execute(
            "INSERT INTO users(name,email,password) VALUES (?,?,?)",
            (request.form["name"], request.form["email"], hashed_pw)
        )
        conn.commit()
        conn.close()

        return render_template("register.html", success=True)

    return render_template("register.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (request.form["email"],)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], request.form["password"]):
            session["user"] = user["name"]
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("admin", None)
    return redirect("/")

# ================= BOOKING =================
@app.route("/booking", methods=["GET","POST"])
def booking():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        package = request.form["package"]
        date = request.form["date"]

        conn = get_db()
        conn.execute(
            "INSERT INTO bookings(name,package,date) VALUES (?,?,?)",
            (name, package, date)
        )
        conn.commit()
        conn.close()

        return render_template("success.html", name=name, package=package, date=date)

    return render_template("booking.html", packages=all_packages)

# ================= CONTACT =================
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO messages(name,message) VALUES (?,?)",
            (request.form["name"], request.form["message"])
        )
        conn.commit()
        conn.close()

        return render_template("contact.html", success=True)

    return render_template("contact.html")

# ================= REVIEWS =================
@app.route("/review", methods=["POST"])
def review():
    conn = get_db()
    conn.execute(
        "INSERT INTO reviews(name,review) VALUES (?,?)",
        (session.get("user","Guest"), request.form["review"])
    )
    conn.commit()
    conn.close()
    return redirect("/")

# ================= ADMIN LOGIN =================
@app.route("/admin-login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")

# ================= ADMIN DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    bookings = conn.execute("SELECT * FROM bookings").fetchall()
    messages = conn.execute("SELECT * FROM messages").fetchall()
    conn.close()

    return render_template("admin.html", users=users, bookings=bookings, messages=messages)

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)