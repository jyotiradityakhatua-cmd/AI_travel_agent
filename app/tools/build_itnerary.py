# def build_itnerary(data: dict, flights, hotels):

#     flights = data.get("flights", [])
#     hotels = data.get("hotels", [])

#     return f"""
# # Travel Itinerary

# ## Trip Details
# - From: {data.get("source", "N/A")}
# - To: {data.get('destination')}
# - Departure: {data.get('departure date')}
# - Return: {data.get('return')}
# - Days: {data.get('days')}

# ---

# ##  Flights Options
# {flights}

# ---

# ##  Hotel Options
# {hotels}

# ---

# ##  Suggested Plan
# Day 1: Arrival + Relax  
# Day 2: Explore Beaches  
# Day 3: Adventure Activities  
# Day 4: Return  

# ---

#  Have a great trip!
# """




# def build_itnerary(data, flights, hotels):

#     return f"""
# # Travel Itinerary

# ## Trip Details
# - From: {data.get("source")}
# - To: {data.get("destination")}
# - Departure: {data.get("departure_date")}
# - Return: {data.get("return_date")}
# - Days: {data.get("days")}

# ---

# ## Flights Options
# {flights}

# ---

# ## Hotel Options
# {hotels}

# ---

# ## Suggested Plan

# # 10-Day Goa Travel Itinerary

# ### Day 1 – Arrival & Candolim

# * Arrive at Goa Airport and transfer to your hotel in Candolim.
# * Lunch at **Fisherman's Cove**, Candolim.
# * Relax at **Candolim Beach**.
# * Evening walk along the beach promenade.
# * Dinner at **Calamari Bathe & Binge**, Candolim.

# ---

# ### Day 2 – Forts & North Goa Beaches

# * Visit **Fort Aguada** and Aguada Lighthouse.
# * Explore **Sinquerim Beach**.
# * Lunch at **Pousada by the Beach**, Calangute.
# * Spend the afternoon at **Calangute Beach** and **Baga Beach**.
# * Dinner at **Britto's**, Baga Beach.

# ---

# ### Day 3 – Vagator & Anjuna

# * Breakfast at a local café.
# * Visit **Chapora Fort** for panoramic sea views.
# * Relax at **Vagator Beach**.
# * Lunch at **Thalassa**, Siolim.
# * Explore **Anjuna Beach**.
# * Enjoy sunset at Anjuna cliffs.
# * Evening at beach cafés and music venues.

# ---

# ### Day 4 – Water Sports Day

# * Head to Calangute or Baga Beach.
# * Activities:

#   * Parasailing
#   * Jet Ski
#   * Banana Boat Ride
#   * Speed Boat Ride
#   * Bumper Ride
# * Lunch at **Souza Lobo**, Calangute.
# * Relax at the hotel.
# * Dinner at **Fat Fish**, Baga.

# ---

# ### Day 5 – Old Goa Heritage Tour

# * Visit **Basilica of Bom Jesus**.
# * Explore **Se Cathedral**.
# * Visit **Church of St. Francis of Assisi**.
# * Lunch at **Mum's Kitchen**, Panaji.
# * Walk through the colorful lanes of **Fontainhas**.
# * Dinner at **The Black Sheep Bistro**, Panaji.

# ---

# ### Day 6 – South Goa Beaches

# * Visit **Colva Beach**.
# * Continue to **Benaulim Beach**.
# * Lunch at **Martins Corner**, Betalbatim.
# * Relax at **Palolem Beach**.
# * Sunset photography session.
# * Dinner at a beachfront shack.

# ---

# ### Day 7 – Island & Cruise Experience

# * Morning dolphin-watching tour.
# * Optional island excursion.
# * Lunch at a riverside restaurant.
# * Evening **Mandovi River Cruise** from Panaji.
# * Live music, cultural performances, and dinner onboard.

# ---

# ### Day 8 – Nature & Wildlife

# * Visit **Dudhsagar Falls**.
# * Explore **Bhagwan Mahavir Wildlife Sanctuary**.
# * Lunch near Mollem.
# * Return to hotel.
# * Relaxing evening spa session.
# * Dinner at **Vinayak Family Restaurant**, Assagao.

# ---

# ### Day 9 – Shopping & Local Experiences

# * Visit **Mapusa Market**.
# * Explore **Anjuna Flea Market** (market days).
# * Shop for:

#   * Cashews
#   * Spices
#   * Handicrafts
#   * Beachwear
# * Lunch at **Gunpowder**, Assagao.
# * Sunset at **Morjim Beach**.
# * Farewell dinner at **Thalassa** or **Antares**, Vagator.

# ---

# ### Day 10 – Leisure & Departure

# * Late breakfast.
# * Final walk on the beach.
# * Visit nearby cafés for coffee and souvenirs.
# * Lunch before departure.
# * Transfer to airport.
# * Return journey.

# ---

# ## Recommended Restaurants

# * Britto's (Baga)
# * Thalassa (Siolim)
# * Souza Lobo (Calangute)
# * Martins Corner (Betalbatim)
# * Mum's Kitchen (Panaji)
# * Pousada by the Beach (Calangute)
# * Fat Fish (Baga)
# * The Black Sheep Bistro (Panaji)

# ---

# ## Must-Try Goan Dishes

# * Goan Fish Curry Rice
# * Prawn Balchão
# * Chicken Cafreal
# * Pork Vindaloo
# * Sorpotel
# * Bebinca
# * Goan Sausage Pulao

# ---

# ## Estimated Budget (Per Person)

# * Budget Trip: ₹25,000 - ₹40,000
# * Mid-Range Trip: ₹45,000 - ₹80,000
# * Luxury Trip: ₹1,00,000+


# ### Recommended Food to Try

# * Goan Fish Curry Rice
# * Prawn Balchão
# * Chicken Cafreal
# * Pork Vindaloo
# * Bebinca
# * Goan Sausage Pulao

# ---

# ### Popular Areas to Stay

# * Calangute
# * Candolim
# * Baga
# * Vagator
# * Panaji
# * Colva

# ---

# ### Local Transport

# * Goa Miles Taxi
# * Rental Scooters
# * Self-drive Cars
# * Local Cabs


# ##  Estimated Budget

# | Category | Estimated Cost |
# |-----------|---------------|
# | Flights | ₹15,000 |
# | Hotel | ₹20,000 |
# | Food | ₹7,000 |
# | Local Transport | ₹3,000 |
# | Activities | ₹5,000 |
# | Miscellaneous | ₹2,000 |
# | **Total** | **₹52,000** |

# ---

# ## Travel Tips

# - Carry valid ID proof.
# - Keep sunscreen and sunglasses handy.
# - Book activities in advance during peak season.
# - Keep digital copies of tickets and hotel bookings.
# - Use local transport apps for convenient travel.

# ---

#  Have an amazing and memorable trip!
# """



# import requests

# def build_itnerary(data, flights, hotels):
#     prompt = f"""
# You are an expert travel planner AI.

# Generate a COMPLETE travel itinerary in MARKDOWN format only.

#  STRICT RULES:
# - Output ONLY valid Markdown
# - No JSON
# - No explanations outside itinerary
# - Make it clean and structured
# - Use headings, bullet points, tables where needed

# ---

# ## USER TRIP DETAILS
# - Source: {data.get("source")}
# - Destination: {data.get("destination")}
# - Departure Date: {data.get("departure_date")}
# - Return Date: {data.get("return_date")}
# - Duration: {data.get("days")} days

# ---

# ## FLIGHT OPTIONS
# {flights}

# ---

# ## HOTEL OPTIONS
# {hotels}

# ---

# ## REQUIRED SECTIONS

# ### 1.  Trip Overview
# Short summary of the trip

# ### 2.  Day-by-Day Itinerary
# Detailed plan for each day (morning, afternoon, evening)

# ### 3.  Food Recommendations
# Local must-try dishes

# ### 4.  Stay Areas
# Best areas to stay

# ### 5.  Transport Guide
# Local transport options

# ### 6.  Estimated Budget
# Table format breakdown

# ### 7.  Travel Tips
# Important travel advice

# ---

# Make it engaging, practical, and travel-ready.
# """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     return response.json()["response"]

# import requests

# def build_itnerary(data, flights, hotels):
#     prompt = f"""
# You are a professional AI travel planner.

#  CRITICAL RULES:
# - Create a FULL itinerary based ONLY on the number of days provided
# - You MUST cover EVERY day from Day 1 to Day {data.get("days")}
# - Do NOT skip any day
# - Do NOT use fixed templates (like Goa plan)
# - Adapt itinerary based on destination
# - Output ONLY in Markdown
# - Make it realistic, practical, and well-structured

# ---

# ## TRIP DETAILS
# - Source: {data.get("source")}
# - Destination: {data.get("destination")}
# - Departure Date: {data.get("departure_date")}
# - Return Date: {data.get("return_date")}
# - Total Days: {data.get("days")}

# ---

# ## FLIGHT OPTIONS
# {flights}

# ---

# ## HOTEL OPTIONS
# {hotels}

# ---

# ## REQUIRED OUTPUT FORMAT

# ###  Trip Overview
# Short summary of the trip

# ---

# ###  Full Day-by-Day Itinerary (MANDATORY)

# You MUST generate exactly:

# - Day 1 → Arrival + local exploration
# - Day 2 → sightseeing + activities
# ...
# - Day {data.get("days")} → departure / relaxation / shopping

# Each day must include:
# - Morning plan
# - Afternoon plan
# - Evening plan
# - Food suggestion

# ---

# ###  Food Recommendations
# Local dishes based on destination

# ---

# ### Stay Areas
# Best areas to stay in destination

# ---

# ###  Transport Guide
# Local transport options

# ---

# ###  Estimated Budget
# Table format breakdown

# ---

# ###  Travel Tips
# Practical travel advice

# ---

# Make it feel like a REAL travel planner, not generic text.
# """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     return response.json()["response"]



# import requests

# def build_itnerary(data, flights, hotels):
#     prompt = f"""
# You are a STRICT travel planner AI.

#  VERY IMPORTANT OUTPUT RULE:
# You MUST follow EXACT section order below.
# Do NOT change order.
# Do NOT mix sections.

# ---

# # REQUIRED OUTPUT STRUCTURE (STRICT ORDER)

# ## 1.  AVAILABLE FLIGHTS 
# Return ONLY the flights provided below (format them nicely in Markdown table).

# Flights Data:
# {flights}

# ---

# ## 2.  AVAILABLE HOTELS 
# Return ONLY the hotels provided below (format them nicely in Markdown table).

# Hotels Data:
# {hotels}

# ---

# ## 3. TRIP OVERVIEW

# Short summary of the trip.

# ---

# You MUST generate EXACTLY {data.get("days")} days.
# You are NOT allowed to summarize.
# You are NOT allowed to write "... and so on".
# You are NOT allowed to skip any day.

# You MUST write every single day explicitly.

# FORMAT MUST BE:

# ### Day 1: ...
# ### Day 2: ...
# ...
# ### Day {data.get("days")}: ...

# Each day MUST include:
# - Morning plan
# - Afternoon plan
# - Evening plan
# - Food suggestion

# RULE:
# - Every day must be unique
# - No repetition
# - Must feel like a real travel experience



# # ---

# # ### Stay Areas
# # Best areas to stay in destination

# # ---

# # ###  Transport Guide
# # Local transport options

# # ---

# # ###  Estimated Budget
# # Table format breakdown

# # ---

# # ###  Travel Tips
# # Practical travel advice

# # ---

# ---

# ## 5.  FOOD RECOMMENDATIONS
# Local dishes only.

# ---

# ## 6.  BEST AREAS TO STAY
# Suggest locations.

# ---

# ## 7.  TRANSPORT GUIDE
# Local transport options.

# ---

# ## 8.  ESTIMATED BUDGET
# Table format.

# ---

# ## 9.  TRAVEL TIPS

# ---

# USER INPUT:
# - Source: {data.get("source")}
# - Destination: {data.get("destination")}
# - Departure: {data.get("departure_date")}
# - Return: {data.get("return_date")}
# - Days: {data.get("days")}

# FINAL RULE:
# Flights and hotels MUST appear at the TOP before everything else.
# """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     return response.json()["response"]


# import requests

# def build_itnerary(data, flights, hotels):
#     prompt = f"""
# You are a strict AI travel planner.

# ## RULES
# - Follow EXACT section order
# - Output ONLY Markdown
# - Do NOT skip or summarize days
# - Generate ALL {data.get("days")} days explicitly
# - No "... and so on"
# - Every day must include: morning, afternoon, evening, food

# ---

# ## 1.  AVAILABLE FLIGHTS
# {flights}

# ---

# ## 2.  AVAILABLE HOTELS
# {hotels}

# ---

# ## 3.  TRIP OVERVIEW
# Short summary of the trip.

# ---

# ## 4.  DAY-BY-DAY ITINERARY
# Generate exactly {data.get("days")} days:

# Format:
# ### Day 1
# - Morning:
# - Afternoon:
# - Evening:
# - Food:

# ### Day 2
# ...

# ### Day {data.get("days")}

# Rules:
# - Each day must be unique
# - Must be realistic travel flow
# - No repetition

# ---

# ## 5.  FOOD RECOMMENDATIONS
# Local dishes only.

# ---

# ## 6.  BEST AREAS TO STAY
# List top areas.

# ---

# ## 7.  TRANSPORT GUIDE
# Local transport options.

# ---

# ## 8.  ESTIMATED BUDGET
# Markdown table only.

# ---

# ## 9.  TRAVEL TIPS
# Bullet points only.

# ---

# USER:
# Source: {data.get("source")}
# Destination: {data.get("destination")}
# Departure: {data.get("departure_date")}
# Return: {data.get("return_date")}
# Days: {data.get("days")}
# """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": True
#         }
#     )
# stream= True
# for line in response.iter_lines():
#        if line:
#             try:
#                 import json
#                 chunk = json.loads(line.decode("utf-8"))
#                 yield chunk.get("response", "")
#             except:
#                 continue


# import json
# import requests

# MODEL = "llama3"


# def build_itnerary(data: dict, flights: str, hotels: str):
#     src  = data.get("source", "")
#     dst  = data.get("destination", "")
#     dep  = data.get("departure_date", "")
#     ret  = data.get("return_date", "")
#     days = data.get("days", 3)

#     prompt = f"""You are a warm, expert travel planner. Write a complete, detailed travel itinerary in Markdown.
# Be specific, practical, and conversational — like a knowledgeable friend planning this trip for someone.
# Never skip any day. Never say "etc" or "and so on".

# TRIP:
# - From: {src} → To: {dst}
# - Departure: {dep} | Return: {ret}
# - Duration: {days} days

# FLIGHTS AVAILABLE:
# {flights}

# HOTELS AVAILABLE:
# {hotels}

# ---

# # ✈️ {src} → {dst} | {dep} – {ret} ({days} Days)

# ---

# ## 🛫 Your Flights
# Pick the best departure and return flight from the list above.
# Show: **Airline · Flight No · Time · Duration · Price**
# Give one sentence on why you picked it.

# ---

# ## 🏨 Your Hotel
# Pick the best hotel from the list above.
# Show: **Hotel Name · Price/night · Total ({days} nights)**
# Give one sentence on why it suits this trip.

# ---

# ## 📅 Day-by-Day Plan
# Write EVERY day. Day 1 through Day {days}. No exceptions.

# ### Day 1 — Arrival in {dst}
# **🌅 Morning:** [arrival + check-in + first impressions]
# **☀️ Afternoon:** [first activity or nearby attraction]
# **🌆 Evening:** [dinner spot + evening plan]
# **🍴 Eat tonight:** [specific dish + restaurant name in {dst}]

# ### Day 2
# **🌅 Morning:** ...
# **☀️ Afternoon:** ...
# **🌆 Evening:** ...
# **🍴 Eat tonight:** ...

# [Continue this exact format for Days 3 through {days - 1}]

# ### Day {days} — Departure
# **🌅 Morning:** [last activity + checkout]
# **☀️ Afternoon:** [airport transfer]
# **✈️ Flight home:** [return flight details from your chosen flight above]

# ---

# ## 🍽️ Must-Try Foods in {dst}
# Exactly 6 dishes. Format:
# **Dish name** — one line description of taste + where to find it.

# ---

# ## 🚌 Getting Around {dst}
# Practical transport guide covering:
# - Metro/local train (if available) — fares
# - Auto-rickshaw — typical fare range
# - Cab apps (Ola/Uber) — typical fare range
# - Tips for getting around like a local

# ---

# ## 💰 Full Budget Breakdown

# | Category | Cost (INR) |
# |---|---|
# | Flights — return | ₹X,XXX |
# | Hotel — {days} nights | ₹X,XXX |
# | Food & dining | ₹X,XXX |
# | Local transport | ₹X,XXX |
# | Activities & entry fees | ₹X,XXX |
# | Shopping & misc | ₹X,XXX |
# | **Total Estimated** | **₹XX,XXX** |

# ---

# ## 💡 Top 5 Travel Tips for {dst}
# Write 5 practical, specific tips — not generic advice.

# ---

# ## 🌤️ Weather & What to Pack
# What weather to expect in {dst} from {dep} to {ret}.
# Specific packing list for this trip.
# """

#     r = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": MODEL, "prompt": prompt, "stream": True},
#         stream=True,
#         timeout=300,
#     )
#     r.raise_for_status()

#     for line in r.iter_lines(decode_unicode=True):
#         if not line:
#             continue
#         try:
#             chunk = json.loads(line)
#             token = chunk.get("response", "")
#             if token:
#                 yield token
#         except Exception:
#             continue

import json
import requests

MODEL = "llama3"


def build_itnerary(data: dict, flights: str, hotels: str):
    src  = data.get("source", "")
    dst  = data.get("destination", "")
    dep  = data.get("departure_date", "")
    ret  = data.get("return_date", "")
    days = data.get("days", 3)

    prompt = f"""You are a warm, expert travel planner. Write a complete, detailed travel itinerary in Markdown.
Be specific, practical, and conversational — like a knowledgeable friend planning this trip for someone.
Never skip any day. Never say "etc" or "and so on".

TRIP:
- From: {src} → To: {dst}
- Departure: {dep} | Return: {ret}
- Duration: {days} days

FLIGHTS AVAILABLE:
{flights}

HOTELS AVAILABLE:
{hotels}

---

# ✈️ {src} → {dst} | {dep} – {ret} ({days} Days)

---

## 🛫 Your Flights
Pick the best departure and return flight from the list above.
Show: **Airline · Flight No · Time · Duration · Price**
Give one sentence on why you picked it.

---

## 🏨 Your Hotel
Pick the best hotel from the list above.
Show: **Hotel Name · Price/night · Total ({days} nights)**
Give one sentence on why it suits this trip.

---

## 📅 Day-by-Day Plan
Write EVERY day. Day 1 through Day {days}. No exceptions.

### Day 1 — Arrival in {dst}
**🌅 Morning:** [arrival + check-in + first impressions]
**☀️ Afternoon:** [first activity or nearby attraction]
**🌆 Evening:** [dinner spot + evening plan]
**🍴 Eat tonight:** [specific dish + restaurant name in {dst}]

### Day 2
**🌅 Morning:** ...
**☀️ Afternoon:** ...
**🌆 Evening:** ...
**🍴 Eat tonight:** ...

[Continue this exact format for Days 3 through {days - 1}]

### Day {days} — Departure
**🌅 Morning:** [last activity + checkout]
**☀️ Afternoon:** [airport transfer]
**✈️ Flight home:** [return flight details from your chosen flight above]

---

## 🍽️ Must-Try Foods in {dst}
Exactly 6 dishes. Format:
**Dish name** — one line description of taste + where to find it.

---

## 🚌 Getting Around {dst}
Practical transport guide covering:
- Metro/local train (if available) — fares
- Auto-rickshaw — typical fare range
- Cab apps (Ola/Uber) — typical fare range
- Tips for getting around like a local

---

## 💰 Full Budget Breakdown

| Category | Cost (INR) |
|---|---|
| Flights — return | ₹X,XXX |
| Hotel — {days} nights | ₹X,XXX |
| Food & dining | ₹X,XXX |
| Local transport | ₹X,XXX |
| Activities & entry fees | ₹X,XXX |
| Shopping & misc | ₹X,XXX |
| **Total Estimated** | **₹XX,XXX** |

---

## 💡 Top 5 Travel Tips for {dst}
Write 5 practical, specific tips — not generic advice.

---

## 🌤️ Weather & What to Pack
What weather to expect in {dst} from {dep} to {ret}.
Specific packing list for this trip.
"""

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": True},
        stream=True,
        timeout=300,
    )
    r.raise_for_status()

    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            chunk = json.loads(line)
            token = chunk.get("response", "")
            if token:
                yield token
        except Exception:
            continue