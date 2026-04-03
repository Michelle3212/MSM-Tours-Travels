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

# ================= HELPER (FOR URL SAFE NAMES) =================
def create_slug(name):
    return name.lower().replace(" ", "-")

# ================= PACKAGES DATA =================
all_packages = [

    {
        "name":"Kerala Boathouse",
        "slug":"kerala-boathouse",
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
        "slug":"rajasthan",
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
        "facilities":"Desert Camp"
    },

    {
        "name":"Paris",
        "slug":"paris",
        "price":"120000",
        "image":"paris.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Eiffel Tower",
            "Day 3: Shopping",
            "Day 4: Departure"
        ],
        "inclusions":"Hotel, Visa",
        "exclusions":"Flights",
        "facilities":"Luxury Stay"
    },

    {
        "name":"Singapore",
        "slug":"singapore",
        "price":"80000",
        "image":"singapore.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Universal Studios",
            "Day 3: City tour"
        ],
        "inclusions":"Hotel",
        "exclusions":"Flights",
        "facilities":"Theme Parks"
    },

    {
        "name":"Dubai",
        "slug":"dubai",
        "price":"60000",
        "image":"dubai.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: City tour",
            "Day 3: Desert safari"
        ],
        "inclusions":"Hotel",
        "exclusions":"Flights",
        "facilities":"Luxury Stay"
    },

    {
        "name":"Ooty",
        "slug":"ooty",
        "price":"15000",
        "image":"ooty.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Garden visit",
            "Day 3: Departure"
        ],
        "inclusions":"Hotel",
        "exclusions":"Transport",
        "facilities":"Hill View"
    },

    {
        "name":"Coorg",
        "slug":"coorg",
        "price":"20000",
        "image":"coorg.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Coffee estates",
            "Day 3: Departure"
        ],
        "inclusions":"Hotel",
        "exclusions":"Transport",
        "facilities":"Nature Stay"
    },

    {
        "name":"Odisha",
        "slug":"odisha",
        "price":"22000",
        "image":"odishawild.jpg",
        "itinerary":[
            "Day 1: Puri",
            "Day 2: Konark",
            "Day 3: Chilika Lake"
        ],
        "inclusions":"Hotel",
        "exclusions":"Flights",
        "facilities":"Temple Tour"
    },

    {
        "name":"Maldives",
        "slug":"maldives",
        "price":"90000",
        "image":"maldives.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: Resort stay",
            "Day 3: Water sports"
        ],
        "inclusions":"Resort",
        "exclusions":"Flights",
        "facilities":"Private Beach"
    },

    {
        "name":"Vietnam",
        "slug":"vietnam",
        "price":"70000",
        "image":"vietnam.jpg",
        "itinerary":[
            "Day 1: Arrival",
            "Day 2: City tour",
            "Day 3: Cruise"
        ],
        "inclusions":"Hotel",
        "exclusions":"Flights",
        "facilities":"Cruise"
    },

    {
        "name":"Mysore",
        "slug":"mysore",
        "price":"12000",
        "image":"mysore.jpg",
        "itinerary":[
            "Day 1: Palace",
            "Day 2: Zoo",
            "Day 3: Departure"
        ],
        "inclusions":"Hotel",
        "exclusions":"Transport",
        "facilities":"City Tour"
    },

    {
        "name":"Hampi Karnataka",
        "slug":"hampi",
        "price":"14000",
        "image":"hampi.jpg",
        "itinerary":[
            "Day 1: Temples",
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

# ================= ADMIN =================
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Invalid Admin Login"
    return render_template("admin_login.html")

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