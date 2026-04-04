from flask import Flask, render_template, request
import sqlite3
import os
import requests
from flask_mail import Mail, Message
import threading

app = Flask(__name__)

# EMAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'msmtoursandtravels2026@gmail.com'
app.config['MAIL_PASSWORD'] = 'ipdildueutmwfuyi'

mail = Mail(app)

# DATABASE
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# EMAIL BACKGROUND (NO LAG)
def send_email_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("✅ Email sent successfully")
        except Exception as e:
            print("❌ Email error:", e)

# PACKAGES
all_packages = [
    {"name":"Kerala Boathouse","slug":"kerala-boathouse","price":"25000","image":"boathouse.jpg"},
    {"name":"Dubai","slug":"dubai","price":"60000","image":"dubai.jpg"},
    {"name":"Maldives","slug":"maldives","price":"90000","image":"maldives.jpg"},
    {"name":"Ooty","slug":"ooty","price":"19000","image":"ooty.jpg"},
    {"name":"Goa Beach","slug":"goa_beach","price":"90000","image":"goa.jpg"},
    {"name":"Hampi Karnataka","slug":"hampi_karnataka","price":"9000","image":"hampi.jpg"},
    {"name":"India Tour","slug":"india_tour","price":"200000","image":"india tour.jpg"},
    {"name":"Italy","slug":"italy","price":"200000","image":"italy.jpg"},
    {"name":"Manali","slug":"manali","price":"30000","image":"manali.jpg"},
    {"name":"Middle East Tour","slug":"middle_east_tour","price":"300000","image":"middleeast.jpg"},
    {"name":"Mysore","slug":"mysore","price":"9000","image":"mysore.jpg"},
    {"name":"Niagara - USA","slug":"niagara_usa","price":"300000","image":"niagara.jpg"},
    {"name":"Odisha Wild","slug":"odisha_wild","price":"20000","image":"odishawild.jpg"},
    {"name":"Paris","slug":"paris","price":"200000","image":"paris.jpg"},
    {"name":"Rajasthan","slug":"rajasthan","price":"40000","image":"rajasthan.jpg"},
    {"name":"Singapore","slug":"singapore","price":"100000","image":"singapore.jpg"},
    {"name":"Himalayas","slug":"himalayas","price":"40000","image":"skii.jpg"},
    {"name":"Delhi","slug":"delhi","price":"40000","image":"tajmahal.jpg"},
    {"name":"World Tour","slug":"world_tour","price":"600000","image":"tour world.jpg"},
    {"name":"Vietnam","slug":"vietnam","price":"90000","image":"vietnam.jpg"},
    {"name":"Thailand","slug":"thailand","price":"90000","image":"vac.jpg"},
    {"name":"Bandipur - Mudumalai Wildlife","slug":"bandipur_mudumalai_wildlife","price":"15000","image":"Wildlife.jpg"},
    {"name":"Nagarhole Tiger Reserve","slug":"nagarhole_tiger_reserve","price":"12000","image":"wild.jpg"},
]

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# PACKAGES
@app.route("/packages")
def packages():
    return render_template("packages.html", packages=all_packages)

# PACKAGE DETAILS
@app.route("/package/<slug>")
def package_detail(slug):
    package = next((p for p in all_packages if p["slug"] == slug), None)
    if package:
        return render_template("package_detail.html", package=package)
    return "Package not found"

# BOOKING (FIXED - NO LOADING ISSUE)
@app.route("/booking/<package>", methods=["GET","POST"])
def booking(package):

    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            date = request.form["date"]
            message = request.form["message"]

            # SAVE TO DATABASE
            conn = get_db()
            conn.execute("""
            INSERT INTO bookings(name,email,phone,package,date,message)
            VALUES (?,?,?,?,?,?)
            """,(name,email,phone,package,date,message))
            conn.commit()
            conn.close()

            # ================= GOOGLE SHEET =================
            data = {
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Package": package,
                "Date": date,
                "Message": message
            }

            # 🔥 PASTE YOUR SHEET URL BELOW
            requests.post("https://api.sheetbest.com/sheets/8587ab41-3cad-44c2-a2f7-05ed8a71b466", json=data)

            # SUCCESS PAGE
            return render_template("success.html", name=name, package=package)

        except Exception as e:
            return f"Error: {e}"

    return render_template("booking.html", package=package)

# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)