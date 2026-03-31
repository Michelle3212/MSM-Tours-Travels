from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= PACKAGES DATA =================
all_packages = [

    {
        "name":"Kerala Boathouse",
        "price":"25000",
        "image":"boathouse.jpg",
        "itinerary":[
            "Day 1: Arrival in Alleppey",
            "Day 2: Houseboat stay",
            "Day 3: Backwater cruise & departure"
        ],
        "inclusions":"Houseboat, Meals, Sightseeing",
        "exclusions":"Flights",
        "facilities":"Luxury Boat, AC Rooms"
    },

    {
        "name":"Rajasthan",
        "price":"30000",
        "image":"rajasthan.jpg",
        "itinerary":[
            "Day 1: Jaipur visit",
            "Day 2: Udaipur sightseeing",
            "Day 3: Desert safari",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Transport",
        "exclusions":"Flights",
        "facilities":"Desert Camp, Cultural Shows"
    },

    {
        "name":"Paris",
        "price":"120000",
        "image":"paris.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Eiffel Tower & city tour",
            "Day 3: Museums & shopping",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Visa, Breakfast",
        "exclusions":"Flights",
        "facilities":"Luxury Stay, Guide"
    },

    {
        "name":"Singapore",
        "price":"80000",
        "image":"singapore.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Universal Studios",
            "Day 3: City tour",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Transport",
        "exclusions":"Flights",
        "facilities":"City Tour, Theme Parks"
    },

    {
        "name":"Dubai",
        "price":"60000",
        "image":"dubai.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: City tour",
            "Day 3: Desert safari",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Visa, Transport",
        "exclusions":"Flights",
        "facilities":"Luxury Stay, Safari"
    },

    {
        "name":"Ooty",
        "price":"15000",
        "image":"ooty.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Botanical Garden",
            "Day 3: Lake visit",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Breakfast",
        "exclusions":"Transport",
        "facilities":"Hill View, Cool Climate"
    },

    {
        "name":"Coorg",
        "price":"20000",
        "image":"coorg.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Coffee estates",
            "Day 3: Abbey Falls",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel",
        "exclusions":"Transport",
        "facilities":"Nature Stay"
    },

    {
        "name":"Odisha",
        "price":"22000",
        "image":"odishawild.jpg",
        "itinerary":[
            "Day 1: Puri visit",
            "Day 2: Konark Sun Temple",
            "Day 3: Chilika Lake",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Transport",
        "exclusions":"Flights",
        "facilities":"Temple Tour, Beach"
    },

    {
        "name":"Maldives",
        "price":"90000",
        "image":"maldives.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Beach & resort stay",
            "Day 3: Water activities",
            "Day 4: Departure"
        ],
        "inclusions":"Resort, Meals",
        "exclusions":"Flights",
        "facilities":"Private Beach, Water Villa"
    },

    {
        "name":"Vietnam",
        "price":"70000",
        "image":"vietnam.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: City tour",
            "Day 3: Cruise experience",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Guide",
        "exclusions":"Flights",
        "facilities":"Cruise, Cultural Tour"
    },

    {
        "name":"Mysore",
        "price":"12000",
        "image":"mysore.jpg",
        "itinerary":[
            "Day 1: Palace visit",
            "Day 2: Zoo & gardens",
            "Day 3: Departure"
        ],
        "inclusions":"Hotel",
        "exclusions":"Transport",
        "facilities":"City Tour"
    },

    {
        "name":"Hampi Karnataka",
        "price":"14000",
        "image":"hampi.jpg",
        "itinerary":[
            "Day 1: Temple visit",
            "Day 2: Heritage sites",
            "Day 3: Departure"
        ],
        "inclusions":"Hotel",
        "exclusions":"Transport",
        "facilities":"Historical Tour"
    }

]

# ================= HOME =================
@app.route("/")
def home():
    conn = get_db()
    reviews = conn.execute("SELECT * FROM reviews").fetchall()
    conn.close()
    return render_template("index.html", reviews=reviews)

# ================= PACKAGES PAGE =================
@app.route("/packages")
def packages():
    search = request.args.get("search")

    if search:
        filtered = [p for p in all_packages if search.lower() in p["name"].lower()]
    else:
        filtered = all_packages

    return render_template("packages.html", packages=filtered)

# ================= PACKAGE DETAIL =================
@app.route("/package/<name>")
def package_detail(name):
    for p in all_packages:
        if p["name"].lower() == name.lower():
            return render_template("package_detail.html", package=p)
    return "Package not found"

# ================= REGISTER =================
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

# ================= LOGIN =================
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

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ================= BOOKING =================
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

# ================= CONTACT =================
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

# ================= REVIEWS =================
@app.route("/review", methods=["POST"])
def review():
    conn = get_db()
    conn.execute("INSERT INTO reviews(name,review) VALUES (?,?)",
                 (session.get("user","Guest"), request.form["review"]))
    conn.commit()
    conn.close()
    return redirect("/")

# ================= ADMIN LOGIN =================
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Invalid Admin Login"
    return render_template("admin_login.html")

# ================= DASHBOARD =================
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

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)