# ========================= app.py (FULL FIXED) =========================
from flask import Flask, render_template, request
import sqlite3
import os
import requests
from flask_mail import Mail, Message
import threading

app = Flask(__name__)

# ================= GOOGLE SHEETS FUNCTION =================
SHEET_URL = "https://api.sheetbest.com/sheets/8587ab41-3cad-44c2-a2f7-05ed8a71b466"

def send_to_sheets(data):
    try:
        response = requests.post(SHEET_URL, json=data)
        print("SHEET STATUS:", response.status_code)
        print("SHEET RESPONSE:", response.text)
    except Exception as e:
        print("Sheet Error:", e)

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= PACKAGES =================
all_packages = [

    {
        "name":"Kerala Alleppey Boathouse + Munnar",
        "slug":"kerala-boathouse",
        "price":"24000",
        "image":"boathouse.jpg",
        "itinerary":["Day 1: Arrival at Kochi and local sightseeing","Day 2: Transfer to Munnar and explore tea gardens","Day 3: Travel to Alleppey and check into houseboat","Day 4: Backwater cruise and departure"],
        "inclusions":"Accommodation, Breakfast and Dinner, Houseboat Stay, Sightseeing, Transfers, Guide",
        "exclusions":"Entry Tickets, Personal Expenses",
        "facilities":"AC Rooms, Private Houseboat, Pickup Drop, Tour Guide, Parking, Room Service"
    },

    {
        "name":"Dubai- City + Desert Safari + Exotic Wildlife",
        "slug":"dubai",
        "price":"-4N/5D-",
        "image":"dubai.jpg",
        "itinerary":["Day 1: Arrival in Dubai → Hotel check-in → Rest & lunch → Evening Desert Safari (dune bashing, camel ride, Arabic coffee, dinner, cultural show) → Overnight stay in Dubai","Day 2: Breakfast → Burj Khalifa visit (observation deck) → Dubai Mall shopping → Evening Dhow Cruise with dinner & entertainment → Overnight stay in Dubai","Day 3:Breakfast → Transfer/flight to Abu Dhabi → Hotel check-in → Yas Waterworld (water rides & activities) → Warner Bros. World (rides, shows & attractions) → Overnight stay in Abu Dhabi","Day 4: Breakfast → Visit Louvre Abu Dhabi (museum & galleries) → Ferrari World (theme park & rides) → Overnight stay in Abu Dhabi","Day 5: Breakfast → Hotel check-out → Transfer to airport → Departure for home"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Lunch, Personal Expenses",
        "facilities":"3 Star Hotel, AC Transport, Tour Guide, Free WiFi, Airport Transfer, Parking"
    },

    {
        "name":"Maldives",
        "slug":"maldives",
        "price":"-4N/5D",
        "image":"maldives.jpg",
        "itinerary":["Day 1: Arrival at Male Airport → Speedboat transfer to resort → Check-in → Leisure time on island → Candlelight dinner → Overnight stay ","Day 2: Breakfast → Male city tour (markets, monuments, shopping) → Beach time → Water sports (snorkelling, diving, scuba diving) → Overnight stay at resort","Day 3:Breakfast → Optional underwater walk / dolphin boat ride → Leisure activities → Dinner at resort → Overnight stay","Day 4: Breakfast → Island hopping tour / beach relaxation / pool time → Resort activities → Overnight stay","Day 5:Breakfast → Check-out → Speedboat to Male Airport → Departure"],
        "inclusions":"Resort Stay, All Meals, Airport Transfers, Water Activities, Sightseeing, Taxes",
        "exclusions":"Spa Charges, Personal Expenses",
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
        "name":"Goa N&S",
        "slug":"goa_beach",
        "price":"-3N/4D-",
        "image":"goa.jpg",
        "itinerary":["Day 1: Arrival in Goa → Hotel check-in → Breakfast → Calangute, Baga, Candolim beaches → Lunch → Optional water sports → Dinner → Overnight stay in North Goa","Day 2: Breakfast → Fort Aguada + lighthouse → Lunch → Chapora Fort & Vagator Beach photography → Sunset at Anjuna → Dinner → Overnight stay in North Goa","Day 3: Breakfast → Drive to South Goa → Visit Basilica of Bom Jesus, Se Cathedral, Mangueshi Temple → Lunch → Colva Beach / Palolem Beach → Dinner → Overnight stay in South Goa / North Goa (as per package)","Day 4: Breakfast → Free time for shopping / spa / café hopping / pool time → Lunch → Departure from Goa"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"  Water Sports Charges, Personal Expenses",
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
        "name":"Italy- Rome + Venice",
        "slug":"italy",
        "price":"-5N/6D-",
        "image":"italy.jpg",
        "itinerary":["Day 1: AArrival at Rome Airport → Transfer to Venice by high-speed train → Hotel check-in → Free time for local exploration → Overnight stay in Venice","Day 2:Breakfast → Boat tour to Murano Island, Burano Island & Torcello Island → Sightseeing (glassmaking, colorful houses, historic cathedral) → Return to hotel → Overnight stay in Venice","Day 3:Breakfast → Train to Florence → Check-in → Visit Pisa (Leaning Tower, Piazza dei Miracoli, Duomo, Baptistery) → Return to Florence → Overnight stay in Florence","Day 4: Breakfast → Florence sightseeing (Cathedral of Santa Maria del Fiore, Uffizi Gallery, Ponte Vecchio, Piazzale Michelangelo) → Travel to Rome → Evening city tour (Trevi Fountain, Piazza Venezia, Roman Forum, Colosseum exterior, etc.) → Overnight stay in Rome","Day 5: Breakfast → Vatican City visit (St. Peter’s Basilica, Vatican Museums, Sistine Chapel) → Free time for shopping / leisure → Overnight stay in Rome", "Day 6: Breakfast → Hotel check-out → Transfer to Rome Airport → Departure"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":" Entry Tickets, Personal Expenses",
        "facilities":"Luxury Hotel, Metro Access, Tour Guide, WiFi, Airport Transfer, Parking"
    },

    {
        "name":"Shimla + Manali + Kullu",
        "slug":"manali",
        "price":"-4N/5D",
        "image":"manali.jpg",
        "itinerary":["Day 1: Delhi → Shimla Mall Road Night Stay","Day 2: Kufri Adventure Park → Jakhoo Temple → Night Stay","Day 3: Shimla → Manali via Kullu Valley → River Rafting → Night Stay","Day 4: Solang Valley → Atal Tunnel → Sissu (if open) → Night Stay", "day 5: Manali Local Sightseeing → Hadimba Temple → Vashisht → Delhi Drop"],
        "inclusions":"Hotel Stay, Meals, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Permits, Adventure Activities, Personal Expenses",
        "facilities":"Hill Resort, Cab Service, Bonfire, Parking, Room Service, Guide"
    },

    {
        "name":"Egypt- CAIRO + ALEXANDRIA",
        "slug":"middle_east_tour",
        "price":"-4N/5D",
        "image":"middleeast.jpg",
        "itinerary":["Day 1: Arrival at Cairo Airport → Meet & assist → Hotel check-in → Evening Sound & Light Show → Overnight stay in Cairo","Day 2: Breakfast → Visit Pyramids of Giza (Cheops, Chephren, Mycerinus) → Sakkara Pyramid → Memphis City → Camel ride (optional) → Papyrus Institute & Old Bazaar → Overnight stay in Cairo","Day 3: Breakfast → Egyptian Museum → Citadel of Saladin → Mosque & old city areas → Church of Virgin Mary & St. Mark’s Cathedral → Local bazaar visit → Overnight stay in Cairo","Day 4:Breakfast → Drive to Alexandria → Pompey’s Pillar → Qaitbay Citadel → Alexandria Library → Return to Cairo → Overnight stay in Cairo","Day 5: Breakfast → Hotel check-out → Transfer to Cairo Airport → Departure"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Personal Expenses, Entry Tickets",
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
        "name":"Rajasthan - JODHPUR + JAISALMER",
        "slug":"rajasthan",
        "price":"-4N/5D-",
        "image":"rajasthan.jpg",
        "itinerary":["Day 1: Arrive Jodhpur,Visit Mehrangarh Fort, Jaswant Thada, Umaid Bhawan Palace → Night Stay Jodhpur","Day 2: Drive to Jaisalmer (5 hrs),En route visit Kuldhara Village → Evening at Gadisar Lake → Night Stay Jaisalmer","Day 3:Jaisalmer Sightseeing,Golden Fort, Patwon Ki Haveli, Nathmal Haveli → Evening Camel Safari & Folk Show at Sam Sand Dunes → Night Stay Desert Camp","Day 4: Jaisalmer → Jodhpur,Shopping / Leisure → Night Stay Jodhpur","Day 5: Drop at Jodhpur Airport / Railway Station"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Desert Safari",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"Heritage Hotel, Desert Camp, Cab Service, Parking, Guide, Room Service"
    },

    {
        "name":"Singapore",
        "slug":"singapore",
        "price":"-4N/5D-",
        "image":"singapore.jpg",
        "itinerary":["Day 1: Arrival,hotel check-in,Merlion Park,Marina Bay Sands Skypark, Gardens by the Bay,supertree lightshow,Night stay","Day 2: Breakfast,Sentosa Island tour(Cable car,S.E.A aquarium/madam tussauds),Wings of the Time show,night stay","Day 3: Breakfast,Universal Studios or Zoo + Night Safari,evening leisure,night stay ","Day 4: breakfast,Singapore Flyer / Duck Tour,Chinatown,little India,Bugis street shopping,Clark Quay Night walk,night stay", "Day 5: breakfast,hotel checkout,airport drop,departure,drop home"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Personal Expenses",
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
        "price":"1000000",
        "image":"tour world.jpg",
        "itinerary":["Day 1: Dubai","Day 2: Paris","Day 3: Switzerland","Day 4: USA","Day 5: Singapore","Day 6: Return"],
        "inclusions":"Flights, Hotel Stay, Visa, Transfers, Sightseeing, Guide",
        "exclusions":"Personal Expenses, Entry Tickets, Meals",
        "facilities":"Luxury Hotels, Flights Included, WiFi, Guide, Airport Transfers, Lounge Access"
    },

    {
        "name":"Vietnam-DA NANG - HANOI -",
        "slug":"vietnam",
        "price":"90000",
        "image":"vietnam.jpg",
        "itinerary":["Day 1: Bangalore Da Nang - Hotel check-in - local sightseeing Marble Mountain, Dragon Bridge, My Khe Beach or Hoi An Ancient Town, Ma May Ancient House, Hoan Kiem Lake & Ngoc Son Temple, Dong Xuan Market, night stay Da Nang","Day 2: Ba Na Hills & Golden Bridge Full Day Tour Sightseeing - cable car, Golden Bridge, French Village, Fantasy Park, Pagodas & Spiritual Area, & other sightseeing - Night Dep by flight, Da Nang - Hanoi, night stay","Day 3: Halong Bay Cruise, full day tour - Sung Sot Cave, Ti Top Island, Luon Cave, Thien Cung Cave, kayak - night stay, Hanoi","Day 4: Ninh Binh & caves Full Day Tour Ninh Binh caves include Trang An boat caves, Tam Coc three caves, and Mua Cave viewpoint with stunning limestone scenery, night stay Hanoi","Day 5: Hanoi Shopping, Dep Bangalore Morning Check out - shopping - Airport Drop"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Personal Expenses, Entry Tickets",
        "facilities":"Hotel, Cruise Stay, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Thailand-Pattaya",
        "slug":"thailand",
        "price":"32000-2N/3D",
        "image":"vac.jpg",
        "itinerary":["Day 1: Bangkok arrival,transfer to Pattaya,hotel check-in, aLcazar show,night stay ","Day 2:breakfast,Coral Island speed boat tour With lunch, beach activities,evening free, night stay","Day 3: -Breakfast, hotel checkout, Bangkok airport drop, flight to Bangalore"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Personal Expenses, Activities",
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



# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

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
    package = next((p for p in all_packages if p["slug"] == slug), None)
    if package:
        return render_template("package_detail.html", package=package)
    return "Package not found", 404

# ================= BOOKING =================
# ================= BOOKING =================
@app.route("/booking/<package>", methods=["GET","POST"])
def booking(package):

    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            package = request.form["package"]
            start_date = request.form["start_date"]
            return_date = request.form["return_date"]
            message = request.form["message"]

            # SAVE TO DATABASE
            conn = get_db()
            conn.execute("""
            INSERT INTO bookings(name,email,phone,package,start_date,return_date,message,service)
            VALUES (?,?,?,?,?,?,?,?)
            """,(name,email,phone,package,start_date,return_date,message,"package_booking"))
            conn.commit()
            conn.close()

            # GOOGLE SHEETS
            data = {
                "name": name,
                "email": email,
                "phone": phone,
                "package": package,
                "start_date": start_date,
                "return_date": return_date,
                "message": message,
                "service": "package_booking"
            }

            response = requests.post(
                "https://api.sheetbest.com/sheets/72a6df90-41c4-4378-b8c7-59c04aa3fa71",
                json=data
            )

            print("BOOKING STATUS:", response.status_code)
            print("BOOKING RESPONSE:", response.text)

            # EMAIL
            try:
                msg = Message(
                    "New Booking",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=["msmtoursandtravels2026@gmail.com"]
                )

                msg.body = f"""
New Booking

Name: {name}
Phone: {phone}
Package: {package}
"""

                threading.Thread(target=send_email_async, args=(app, msg)).start()

            except Exception as e:
                print("Email failed:", e)

            return render_template("success.html", name=name, package=package)

        except Exception as e:
            return f"Error: {e}"

    return render_template("booking.html", package=package)

# ================= SERVICE =================
# ================= SERVICE =================
@app.route("/service", methods=["GET","POST"])
def service():

    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            start_date = request.form["start_date"]
            return_date = request.form["return_date"]
            message = request.form["message"]
            service_type = request.form["service"]

            # SAVE TO DATABASE
            conn = get_db()
            conn.execute("""
            INSERT INTO bookings(name,email,phone,package,start_date,return_date,message,service)
            VALUES (?,?,?,?,?,?,?,?)
            """,(name,email,phone,service_type,start_date,return_date,message,service_type))
            conn.commit()
            conn.close()

            # GOOGLE SHEETS (FIXED)
            data = {
                "name": name,
                "email": email,
                "phone": phone,
                "package": service_type,
                "start_date": start_date,
                "return_date": return_date,
                "message": message,
                "service": service_type
            }

            response = requests.post(
                "https://api.sheetbest.com/sheets/72a6df90-41c4-4378-b8c7-59c04aa3fa71",
                json=data
            )

            print("SERVICE STATUS:", response.status_code)
            print("SERVICE RESPONSE:", response.text)

            return render_template("success.html", name=name, package=service_type)

        except Exception as e:
            return f"Error: {e}"

    return render_template("service.html")

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)


# ========================= init_db.py (UPDATED) =========================
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT,
package TEXT,
start_date TEXT,
return_date TEXT,
message TEXT,
service TEXT
)
""")

conn.commit()
conn.close()

print("Database ready!")


# ========================= FIX HTML CHANGE =========================
# In package_detail.html CHANGE THIS:
# <a href="/booking/{{package.name}}">
# TO:
# <a href="/booking/{{package.slug}}">
