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
        "name":"Goa N&S",
        "slug":"goa_beach",
        "price":"₹12,204 - 3D/2N",
        "image":"goa.jpg",
        "itinerary":["Day 1: Arrival in Goa → Hotel check-in → Relax & freshen up → Calangute, Baga, Candolim beaches → Lunch → Free time for beach activities → Sunset view → Dinner → Overnight stay in North Goa","Day 2: Breakfast → Fort Aguada + lighthouse → Calangute & Baga Beach visit → Lunch → Anjuna Beach → Vagator Beach & Chapora Fort photography → Sunset → Optional cruise / nightlife → Dinner → Overnight stay in North Goa","Day 3: Breakfast → Check-out → Drive to South Goa → Visit Basilica of Bom Jesus, Se Cathedral, Dona Paula View Point → Lunch → Miramar Beach → Shopping (if time permits) → Departure from Goa"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"entry tickets, Personal Expenses",
        "facilities":"Beach Resort, Swimming Pool, AC Rooms, WiFi, Bar, Parking"
    },
    {
        "name":"Ooty",
        "slug":"goa_beach",
        "price":"₹5300- 2D/1N",
        "image":"ooty.jpg",
        "itinerary":["Day 1: Departure from Bangalore → Scenic journey to Ooty via Mysore & Bandipur → Hotel check-in → Relax & freshen up → Visit Ooty Lake & Botanical Garden → Evening shopping at local market → Dinner → Overnight stay in Ooty","Day 2: Breakfast → Explore Doddabetta Peak, Tea Factory & Rose Garden → Lunch → Visit Pykara Lake & Waterfalls → Boating & sightseeing → Return to hotel → Dinner → Overnight stay in Ooty","Day 3: Breakfast → Excursion to Coonoor → Visit Sim’s Park, Dolphin’s Nose & Lamb’s Rock → Lunch → Enjoy Nilgiri mountain views & tea estates → Return to Ooty → Campfire/music (optional) → Dinner → Overnight stay in Ooty","Day 4: Breakfast → Leisure morning & local shopping → Check-out from hotel → Departure to Bangalore with memorable hill station experiences"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"entry tickets, Personal Expenses",
        "facilities":"Beach Resort, Swimming Pool, AC Rooms, WiFi, Bar, Parking"
    },

    {
        "name":"Kerala Beach + Mountain",
        "slug":"kerala-boathouse",
        "price":"14,713/-5D/4N-",
        "image":"kerala.jpg",
        "itinerary":["Day 1: Departure from Bangalore → Scenic drive/train journey to Munnar → Hotel check-in → Relax & freshen up → Visit Tea Gardens & Mattupetty Dam → Evening at leisure amidst hills → Dinner → Overnight stay in Munnar","Day 2: Breakfast → Explore Eravikulam National Park, Echo Point & Kundala Lake → Lunch → Departure to Alleppey → Check-in to houseboat/resort → Backwater cruise experience → Sunset by the lake → Traditional Kerala dinner → Overnight stay in Alleppey","Day 3: Breakfast → Departure to Varkala → Hotel check-in → Relax at Varkala Cliff & Beach → Lunch → Free time for beach activities & café hopping → Sunset view at Varkala Beach → Dinner → Overnight stay in Varkala","Day 4: Breakfast → Leisure morning by the beach → Departure to Kochi → Hotel check-in → Explore Fort Kochi, Chinese Fishing Nets & Marine Drive → Shopping & local food experience → Dinner → Overnight stay in Kochi","Day 5: Breakfast → Visit Lulu Mall / local sightseeing if time permits → Check-out → Departure from Kochi to Bangalore → Tour ends with beautiful Kerala beach & mountain memories"],
        "inclusions":"Accommodation, Breakfast and Dinner, Houseboat Stay, Sightseeing, Transfers, Guide",
        "exclusions":"Entry Tickets, Personal Expenses",
        "facilities":"AC Rooms, Private Houseboat, Pickup Drop, Tour Guide, Parking, Room Service"
    },

    {
        "name":"Dubai- City + Desert Safari + Exotic Wildlife",
        "slug":"dubai",
        "price":"-4N/5D-",
        "image":"dubai.jpg",
        "itinerary":["Day 1: Arrival in Dubai → Hotel check-in → Rest & lunch → Evening Desert Safari (dune bashing, camel ride, Arabic coffee, dinner, cultural show) → Overnight stay in Dubai","Day 2: Breakfast → Burj Khalifa visit (observation deck) → Dubai Mall shopping → Evening Cruise with dinner & entertainment → Overnight stay in Dubai","Day 3:Breakfast → Transfer/flight to Abu Dhabi → Hotel check-in → Yas Waterworld (water rides & activities) → Warner Bros. World (rides, shows & attractions) → Overnight stay in Abu Dhabi","Day 4: Breakfast → Visit Louvre Abu Dhabi (museum & galleries) → Ferrari World (theme park & rides) → Overnight stay in Abu Dhabi","Day 5: Breakfast → Hotel check-out → Transfer to airport → Departure for home"],
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
        "name":"Ooty - Wayanad from B'lore",
        "slug":"ooty",
        "price":"₹12999 - 4D/3N",
        "image":"ooty.jpg",
        "itinerary":["Day 1: Pick up at 6 AM from Bangalore - Drive to Wayanad & Wayanad Sightseeing","Day 2: Start at 9 AM - Wayanad sightseeing","Day 3: Start at 9 AM - Wayanad to Ooty and Ooty sightseeing","Day 4: Start at 9 AM - Ooty sightseeing and drop to Bangalore"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Entry Fees, Personal Expenses",
        "facilities":"Hill View Rooms, Cab Service, Hot Water, Parking, Room Service, Guide"
    },

    {
        "name":"Hampi Karnataka",
        "slug":"hampi_karnataka",
        "price":"₹5505-3D/2N-",
        "image":"hampi.jpg",
        "itinerary":["Day 1:Departure From Bangalore For Hampi","Day 2:  Reach Hampi and explore the historical city","Day 3: Sunset at the hill and lake visit, Departure"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"Budget Hotel, Local Guide, Cab, Parking, Room Service, Hot Water"
    },

    {
        "name":"India Tour",
        "slug":"india_tour",
        "price":"-15D/14N-",
        "image":"india tour.jpg",
        "itinerary":["Day 1: Bangalore Delhi - Arrival - Local Sightseeing - Night Stay Delhi","Day 2:Delhi Sightseeing - India Gate, Qutub Minar, Lotus Temple - Night Stay Delhi","Day 3:Delhi Agra - Visit Taj Mahal, Agra Fort - Night Stay Agra","Day 4: Agra Jaipur via Fatehpur Sikri - Night Stay Jaipur","Day 5: Jaipur Sightseeing - Amber Fort, City Palace, Jantar Mantar, Hawa Mahal - Night Stay Jaipur","Day 6: Jaipur Mumbai - Arrival - Marine Drive, Gateway of India - Night Stay Mumbai","Day 7: Mumbai Sightseeing - Local Tour - Night Stay Mumbai","Day 8: Mumbai Goa - Arrival - Beach Leisure - Night Stay Goa","Day 9: Goa Sightseeing - North Goa / South Goa - Night Stay Goa","Day 10: Goa Bangalore Kochi - Arrival - Night Stay Kochi","Day 11: Kochi Munnar - Hill Station - Tea Gardens - Night Stay Munnar","Day 12: Munnar Alleppey - Houseboat Stay - Backwaters - Night Stay Alleppey","Day 13: Alleppey Madurai - Temple Visit - Night Stay Madurai","Day 14: Madurai Rameswaram - Temple Darshan - Night Stay Rameswaram","Day 15: Rameswaram Bangalore - Departure"],
        "inclusions":"Hotels, Breakfast, Domestic Flights, Transfers, Sightseeing, Guide",
        "exclusions":"Personal Expenses, Entry Tickets",
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
        "name":"Shimla + Manali + Kasol",
        "slug":"manali",
        "price":"46750/-, 8D/7N",
        "image":"manali.jpg",
        "itinerary":["Day 1: Departure from Bangalore → Arrival in Delhi/Chandigarh → Scenic drive to Shimla → Hotel check-in → Relax & freshen up → Evening stroll at Mall Road & Ridge → Dinner → Overnight stay in Shimla","Day 2: Breakfast → Visit Kufri, Green Valley & Jakhoo Temple → Adventure activities & sightseeing → Lunch → Free time for shopping and café visits at Mall Road → Dinner → Overnight stay in Shimla","Day 3:Breakfast → Check-out from Shimla → Scenic drive to Manali via Kullu Valley → Enroute river rafting & shawl factory visit → Arrival in Manali → Hotel check-in → Dinner → Overnight stay in Manali","Day 4: Breakfast → Full-day Solang Valley excursion → Enjoy snow activities, ropeway, ATV rides & paragliding → Lunch → Return to hotel → Bonfire & music session → Dinner → Overnight stay in Manali", "Day 5: Early breakfast → Excursion to Atal Tunnel, Sissu & Rohtang Pass (subject to permit/weather) → Snow sightseeing & photography → Return to Manali → Leisure evening at Mall Road → Dinner → Overnight stay in Manali", "Day 6: Breakfast → Visit Hadimba Temple, Vashisht Hot Springs & Old Manali cafés → Check-out → Drive to Kasol → Riverside campsite/hotel check-in → Relax by Parvati River → Bonfire & dinner → Overnight stay in Kasol","Day 7: Breakfast → Explore Kasol local market & cafés → Trek to Chalal/Manikaran Sahib visit → Lunch → Free time amidst mountains and riverside views → Evening music & bonfire → Dinner → Overnight stay in Kasol","Day 8: Breakfast → Check-out from Kasol → Drive back to Delhi/Chandigarh → Departure to Bangalore → Tour ends with unforgettable Himachal mountain memories"],
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
        "name":"Mysore - Coorg",
        "slug":"mysore",
        "price":"-4D/3N-",
        "image":"coorgmysore.jpg",
        "itinerary":["Day 1: Mysore Nagarhole - Safari - RRPu Falls - Coorg Overnight Stay","Day 2:Coorg Thalakavery - Bagamandala - Glass Bridge - Mandalpati Peak Jeep Safari - Abbey Falls - Raja's Seat","Day 3: Coorg Dubare Elephant Camp - River Rafting - Chiklihole Dam - Kaveri Nisargadama - Golden Temple - Harangi Tree Park","Day 4: Coorg Mysore - Chamundeshwari Temple - Sand Museum - Wax Museum - Karanji Lake - Jaganmohan Palace - Mysore Palace"],
        "inclusions":"Hotel Stay, Breakfast, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"City Hotel, Cab Service, Parking, Room Service, Guide, Hot Water"
    },

    {
        "name":"Niagara - USA",
        "slug":"niagara_usa",
        "price":"7D/6N",
        "image":"niagara.jpg",
        "itinerary":["Day 1:Arrival in New York | Day at Leisure","Day 2:Statue of Liberty Cruise | New York Sightseeing Tour | Visit to One World Observation","Day 3:Transfer to Washington D.C. | Enroute Sightseeing to Philadelphia","Day 4:Washington D.C. Sightseeing Tour | Visit to Air & Space Museum | Enjoy the Capital Wheel","Day 5:Transfer to Niagara Falls, NY | Enroute Visit Hershey’s Chocolate World | Leisure Time","Day 6:Niagara Falls, NY Sightseeing Tour","Day 7:Departure Day"],
        "inclusions":"Hotel Stay, Breakfast, Transfers, Visa Assistance, Sightseeing, Guide",
        "exclusions":"Entry Tickets, Personal Expenses",
        "facilities":"Premium Hotel, Coach Travel, WiFi, Tour Guide, Airport Transfer, Parking"
    },

    {
        "name":"Odisha Wild",
        "slug":"odisha_wild",
        "price":"3D/2N",
        "image":"odishawild.jpg",
        "itinerary":["Day 1:Arrival at Bhadrak/Bhubaneswar; Drive to Bhitarkanika","Day 2: Bhitarkanika Sightseeing","Day 3:Return to Bhadrak/Bhubaneswar; End of Tour,Departure"],
        "inclusions":"Hotel Stay, Breakfast, Safari, Transfers, Sightseeing, Guide",
        "exclusions":"Entry Fees, Personal Expenses, Meals",
        "facilities":"Resort Stay, Jeep Safari, Parking, Guide, Room Service, Hot Water"
    },

    {
        "name":"Europe at a Glance - Zurich 3N, Paris 3N, London 3N",
        "slug":"paris",
        "price":"-10D/9N-",
        "image":"paris.jpg",
        "itinerary":["Day 1:Zurich Calling - The Swiss Chapter Begins","Day 2: World's First Rotating Cable Car Rotair Up Mt. Titlis Peak At 3,020m - Orientation Tour Of Lucerne","Day 3:Magical Alpine Excursion To The Top Of Europe - The Amazing Jungfraujoch And Scenic Interlaken (Extra Cost)","Day 4: From The Roar Of Rhine Falls To The Romance Of Paris","Day 5: Paris City Tour  Eiffel Tower 2nd Level & Seine River Cruise","Day 6: A Magical Day At Disneyland Paris","Day 7: Paris To London  Across The Channel With A Taste Of Elegance","Day 8: Iconic London  City Tour, Madame Tussauds & The London Eye","Day 9: Lords Cricket Ground & Bicester Village Shopping","Day 10: Adieu Europe  A Grand Journey Concludes"],
        "inclusions":"Hotel Stay, Breakfast, Visa Assistance, Transfers, Sightseeing, Guide",
        "exclusions":"Entry Tickets, Personal Expenses",
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
        "price":"₹63,250,-4D/3N-",
        "image":"singapore.jpg",
        "itinerary":["Day 1: Arrival in Singapore,hotel check-in,Merlion Park,Marina Bay Sands SkyPark,Helix Bridge, Gardens by the Bay,Supertree Grove Light Show,night stay","Day 2: Breakfast,Sentosa Island tour(Cable Car,S.E.A Aquarium/Madame Tussauds,Siloso Beach),Wings of Time show,dinner,night stay","Day 3: Breakfast,Universal Studios Singapore full day tour,rides and attractions,evening leisure at Orchard Road,night stay","Day 4: Breakfast,Singapore Flyer,Chinatown,Little India,Bugis Street shopping,Clarke Quay evening walk,hotel checkout,airport drop,departure"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Breakfast, flight ticket,Train from Rome to Florence,private transfer",
        "exclusions":"Personal Expenses",
        "facilities":"City Hotel, Metro Pass, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Rome + Florence",
        "slug":"singapore",
        "price":"₹1,28,900,-4D/3N-",
        "image":"romeflor.jpg",
        "itinerary":["Day 1: Arrival in Rome,hotel check-in,Colosseum,Roman Forum,Trevi Fountain,Spanish Steps,Piazza Navona,night stay","Day 2: Breakfast,Vatican City tour(St. Peter’s Basilica,Sistine Chapel,Vatican Museums),Pantheon,evening leisure in Trastevere,night stay","Day 3: Breakfast,train transfer to Florence,hotel check-in,Florence Cathedral,Piazza della Signoria,Ponte Vecchio,Uffizi Gallery,night stay","Day 4: Breakfast,Pisa half-day excursion or Tuscany countryside tour,shopping at Florence local markets,hotel checkout,departure"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Breakfast, flight ticket,Train from Rome to Florence,private transfer",
        "exclusions":"Personal Expenses",
        "facilities":"City Hotel, Metro Pass, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Kashmir - SRINAGAR + GULMARG + SONAMARG + PAHALGAM",
        "slug":"himalayas",
        "price":"-5N/6D-",
        "image":"skii.jpg",
        "itinerary":["Day 1: Arrival at Srinagar - Shikara Ride - Overnight stay","Day 2: Srinagar Gulmarg - Gondola Ride - Snow activities","Day 3:Srinagar Sonamarg - Thajiwas Glacier - Return","Day 4: Srinagar Pahalgam - Lidder Valley - Aru / Betaab Valley","Day 5: Pahalgam Srinagar - Local Sightseeing","Day 6:Srinagar Departure"],
        "inclusions":"Hotel Stay, Meals, Sightseeing, Transfers, Guide, Parking",
        "exclusions":"Adventure Activities, Permits, Personal Expenses",
        "facilities":"Hill Resort, Camp Stay, Bonfire, Guide, Parking, Room Service"
    },

    {
        "name":"DELHI + AGRA + JAIPUR",
        "slug":"delhi",
        "price":"-4N/5D-",
        "image":"tajmahal.jpg",
        "itinerary":["Day 1:Arrive Delhi Visit India Gate, Qutub Minar, Lotus Temple - Night Stay Delhi","Day 2: Delhi Agra - Visit Taj Mahal, Agra Fort - Night Stay Agra","Day 3:Agra Jaipur via Fatehpur Sikri - Night Stay Jaipur","Day 4: Jaipur Sightseeing - Amber Fort, City Palace, Jantar Mantar, Hawa Mahal - Night Stay Jaipur","Day 5: Drop at Jaipur Airport / Railway Station"],
        "inclusions":"Hotel Stay, Breakfast, Transfers, Sightseeing, Guide, Parking",
        "exclusions":"Entry Tickets, Personal Expenses, Meals",
        "facilities":"City Hotel, Cab Service, WiFi, Guide, Parking, Room Service"
    },

    {
        "name":"Best Of China ",
        "slug":"world_tour",
        "price":"13D/12N",
        "image":"china.jpg",
        "itinerary":["Day 1: Arrive Beijing - Leisure","Day 2: Beijing - Summer Palace - Tiananmen Square - Forbidden City","Day 3: Beijing - Great Wall of China - Olympic Village - Temple of Heaven","Day 4: Beijing Chengdu - Panda Research Base - Face Changing Show","Day 5: Chengdu Leshan Chengdu - Leshan Giant Buddha - Boat Ride","Day 6: Chengdu Chongqing - Bullet Train - Liziba Station - Yangtze Cable Car - Hongya Cave","Day 7: Chongqing Zhangjiajie - Tianmen Mountain - Cable Car","Day 8: Zhangjiajie - Wulingyuan - Bailong Elevator - Glass Bridge","Day 9: Zhangjiajie Guilin - Arrival - Foot Massage","Day 10: Guilin - Li River Cruise - Elephant Hill - Reed Flute Cave","Day 11: Guilin Shanghai - Maglev Train - The Bund - Jin Mao Tower - Circus Show","Day 12: Shanghai - Silk Factory - Yu Yuan Garden - Leisure","Day 13: Shanghai Departure"],
        "inclusions":"Flights, Hotel Stay, Visa, Transfers, Sightseeing, Guide",
        "exclusions":"Personal Expenses, Entry Tickets, Meals",
        "facilities":"Luxury Hotels, Flights Included, WiFi, Guide, Airport Transfers, Lounge Access"
    },

    {
        "name":"Vietnam-DA NANG - HANOI -",
        "slug":"vietnam",
        "price":"59,750/-4D/3N",
        "image":"vietnam.jpg",
        "itinerary":["Day 1:Departure from Bangalore → Arrival at Hanoi Airport → Hotel check-in → Hanoi Old Quarter visit → Night market → Overnight stay","Day 2:Breakfast → Transfer to Halong Bay → Cruise experience → Cave visit & sightseeing → Return to Hanoi → Overnight stay","Day 3: Breakfast → Transfer / Flight to Da Nang → Bana Hills & Golden Bridge visit → Beach leisure time → Dragon Bridge visit → Overnight stay","Day 4: Breakfast → Shopping & relaxation → Airport transfer → Departure to Bangalore"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Personal Expenses, Entry Tickets",
        "facilities":"Hotel, Cruise Stay, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Thailand-Bangkok+Pattaya",
        "slug":"thailand",
        "price":"52,350-4D/3N",
        "image":"vac.jpg",
        "itinerary":["Day 1: Departure from Bangalore → Arrival at Bangkok Airport → Transfer to Pattaya → Hotel check-in → Pattaya beach leisure time → Dinner → Overnight stay","Day 2:Breakfast → Coral Island tour by speedboat → Water activities & beach relaxation → Return to hotel → Shopping / Walking Street → Overnight stay","Day 3:Breakfast → Transfer to Bangkok → Bangkok city & temple tour → Hotel check-in → Chao Phraya dinner cruise → Shopping at MBK / Indra Market → Overnight stay","Day 4: Breakfast → Free time / shopping → Airport transfer → Departure to Bangalore"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Personal Expenses, Activities",
        "facilities":"Hotel, Cab Service, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Karnataka Wildlife",
        "slug":"bandipur_mudumalai_wildlife",
        "price":"5D/4N",
        "image":"Wildlife.jpg",
        "itinerary":["Day 1:Bangalore Arrival - Bannerghatta National Park - Leisure","Day 2:Bangalore Mysore - Mysore Zoo - Karanji Lake - Brindavan Gardens","Day 3:Mysore Nagarhole - Jungle Safari - Overnight Stay","Day 4: Nagarhole Bandipur - Wildlife Safari - Overnight Stay","Day 5: Bandipur Bangalore - Departure"],
        "inclusions":"Resort Stay, Meals, Safari, Transfers, Guide, Sightseeing",
        "exclusions":"Entry Fees, Personal Expenses, Activities",
        "facilities":"Jungle Resort, Jeep Safari, Guide, Parking, Room Service, Campfire"
    },

    {
        "name":"Bali ",
        "slug":"Bali",
        "price":"64,850-4D/3N",
        "image":"bali.jpg",
        "itinerary":["Day 1: Departure from Bangalore → Arrival at Bali Airport → Resort check-in → Beach sunset experience → Dinner → Overnight stay","Breakfast → Kintamani Volcano tour → Bali Swing → Ubud market visit → Coffee plantation → Overnight stay","Day 3: Breakfast → Nusa Penida island tour → Kelingking Beach & Angel Billabong visit → Beach relaxation → Cruise / candlelight dinner → Overnight stay","Day 4: Breakfast → Shopping & leisure time → Airport transfer → Departure to Bangalore"],
        "inclusions":"Home pickup/drop, 3*/4*/5*Hotel Stay,Indian food, flight ticket,guide, Transfers,Visa, Sightseeing, Insurance",
        "exclusions":"Personal Expenses, Activities",
        "facilities":"Hotel, Cab Service, WiFi, Guide, Airport Transfer, Parking"
    },

    {
        "name":"Mangalore + Chikmagalur",
        "slug":"kerala_beach+mountain",
        "price":"4190/-,2D/1N",
        "image":"mangchik.jpg",
        "itinerary":["Day 1: Departure from Bangalore → Arrival in Chikmagalur → Breakfast enroute → Hotel/resort check-in → Visit Mullayanagiri Peak, Jhari Falls & coffee plantations → Lunch → Sunset viewpoint experience → Campfire & dinner → Overnight stay in Chikmagalur","Day 2: Early breakfast → Departure to Mangalore → Visit Panambur Beach, Tannirbhavi Beach & local sightseeing → Lunch → Shopping/local food experience → Departure back to Bangalore → Tour ends with beautiful beach & hill memories"],
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
