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

# ================== YOUR PACKAGES (UNCHANGED) ==================
all_packages = [

    {
        "name":"Kerala Boathouse",
        "slug":"kerala-boathouse",
        "price":"25000",
        "image":"boathouse.jpg",
        "itinerary":["Day 1: Arrival at Kochi and local sightseeing","Day 2: Transfer to Munnar and explore tea gardens","Day 3: Travel to Alleppey and check into houseboat","Day 4: Backwater cruise and departure"],
        "inclusions":"Accommodation, Breakfast and Dinner, Houseboat Stay, Sightseeing, Transfers, Guide",
        "exclusions":"Flights, Entry Tickets, Personal Expenses",
        "facilities":"AC Rooms, Private Houseboat, Pickup Drop, Tour Guide, Parking, Room Service"
    },

    {
        "name":"Dubai",
        "slug":"dubai",
        "price":"60000",
        "image":"dubai.jpg",
        "itinerary":["Day 1: Arrival and Marina Dhow Cruise","Day 2: Dubai City Tour and Burj Khalifa","Day 3: Desert Safari with BBQ Dinner","Day 4: Shopping and leisure","Day 5: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Visa Assistance, Transfers, Desert Safari, Cruise Dinner",
        "exclusions":"Flights, Lunch, Personal Expenses",
        "facilities":"3 Star Hotel, AC Transport, Tour Guide, Free WiFi, Airport Transfer, Parking"
    },

    {
        "name":"Maldives",
        "slug":"maldives",
        "price":"90000",
        "image":"maldives.jpg",
        "itinerary":["Day 1: Arrival and resort transfer","Day 2: Leisure and beach activities","Day 3: Water sports and snorkeling","Day 4: Relaxation and departure"],
        "inclusions":"Resort Stay, All Meals, Airport Transfers, Water Activities, Sightseeing, Taxes",
        "exclusions":"Flights, Spa Charges, Personal Expenses",
        "facilities":"Water Villa, Private Beach, Swimming Pool, WiFi, Spa, Room Service"
    },

    {
        "name":"Ooty",
        "slug":"ooty",
        "price":"19000",
        "image":"ooty.jpg",
        "itinerary":["Day 1: Arrival and Ooty Lake visit","Day 2: Botanical Garden and Doddabetta Peak","Day 3: Coonoor excursion","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Transport to Ooty, Entry Fees, Personal Expenses",
        "facilities":"Hill View Rooms, Cab Service, Hot Water, Parking, Room Service, Guide"
    },

    {
        "name":"Goa Beach",
        "slug":"goa_beach",
        "price":"90000",
        "image":"goa.jpg",
        "itinerary":["Day 1: Arrival and North Goa beaches","Day 2: South Goa sightseeing","Day 3: Water sports and nightlife","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Beach Activities, Guide",
        "exclusions":"Flights, Water Sports Charges, Personal Expenses",
        "facilities":"Beach Resort, Swimming Pool, AC Rooms, WiFi, Bar, Parking"
    },

    {
        "name":"Hampi Karnataka",
        "slug":"hampi_karnataka",
        "price":"9000",
        "image":"hampi.jpg",
        "itinerary":["Day 1: Arrival and temple visit","Day 2: Heritage monuments and stone chariot","Day 3: Local sightseeing and departure"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"Budget Hotel, Local Guide, Cab, Parking, Room Service, Hot Water"
    },

    {
        "name":"India Tour",
        "slug":"india_tour",
        "price":"200000",
        "image":"india tour.jpg",
        "itinerary":["Day 1: Delhi arrival and sightseeing","Day 2: Agra Taj Mahal visit","Day 3: Jaipur forts and palaces","Day 4: Varanasi ghats","Day 5: Kerala backwaters","Day 6: Departure"],
        "inclusions":"Hotels, Breakfast, Domestic Flights, Transfers, Sightseeing, Guide",
        "exclusions":"International Flights, Personal Expenses, Entry Tickets",
        "facilities":"Premium Hotels, AC Transport, Tour Guide, Flights Included, WiFi, Parking"
    },

    {
        "name":"Italy",
        "slug":"italy",
        "price":"200000",
        "image":"italy.jpg",
        "itinerary":["Day 1: Arrival in Rome","Day 2: Vatican City and Colosseum","Day 3: Florence and Pisa","Day 4: Venice canals","Day 5: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Visa Assistance, Transfers, Sightseeing, Guide",
        "exclusions":"Flights, Entry Tickets, Personal Expenses",
        "facilities":"Luxury Hotel, Metro Access, Tour Guide, WiFi, Airport Transfer, Parking"
    },

    {
        "name":"Manali",
        "slug":"manali",
        "price":"30000",
        "image":"manali.jpg",
        "itinerary":["Day 1: Arrival and local sightseeing","Day 2: Solang Valley activities","Day 3: Rohtang Pass visit","Day 4: Departure"],
        "inclusions":"Hotel Stay, Meals, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Permits, Adventure Activities, Personal Expenses",
        "facilities":"Hill Resort, Cab Service, Bonfire, Parking, Room Service, Guide"
    },

    {
        "name":"Middle East Tour",
        "slug":"middle_east_tour",
        "price":"300000",
        "image":"middleeast.jpg",
        "itinerary":["Day 1: Dubai arrival","Day 2: Abu Dhabi city tour","Day 3: Doha visit","Day 4: Muscat sightseeing","Day 5: Departure"],
        "inclusions":"Hotels, Breakfast, Visa, Transfers, Internal Flights, Guide",
        "exclusions":"International Flights, Personal Expenses, Entry Tickets",
        "facilities":"Luxury Hotels, AC Transport, WiFi, Guide, Airport Pickup, Parking"
    },

    {
        "name":"Mysore",
        "slug":"mysore",
        "price":"9000",
        "image":"mysore.jpg",
        "itinerary":["Day 1: Arrival and Mysore Palace","Day 2: Zoo and Chamundi Hills","Day 3: Brindavan Gardens and departure"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"City Hotel, Cab Service, Parking, Room Service, Guide, Hot Water"
    },

    {
        "name":"Niagara - USA",
        "slug":"niagara_usa",
        "price":"300000",
        "image":"niagara.jpg",
        "itinerary":["Day 1: Arrival in New York","Day 2: Niagara Falls tour","Day 3: Washington DC sightseeing","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Transfers, Visa Assistance, Sightseeing, Guide",
        "exclusions":"Flights, Entry Tickets, Personal Expenses",
        "facilities":"Premium Hotel, Coach Travel, WiFi, Tour Guide, Airport Transfer, Parking"
    },

    {
        "name":"Odisha Wild",
        "slug":"odisha_wild",
        "price":"20000",
        "image":"odishawild.jpg",
        "itinerary":["Day 1: Bhubaneswar temples","Day 2: Puri and Konark","Day 3: Chilika Lake and safari","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Safari, Transfers, Sightseeing, Guide",
        "exclusions":"Entry Fees, Personal Expenses, Meals",
        "facilities":"Resort Stay, Jeep Safari, Parking, Guide, Room Service, Hot Water"
    },

    {
        "name":"Paris",
        "slug":"paris",
        "price":"200000",
        "image":"paris.jpg",
        "itinerary":["Day 1: Arrival and Eiffel Tower","Day 2: Louvre Museum and city tour","Day 3: Disneyland visit","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Visa Assistance, Transfers, Sightseeing, Guide",
        "exclusions":"Flights, Entry Tickets, Personal Expenses",
        "facilities":"Central Hotel, Metro Access, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Rajasthan",
        "slug":"rajasthan",
        "price":"40000",
        "image":"rajasthan.jpg",
        "itinerary":["Day 1: Jaipur sightseeing","Day 2: Jodhpur forts","Day 3: Udaipur lakes","Day 4: Jaisalmer desert safari","Day 5: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Desert Safari",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"Heritage Hotel, Desert Camp, Cab Service, Parking, Guide, Room Service"
    },

    {
        "name":"Singapore",
        "slug":"singapore",
        "price":"100000",
        "image":"singapore.jpg",
        "itinerary":["Day 1: Arrival and Night Safari","Day 2: City tour and Sentosa Island","Day 3: Universal Studios","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Entry Tickets, Transfers, Sightseeing, Guide",
        "exclusions":"Flights, Personal Expenses, Lunch",
        "facilities":"City Hotel, Metro Pass, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Himalayas",
        "slug":"himalayas",
        "price":"40000",
        "image":"skii.jpg",
        "itinerary":["Day 1: Shimla arrival","Day 2: Kufri snow activities","Day 3: Manali sightseeing","Day 4: Solang Valley","Day 5: Departure"],
        "inclusions":"Hotel Stay, Meals, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Adventure Activities, Permits, Personal Expenses",
        "facilities":"Hill Resort, Camp Stay, Bonfire, Guide, Parking, Room Service"
    },

    {
        "name":"Delhi",
        "slug":"delhi",
        "price":"40000",
        "image":"tajmahal.jpg",
        "itinerary":["Day 1: Delhi sightseeing","Day 2: Agra Taj Mahal","Day 3: Jaipur visit","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Transfers, Sightseeing, Guide, Parking",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"City Hotel, Cab Service, WiFi, Guide, Parking, Room Service"
    },

    {
        "name":"World Tour",
        "slug":"world_tour",
        "price":"600000",
        "image":"tour world.jpg",
        "itinerary":["Day 1: Dubai","Day 2: Paris","Day 3: Switzerland","Day 4: USA","Day 5: Singapore","Day 6: Return"],
        "inclusions":"Flights, Hotel Stay, Visa, Transfers, Sightseeing, Guide",
        "exclusions":"Personal Expenses, Entry Tickets, Meals",
        "facilities":"Luxury Hotels, Flights Included, WiFi, Guide, Airport Transfers, Lounge Access"
    },

    {
        "name":"Vietnam",
        "slug":"vietnam",
        "price":"90000",
        "image":"vietnam.jpg",
        "itinerary":["Day 1: Hanoi arrival","Day 2: Halong Bay cruise","Day 3: Ho Chi Minh city","Day 4: Cu Chi tunnels","Day 5: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Cruise, Transfers, Sightseeing, Guide",
        "exclusions":"Flights, Personal Expenses, Entry Tickets",
        "facilities":"Hotel, Cruise Stay, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Thailand",
        "slug":"thailand",
        "price":"90000",
        "image":"vac.jpg",
        "itinerary":["Day 1: Bangkok arrival","Day 2: Pattaya Coral Island","Day 3: Bangkok temples","Day 4: Departure"],
        "inclusions":"Hotel Stay, Breakfast, Transfers, Sightseeing, Guide, Entry Tickets",
        "exclusions":"Flights, Personal Expenses, Activities",
        "facilities":"Hotel, Cab Service, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Bandipur - Mudumalai Wildlife",
        "slug":"bandipur_mudumalai_wildlife",
        "price":"15000",
        "image":"Wildlife.jpg",
        "itinerary":["Day 1: Arrival and jungle stay","Day 2: Safari and bird watching","Day 3: Nature walk and departure"],
        "inclusions":"Resort Stay, Meals, Safari, Transfers, Guide, Sightseeing",
        "exclusions":"Entry Fees, Personal Expenses, Activities",
        "facilities":"Jungle Resort, Jeep Safari, Guide, Parking, Room Service, Campfire"
    },

    {
        "name":"Nagarhole Tiger Reserve",
        "slug":"nagarhole_tiger_reserve",
        "price":"12000",
        "image":"wild.jpg",
        "itinerary":["Day 1: Arrival and forest stay","Day 2: Tiger safari and nature walk","Day 3: Departure"],
        "inclusions":"Resort Stay, Meals, Safari, Guide, Transfers, Sightseeing",
        "exclusions":"Entry Fees, Personal Expenses, Activities",
        "facilities":"Forest Lodge, Jeep Safari, Guide, Parking, Room Service, Campfire"
    }

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

# ================= BOOKING (FULLY FIXED) =================
@app.route("/booking/<package>", methods=["GET","POST"])
def booking(package):

    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            start_date = request.form["start_date"]
            return_date = request.form["return_date"]
            message = request.form["message"]

            # SAVE TO DATABASE
            conn = get_db()
            conn.execute("""
            INSERT INTO bookings(name,email,phone,package,start_date,return_date,message)
            VALUES (?,?,?,?,?,?,?)
            """,(name,email,phone,package,start_date,return_date,message))
            conn.commit()
            conn.close()

            # ================= GOOGLE SHEETS =================
            data = {
                "name": name,
                "email": email,
                "phone": phone,
                "package": package,
                "start_date": start_date,
                "return_date": return_date,
                "message": message
            }

            try:
                requests.post(
                    "https://api.sheetbest.com/sheets/8587ab41-3cad-44c2-a2f7-05ed8a71b466",
                    json=data
                )
                print("✅ Sent to Google Sheets")
            except Exception as e:
                print("❌ Sheets error:", e)

            # ================= EMAIL (OPTIONAL) =================
            try:
                msg = Message(
                    "New Booking - MSM Tours",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[
                        "msmtoursandtravels2026@gmail.com",
                        "michellemagdalene885@gmail.com"
                    ]
                )

                msg.body = f"""
New Booking Received!

Name: {name}
Email: {email}
Phone: {phone}
Package: {package}
Start Date: {start_date}
Return Date: {return_date}
Message: {message}
"""

                threading.Thread(target=send_email_async, args=(app, msg)).start()

            except Exception as e:
                print("❌ Email failed:", e)

            return render_template("success.html", name=name, package=package)

        except Exception as e:
            return f"Error: {e}"

    return render_template("booking.html", package=package)

# =======================================================

# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)