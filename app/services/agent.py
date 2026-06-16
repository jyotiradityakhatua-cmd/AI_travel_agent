# from app.tools.search_flight import search_flight
# from app.tools.search_hotel import search_hotel
# from app.tools.build_itnerary import build_itinerary


# # def travel_agent(chat_id, message):

# #     if "goa" in message.lower() and "delhi" in message.lower():

# #         if "days" not in message:
# #             return "Please provide return date and number of days"

# #         flights = search_flight("Delhi", "Goa", "6 Sep")
# #         hotels = search_hotel("Goa", 4)

# #         return build_itinerary({
# #             "source": "Delhi",
# #             "destination": "Goa",
# #             "departure": "6 Sep",
# #             "return": "10 Sep",
# #             "days": 4,
# #             "flights": flights,
# #             "hotels": hotels
# #         })

# #     return "Tell me your travel plan (source, destination, dates)"


# def travel_agent(chat_id, message, history=None):

#     history = history or []

#     full_context = " ".join([h["content"] for h in history]) + " " + message
#     full_context = full_context.lower()


#     if "delhi" in full_context and "goa" in full_context:

#         if "10th" in full_context and "4" in full_context:

#             flights = search_flight("Delhi", "Goa", "10 Sep")
#             hotels = search_hotel("Goa", 4)

#             return build_itinerary({
#                 "source": "Delhi",
#                 "destination": "Goa",
#                 "departure": "10 Sep",
#                 "return": "14 Sep",
#                 "days": 4,
#                 "flights": flights,
#                 "hotels": hotels
#             })

#         return "Got it  When is your travel date and duration?"

#     return "Tell me source and destination"

# import json
# from app.llm.ollama_client import ask_ollama
# from app.llm.prompt import SYSTEM_PROMPT
# from app.tools.search_flight import search_flight
# from app.tools.search_hotel import search_hotel
# from app.tools.build_itnerary import build_itinerary


# def travel_agent(chat_id, message, history):

#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT}
#     ]


#     for h in history:
#         messages.append({
#             "role": h["role"],
#             "content": h["content"]
#         })


#     messages.append({"role": "user", "content": message})


#     llm_output = ask_ollama(messages)

#     data = json.loads(llm_output)


#     if data.get("missing_fields"):
#         return f"Please provide: {', '.join(data['missing_fields'])}"


#     flights = search_flight(
#         data["source"],
#         data["destination"],
#         data["departure_date"]
#     )

#     hotels = search_hotel(
#         data["destination"],
#         data["days"]
#     )

#     itinerary = build_itinerary({
#         **data,
#         "flights": flights,
#         "hotels": hotels
#     })

#     return itinerary














# import json
# import re
# import requests
# from datetime import datetime, timedelta

# from app.db.chat_repo import get_chat_history
# from app.tools.search_flight import search_flight
# from app.tools.search_hotel import search_hotel
# from app.tools.build_itnerary import build_itnerary

# OLLAMA_URL = "http://localhost:11434/api/chat"
# MODEL = "llama3"


# def _build_system() -> str:
#     today = datetime.now().strftime("%d %b %Y")
#     return f"""You are a friendly AI travel assistant. Today is {today}.

# You have exactly 3 tools. You MUST output ONLY a JSON object — no text before or after it, ever.

# ═══════════════════════════════════════════════
# TOOL 1 — search_flights
# Use when: user asks about flights, wants to see flight options
# Required: source, destination, departure_date
# Optional: return_date (only include if user explicitly gave a return date)
# Output: {{"tool":"search_flights","source":"...","destination":"...","departure_date":"...","return_date":"..."}}

# TOOL 2 — search_hotels
# Use when: user asks about hotels, accommodation, where to stay
# Required: destination, check_in, check_out
# Output: {{"tool":"search_hotels","destination":"...","check_in":"...","check_out":"..."}}

# TOOL 3 — build_itinerary
# Use when: user asks for a trip plan, itinerary, travel plan
# Required: source, destination, departure_date, return_date, days
# Output: {{"tool":"build_itinerary","source":"...","destination":"...","departure_date":"...","return_date":"...","days":<number>}}

# TOOL 4 — chat
# Use when: info is missing OR you need to ask something OR user is just chatting
# Output: {{"tool":"chat","message":"<your natural conversational reply here>"}}
# ═══════════════════════════════════════════════

# CONVERSATION FLOW — follow this strictly:

# STEP 1: If user gives source + destination but no dates → ask departure date only.
# STEP 2: After getting departure date → ask "What's your return date? Or how many days are you staying?"
# STEP 3: After getting return date/days → ask "Got it! Would you like to see flights, hotels, or a full itinerary?"
# STEP 4: Call the tool the user chooses.

# SPECIAL CASES:
# - If user asks for BOTH flights and hotels → output TWO JSON objects, one per line.
# - If user asks for itinerary → call build_itinerary (it includes flights + hotels internally).
# - If user asks for flights on a specific date → call search_flights with ONLY that date as departure_date. Do NOT add return_date unless user gave one.
# - If user gives ALL info (source, destination, departure, return) upfront → go to STEP 3 immediately.
# - If user says "N days" → compute return_date = departure_date + N days yourself before calling the tool.

# STRICT RULES:
# - Output ONLY JSON. Never output plain text outside a JSON object.
# - Use chat tool for ALL conversational replies, questions, and clarifications.
# - Never call search_flights with a return_date the user did not provide.
# - Never call build_itinerary unless you have source, destination, departure_date AND return_date.
# - Dates format: "D Mon YYYY" e.g. "15 Jun 2025".
# - chat tool messages should be warm, short, human — like texting a knowledgeable friend.
# """


# def _stream_generate(prompt: str):
#     """Stream tokens from /api/generate."""
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


# def _stream_chat(messages: list):
#     """Stream tokens from /api/chat."""
#     r = requests.post(
#         OLLAMA_URL,
#         json={"model": MODEL, "messages": messages, "stream": True},
#         stream=True,
#         timeout=300,
#     )
#     r.raise_for_status()
#     for line in r.iter_lines(decode_unicode=True):
#         if not line:
#             continue
#         try:
#             chunk = json.loads(line)
#             token = chunk.get("message", {}).get("content", "")
#             if token:
#                 yield token
#         except Exception:
#             continue


# def _llm_decide(messages: list) -> str:
#     """Non-streaming call to get tool decision JSON."""
#     r = requests.post(
#         OLLAMA_URL,
#         json={"model": MODEL, "messages": messages, "stream": False},
#         timeout=60,
#     )
#     r.raise_for_status()
#     return r.json()["message"]["content"].strip()


# def _extract_all_tools(text: str) -> list[dict]:
#     """Extract one or more tool JSON objects from LLM output."""
#     text = re.sub(r"```(?:json)?|```", "", text).strip()
#     results = []
#     # Try whole text as single JSON
#     try:
#         d = json.loads(text)
#         if "tool" in d:
#             return [d]
#     except Exception:
#         pass
#     # Find all JSON objects
#     for m in re.finditer(r'\{[^{}]*"tool"\s*:\s*"[^"]*"[^{}]*\}', text, re.DOTALL):
#         try:
#             d = json.loads(m.group())
#             if "tool" in d:
#                 results.append(d)
#         except Exception:
#             pass
#     return results


# def _build_messages(history_rows, new_message: str) -> list:
#     msgs = [{"role": "system", "content": _build_system()}]
#     for row in history_rows:
#         role = "assistant" if row.role == "assistant" else "user"
#         content = row.message
#         if role == "assistant" and len(content) > 600:
#             content = "[Full travel response shown to user]"
#         msgs.append({"role": role, "content": content})
#     msgs.append({"role": "user", "content": new_message})
#     return msgs


# def _days_between(dep: str, ret: str) -> int:
#     for fmt in ["%d %b %Y", "%d %B %Y", "%d %b", "%d %B"]:
#         try:
#             return max((datetime.strptime(ret.strip(), fmt) - datetime.strptime(dep.strip(), fmt)).days, 1)
#         except Exception:
#             pass
#     return 3


# def _add_days(dep: str, days: int) -> str:
#     for fmt in ["%d %b %Y", "%d %b"]:
#         try:
#             return (datetime.strptime(dep.strip(), fmt) + timedelta(days=days)).strftime("%-d %b %Y")
#         except Exception:
#             pass
#     return ""


# def _stream_text(text: str):
#     """Stream text character by character for human-like feel."""
#     for ch in text:
#         yield ch


# def _run_tool(tool_call: dict, all_messages: list):
#     """Execute a single tool and stream its output."""
#     tool = tool_call.get("tool")

#     # ── chat (conversational reply) ───────────────────────────────────────────
#     if tool == "chat":
#         msg = tool_call.get("message", "")
#         yield from _stream_text(msg)
#         return

#     # ── search_flights ────────────────────────────────────────────────────────
#     if tool == "search_flights":
#         src = tool_call.get("source", "")
#         dst = tool_call.get("destination", "")
#         dep = tool_call.get("departure_date", "")
#         ret = tool_call.get("return_date") or ""
#         days = tool_call.get("days")
#         if days and dep and not ret:
#             ret = _add_days(dep, int(days))

#         header = f"Searching flights from **{src}** to **{dst}** on {dep}... ✈️\n\n"
#         yield from _stream_text(header)

#         try:
#             raw = search_flight(src, dst, dep, ret)
#         except Exception as e:
#             yield f"Sorry, couldn't fetch flights: {e}"
#             return

#         prompt = f"""You are a friendly travel assistant. Present these flight options in warm, clear Markdown.

# Route: {src} → {dst}
# Date: {dep}{(" | Return: " + ret) if ret else " (one-way)"}

# Raw flight data:
# {raw}

# Format each flight as:
# ✈️ **Airline · Flight No** | `HH:MM → HH:MM` | ⏱ Duration | 💰 ₹Price

# Separate departure and return flights with a clear heading if return flights exist.
# At the end, highlight your best value pick with a short reason.
# Be warm and conversational — like texting a knowledgeable friend.
# """
#         yield from _stream_generate(prompt)
#         return

#     # ── search_hotels ─────────────────────────────────────────────────────────
#     if tool == "search_hotels":
#         dst      = tool_call.get("destination", "")
#         check_in = tool_call.get("check_in", "")
#         check_out= tool_call.get("check_out", "")
#         nights   = _days_between(check_in, check_out)

#         header = f"Searching hotels in **{dst}** ({check_in} → {check_out})... 🏨\n\n"
#         yield from _stream_text(header)

#         try:
#             raw = search_hotel(dst, check_in, check_out)
#         except Exception as e:
#             yield f"Sorry, couldn't fetch hotels: {e}"
#             return

#         prompt = f"""You are a friendly travel assistant. Present these hotel options in warm, clear Markdown.

# Destination: {dst}
# Check-in: {check_in} | Check-out: {check_out} | {nights} nights

# Raw hotel data:
# {raw}

# Group hotels as:
# ### 💚 Budget
# ### 🌟 Mid-Range  
# ### 👑 Luxury

# For each hotel:
# 🏨 **Hotel Name** ⭐ Rating | ₹X,XXX/night | ₹X,XXX total | 📌 Standout feature

# End with your top pick and a short reason why.
# Be warm and conversational — like advising a friend.
# """
#         yield from _stream_generate(prompt)
#         return

#     # ── build_itinerary ───────────────────────────────────────────────────────
#     if tool == "build_itinerary":
#         src  = tool_call.get("source", "")
#         dst  = tool_call.get("destination", "")
#         dep  = tool_call.get("departure_date", "")
#         ret  = tool_call.get("return_date", "")
#         days = tool_call.get("days")

#         if days and dep and not ret:
#             ret = _add_days(dep, int(days))
#         if not days:
#             days = _days_between(dep, ret)
#         try:
#             days = int(days)
#         except Exception:
#             days = 3

#         header = f"Planning your **{days}-day trip** from **{src}** to **{dst}** ({dep} → {ret})! Let me search flights and hotels...\n\n"
#         yield from _stream_text(header)

#         try:
#             flights = search_flight(src, dst, dep, ret)
#         except Exception as e:
#             flights = f"(Flights unavailable: {e})"

#         try:
#             hotels = search_hotel(dst, dep, ret)
#         except Exception as e:
#             hotels = f"(Hotels unavailable: {e})"

#         yield from build_itnerary(
#             {"source": src, "destination": dst,
#              "departure_date": dep, "return_date": ret, "days": days},
#             flights, hotels,
#         )
#         return


# def travel_agent(chat_id: str, message: str, db):
#     history = get_chat_history(db=db, chat_id=chat_id)
#     messages = _build_messages(history, message)

#     print(f"\n[AGENT] chat={chat_id} history={len(history)}")

#     try:
#         decision = _llm_decide(messages)
#     except Exception as e:
#         yield f"Sorry, I can't reach the AI model right now. ({e})"
#         return

#     print(f"[AGENT] Decision → {decision[:300]}")

#     tool_calls = _extract_all_tools(decision)

#     # No tool found — stream a plain conversational reply
#     if not tool_calls:
#         print("[AGENT] No tool call — streaming plain reply")
#         try:
#             for token in _stream_chat(messages):
#                 yield token
#         except Exception:
#             yield decision
#         return

#     print(f"[AGENT] Tools to run: {[t.get('tool') for t in tool_calls]}")

#     # Run each tool — supports multiple tools (e.g. flights + hotels together)
#     for i, tool_call in enumerate(tool_calls):
#         if i > 0:
#             yield "\n\n---\n\n"  # separator between multiple tool outputs
#         yield from _run_tool(tool_call, messages)







# return StreamingResponse(
#     stream(),
#     media_type="text/plain"
# )

# from datetime import datetime, timedelta

# from fastapi.responses import StreamingResponse

# from app.services.llm_service import extract_state_with_llm
# from app.tools.search_flight import search_flight
# from app.tools.search_hotel import search_hotel
# from app.tools.build_itnerary import build_itnerary

# from app.db.chat_state import get_state, save_state
# from app.db.chat_repo import save_message


# def travel_agent(chat_id, message, db):


#     state = get_state(db, chat_id)

#     if state is None:
#         state = {
#             "source": None,
#             "destination": None,
#             "departure_date": None,
#             "return_date": None,
#             "days": None,
#         }

#     updated = extract_state_with_llm(state, message)

#     state.update({
#         k: v for k, v in updated.items()
#         if v not in [None, "", []]
#     })


#     try:
#         if state.get("departure_date") and state.get("return_date"):

#             dep = datetime.strptime(state["departure_date"], "%d %b")
#             ret = datetime.strptime(state["return_date"], "%d %b")

#             state["days"] = (ret - dep).days

#         elif state.get("departure_date") and state.get("days") and not state.get("return_date"):

#             dep = datetime.strptime(state["departure_date"], "%d %b")
#             ret = dep + timedelta(days=int(state["days"]))

#             state["return_date"] = ret.strftime("%d %b")

#     except Exception as e:
#         print("Date calculation error:", e)


#     save_state(db, chat_id, state)

#     required = ["source", "destination", "departure_date"]

#     missing = [f for f in required if not state.get(f)]

#     if missing:
#         return StreamingResponse(iter([f"Please provide: {', '.join(missing)}"]),
#                                  media_type="text/plain")

#     if not state.get("days") and not state.get("return_date"):
#         return StreamingResponse(iter(["Please provide either days or return_date"]),
#                                  media_type="text/plain")

#     flights = search_flight(
#         state["source"],
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     hotels = search_hotel(
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     def stream():


#         yield "Generating your travel itinerary...\n\n"

#         itinerary_text = ""

#         for chunk in build_itnerary(state, flights, hotels):
#             itinerary_text += chunk
#             yield chunk

   

#     return StreamingResponse(
#         stream(),
#         media_type="text/plain"
#     )








# def travel_agent(chat_id, message, db):

#     state = get_state(db, chat_id)

#     if not state:
#         state = {
#             "source": None,
#             "destination": None,
#             "departure_date": None,
#             "return_date": None,
#             "days": None,
#         }

#     updated = extract_state_with_llm(state, message)

#     state.update({
#         k: v for k, v in updated.items()
#         if v not in [None, "", []]
#     })

 
#     try:
#         dep = state.get("departure_date")
#         ret = state.get("return_date")
#         days = state.get("days")

#         if dep and ret:
#             dep_dt = datetime.strptime(dep, "%d %b")
#             ret_dt = datetime.strptime(ret, "%d %b")
#             state["days"] = (ret_dt - dep_dt).days

#         elif dep and days and not ret:
#             dep_dt = datetime.strptime(dep, "%d %b")
#             ret_dt = dep_dt + timedelta(days=int(days))
#             state["return_date"] = ret_dt.strftime("%d %b")

#     except Exception as e:
#         print("Date calculation error:", e)


#     save_state(db, chat_id, state)


#     required_fields = ["source", "destination", "departure_date"]

#     missing = [f for f in required_fields if not state.get(f)]

#     if missing:
#         return f"Please provide: {', '.join(missing)}"

#     if not state.get("days") and not state.get("return_date"):
#         return "Please provide either days or return_date"


#     flights = search_flight(
#         state["source"],
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     hotels = search_hotel(
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     itinerary = build_itnerary(
#         state,
#         flights,
#         hotels
#     )

#     return itinerary





# def travel_agent_stream(chat_id, message, db):


#     state = get_state(db, chat_id)

#     if not state:
#         state = {
#             "source": None,
#             "destination": None,
#             "departure_date": None,
#             "return_date": None,
#             "days": None,
#         }

#     updated = extract_state_with_llm(state, message)

#     state.update({
#         k: v for k, v in updated.items()
#         if v not in [None, "", []]
#     })

#     yield " Updating travel details...\n\n"


#     try:
#         dep = state.get("departure_date")
#         ret = state.get("return_date")

#         if dep and ret:
#             dep_dt = datetime.fromisoformat(dep)
#             ret_dt = datetime.fromisoformat(ret)
#             state["days"] = (ret_dt - dep_dt).days

#         elif dep and state.get("days") and not ret:
#             dep_dt = datetime.fromisoformat(dep)
#             ret_dt = dep_dt + timedelta(days=int(state["days"]))
#             state["return_date"] = ret_dt.date().isoformat()

#     except Exception as e:
#         yield f" Date parsing error: {e}\n\n"

#     save_state(db, chat_id, state)

#     required = ["source", "destination", "departure_date"]

#     missing = [f for f in required if not state.get(f)]

#     if missing:
#         yield f" Missing fields: {', '.join(missing)}"
#         return

#     if not state.get("days") and not state.get("return_date"):
#         yield " Please provide either days or return_date"
#         return


#     yield "\nFetching flights...\n"

#     flights = search_flight(
#         state["source"],
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     yield flights + "\n"


#     yield "\n Fetching hotels...\n"

#     hotels = search_hotel(
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     yield hotels + "\n"

  
#     yield "\n Generating itinerary...\n\n"
# from datetime import datetime, timedelta


# def travel_agent_stream(chat_id, message, db):

#     # =========================
#     # 1. LOAD STATE
#     # =========================
#     state = get_state(db, chat_id)

#     if not state:
#         state = {
#             "source": None,
#             "destination": None,
#             "departure_date": None,
#             "return_date": None,
#             "days": None,
#         }
    

#         yield f"Chat ID: {chat_id}\n\n"
#     yield "Understanding your travel request...\n\n"


#     updated = extract_state_with_llm(state, message)

#     state.update({
#         k: v for k, v in updated.items()
#         if v not in [None, "", []]
#     })

#     yield f"Route: {state.get('source')} → {state.get('destination')}\n"


#     try:
#         dep = state.get("departure_date")
#         ret = state.get("return_date")
#         days = state.get("days")

#         if dep and ret:
#             dep_dt = datetime.strptime(dep, "%d %b")
#             ret_dt = datetime.strptime(ret, "%d %b")
#             state["days"] = (ret_dt - dep_dt).days

#         elif dep and days and not ret:
#             dep_dt = datetime.strptime(dep, "%d %b")
#             ret_dt = dep_dt + timedelta(days=int(days))
#             state["return_date"] = ret_dt.strftime("%d %b")

#     except Exception:
#         yield "Date parsing issue detected, using fallback format\n"

#     save_state(db, chat_id, state)


#     required_fields = ["source", "destination", "departure_date"]

#     missing = [f for f in required_fields if not state.get(f)]

#     if missing:
#         yield f"\nplease provide: {', '.join(missing)}"
#         return

#     if not state.get("days") and not state.get("return_date"):
#         yield "\nPlease provide either days or return_date"
#         return

#     # =========================
#     # 6. FLIGHTS
#     # =========================
#     yield "\nSearching flights...\n"

#     flights = search_flight(
#         state["source"],
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     yield flights + "\n"

#     # =========================
#     # 7. HOTELS
#     # =========================
#     yield "\nSearching hotels...\n"

#     hotels = search_hotel(
#         state["destination"],
#         state["departure_date"],
#         state["return_date"]
#     )

#     yield hotels + "\n"

#     # =========================
#     # 8. ITINERARY GENERATION
#     # =========================
#     yield "\nGenerating itinerary...\n\n"

#     itinerary = build_itnerary(state, flights, hotels)

#     # =========================
#     # 9. STREAM FINAL OUTPUT
#     # =========================
#     for word in itinerary.split(" "):
#         yield word + " "



# import json
# import re
# import requests
# from datetime import datetime, timedelta

# from app.db.chat_repo import get_chat_history
# from app.tools.search_flight import search_flight
# from app.tools.search_hotel import search_hotel
# from app.tools.build_itnerary import build_itnerary

# OLLAMA_URL = "http://localhost:11434/api/chat"
# MODEL = "llama3"


# def _build_system() -> str:
#     today = datetime.now().strftime("%d %b %Y")
#     return f"""You are a friendly AI travel assistant. CURRENT DATE is {today}.

# You MUST always respond with ONLY a JSON object — never plain text, never explanation.

# ═══════════════════════════════════════════════════════
# TOOLS
# ═══════════════════════════════════════════════════════

# {{"tool":"chat","message":"..."}}
#   → For ALL questions, clarifications, confirmations, and conversational replies.
#   → message must be warm, natural, 1–2 sentences. Like texting a friend.

# {{"tool":"search_flights","source":"...","destination":"...","departure_date":"...","return_date":""}}
#   → Search for flights. Set return_date="" unless user explicitly gave one.

# {{"tool":"search_hotels","destination":"...","check_in":"...","check_out":"..."}}
#   → Search for hotels.

# {{"tool":"build_itinerary","source":"...","destination":"...","departure_date":"...","return_date":"...","days":0}}
#   → Build a full trip plan with flights, hotels, and day-by-day itinerary.

# ═══════════════════════════════════════════════════════
# STRICT CONVERSATION WORKFLOW
# ═══════════════════════════════════════════════════════

# Follow these steps IN ORDER. Never skip. Never combine steps.

# STEP 1 — Need source + destination
#   If missing → {{"tool":"chat","message":"Where are you flying from and to? 🌍"}}

# STEP 2 — Need departure date
#   Have source + destination but no departure date →
#   {{"tool":"chat","message":"When are you planning to depart? 📅"}}

# STEP 3 — Need return date or days
#   Have source + destination + departure but no return →
#   {{"tool":"chat","message":"What's your return date? Or how many days are you staying? 🗓️"}}

# STEP 4 — All 4 fields collected. Ask what they want:
#   {{"tool":"chat","message":"Perfect! 🎉 Here's your trip summary:\\n✅ source → destination\\n📅  → return date\\n\\nWhat would you like?\\n✈️ Flights\\n🏨 Hotels\\n📋 Full Itinerary\\n\\n(You can pick one, two, or all three!)"}}


# ═══════════════════════════════════════════════════════
# DATE VALIDATION
# ═══════════════════════════════════════════════════════
# -1. Today's date is exactly {today}.
# 2. Any date earlier than {today} is a PAST DATE.
# 3. Never search flights, hotels, or build itineraries using a past date.
# 4. If a user gives a past date, respond ONLY:
# - ***Today is {today}. Any date before today is a PAST DATE.
# - If user gives a past date (e.g. "10 Jan 2024", "5 Mar 2023", "15 Jun 2026"):
#   → {{"tool":"chat","message":"Oops! That date has already passed 😅 Could you give me a future date?"}}***
# - ***If user gives only day + month with no year (e.g. "16 Jun"):***
#   → ***Assume the nearest future occurrence of that date.***
#   → ***If "15 Jun" has passed this year, use next year automatically. Do NOT ask for year.
# - Always store dates as "D Mon YYYY" e.g. "16 Jun 2026".***
# - If user gives a past date (e.g. "10 Jan 2024", "5 Mar 2023", "15 Jun 2026"):
#   → {{"tool":"chat","message":"Oops! That date has already passed 😅 Could you give me a future date?"}}***

# ═══════════════════════════════════════════════════════
# TOOL CALLING RULES
# ═══════════════════════════════════════════════════════

# - User says "flights" → search_flights only
# - User says "hotels" → search_hotels only
# - User says "itinerary" or "plan" → build_itinerary only
# - User says "flights and hotels" → output search_flights JSON on line 1, search_hotels JSON on line 2
# - User says "flights and itinerary" → search_flights on line 1, build_itinerary on line 2
# - User says "all" or "everything" → all 3 tools, one per line
# - User asks "show me flights from X to Y on DATE" → call search_flights immediately with that date, return_date=""
# - If user says "N days" → compute return_date = departure_date + N days yourself, then proceed

# ═══════════════════════════════════════════════════════
# ABSOLUTE RULES
# ═══════════════════════════════════════════════════════

# 1. NEVER output plain text. Every single response must be a JSON object.
# 2. NEVER skip STEP 2 or STEP 3 — always ask for missing fields one at a time.
# 3. NEVER add return_date to search_flights unless user explicitly gave one.
# 4. NEVER call build_itinerary without all 4 fields confirmed.
# 5. NEVER call any tool before completing STEP 4 (unless user directly asked for flights/hotels with enough info).
# 6. Multiple tools = one JSON per line, nothing else between them.
# 7. Dates always in "D Mon YYYY" format.
# 8. chat messages: short, warm, friendly — 1–2 sentences max.
# 9. Date before today is PASTDATE whenever user gives you past date ask for present or future date
# """


# def _stream_generate(prompt: str):
#     r = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": MODEL, "prompt": prompt, "stream": True},
#         stream=True, timeout=300,
#     )
#     r.raise_for_status()
#     for line in r.iter_lines(decode_unicode=True):
#         if not line:
#             continue
#         try:
#             token = json.loads(line).get("response", "")
#             if token:
#                 yield token
#         except Exception:
#             continue


# def _stream_chat(messages: list):
#     r = requests.post(
#         OLLAMA_URL,
#         json={"model": MODEL, "messages": messages, "stream": True},
#         stream=True, timeout=300,
#     )
#     r.raise_for_status()
#     for line in r.iter_lines(decode_unicode=True):
#         if not line:
#             continue
#         try:
#             token = json.loads(line).get("message", {}).get("content", "")
#             if token:
#                 yield token
#         except Exception:
#             continue


# def _llm_decide(messages: list) -> str:
#     r = requests.post(
#         OLLAMA_URL,
#         json={"model": MODEL, "messages": messages, "stream": False},
#         timeout=60,
#     )
#     r.raise_for_status()
#     return r.json()["message"]["content"].strip()


# def _extract_all_tools(text: str) -> list:
#     text = re.sub(r"```(?:json)?|```", "", text).strip()

#     # Try whole text as JSON
#     try:
#         d = json.loads(text)
#         if isinstance(d, dict) and "tool" in d:
#             return [d]
#     except Exception:
#         pass

#     # Find all {...} blocks
#     results = []
#     for m in re.finditer(r'\{[^{}]+\}', text, re.DOTALL):
#         try:
#             d = json.loads(m.group())
#             if isinstance(d, dict) and "tool" in d:
#                 results.append(d)
#         except Exception:
#             pass
#     if results:
#         return results

#     # Fix single quotes / trailing commas
#     fixed = re.sub(r"'", '"', text)
#     fixed = re.sub(r',\s*([}\]])', r'\1', fixed)
#     try:
#         d = json.loads(fixed)
#         if isinstance(d, dict) and "tool" in d:
#             return [d]
#     except Exception:
#         pass

#     return []


# def _force_retry(messages: list, original: str) -> list:
#     """If LLM gave plain text, force it to wrap in chat tool JSON."""
#     retry = messages + [
#         {"role": "assistant", "content": original},
#         {"role": "user", "content":
#             "REMINDER: You must respond with ONLY a JSON object. "
#             "Wrap your previous reply as: "
#             '{"tool":"chat","message":"<your reply here>"} '
#             "Output only the JSON, nothing else."
#         }
#     ]
#     r = requests.post(
#         OLLAMA_URL,
#         json={"model": MODEL, "messages": retry, "stream": False},
#         timeout=120,
#     )
#     r.raise_for_status()
#     return _extract_all_tools(r.json()["message"]["content"].strip())


# def _build_messages(history_rows, new_message: str) -> list:
#     msgs = [{"role": "system", "content": _build_system()}]
#     for row in history_rows:
#         role = "assistant" if row.role == "assistant" else "user"
#         content = row.message
#         if role == "assistant" and len(content) > 600:
#             content = "[Full travel response shown to user]"
#         msgs.append({"role": role, "content": content})
#     msgs.append({"role": "user", "content": new_message})
#     return msgs


# def _days_between(dep: str, ret: str) -> int:
#     for fmt in ["%d %b %Y", "%d %B %Y", "%d %b", "%d %B"]:
#         try:
#             return max(
#                 (datetime.strptime(ret.strip(), fmt) - datetime.strptime(dep.strip(), fmt)).days, 1
#             )
#         except Exception:
#             pass
#     return 3


# def _add_days(dep: str, days: int) -> str:
#     for fmt in ["%d %b %Y", "%d %b"]:
#         try:
#             return (datetime.strptime(dep.strip(), fmt) + timedelta(days=days)).strftime("%-d %b %Y")
#         except Exception:
#             pass
#     return ""


# def _stream_text(text: str):
#     for ch in text:
#         yield ch


# def _run_tool(tool_call: dict, all_messages: list):
#     tool = tool_call.get("tool")

#     # ── chat ──────────────────────────────────────────────────────────────────
#     if tool == "chat":
#         yield from _stream_text(tool_call.get("message", ""))
#         return

#     # ── search_flights ────────────────────────────────────────────────────────
#     if tool == "search_flights":
#         src = tool_call.get("source", "")
#         dst = tool_call.get("destination", "")
#         dep = tool_call.get("departure_date", "")
#         ret = tool_call.get("return_date") or ""
#         days = tool_call.get("days")
#         if days and dep and not ret:
#             ret = _add_days(dep, int(days))

#         yield from _stream_text(
#             f"Searching flights from **{src}** to **{dst}** on {dep}... ✈️\n\n"
#         )

#         try:
#             raw = search_flight(src, dst, dep, ret)
#         except Exception as e:
#             yield f"Sorry, couldn't fetch flights: {e}"
#             return

#         yield from _stream_generate(f"""You are a friendly travel assistant. Present these flight results in warm, clear Markdown. Stream naturally like a human typing.

# Route: {src} → {dst}
# {f"Departure: {dep} | Return: {ret}" if ret else f"Departure: {dep} (one-way — show departure flights only, no return section)"}

# Raw flight data:
# {raw}

# ## 🛫 Departure Flights ({dep})
# ✈️ **Airline · Flight No** | `HH:MM → HH:MM` | ⏱ Duration | 💰 ₹Price

# {"## 🛬 Return Flights (" + ret + ")" if ret else ""}

# End with:
# ⭐ **Best Pick:** [Airline · reason in one sentence]

# Be warm and conversational.
# """)
#         return

#     # ── search_hotels ─────────────────────────────────────────────────────────
#     if tool == "search_hotels":
#         dst      = tool_call.get("destination", "")
#         check_in = tool_call.get("check_in", "")
#         check_out= tool_call.get("check_out", "")
#         nights   = _days_between(check_in, check_out)

#         yield from _stream_text(
#             f"Searching hotels in **{dst}** ({check_in} → {check_out})... 🏨\n\n"
#         )

#         try:
#             raw = search_hotel(dst, check_in, check_out)
#         except Exception as e:
#             yield f"Sorry, couldn't fetch hotels: {e}"
#             return

#         yield from _stream_generate(f"""You are a friendly travel assistant. Present these hotel options in warm, clear Markdown. Stream naturally.

# Destination: {dst} | {check_in} – {check_out} | {nights} nights

# Raw hotel data:
# {raw}

# ### 💚 Budget
# ### 🌟 Mid-Range
# ### 👑 Luxury

# Each hotel:
# 🏨 **Hotel Name** ⭐Rating | ₹X,XXX/night | ₹X,XXX total ({nights} nights) | 📌 Best feature

# End with:
# ⭐ **Top Pick:** [Hotel name · reason in one sentence]

# Be warm and conversational.
# """)
#         return

#     # ── build_itinerary ───────────────────────────────────────────────────────
#     if tool == "build_itinerary":
#         src  = tool_call.get("source", "")
#         dst  = tool_call.get("destination", "")
#         dep  = tool_call.get("departure_date", "")
#         ret  = tool_call.get("return_date", "")
#         days = tool_call.get("days")

#         if days and dep and not ret:
#             ret = _add_days(dep, int(days))
#         if not days:
#             days = _days_between(dep, ret)
#         try:
#             days = int(days)
#         except Exception:
#             days = 3

#         yield from _stream_text(
#             f"Let's build your **{days}-day trip** from **{src}** to **{dst}** "
#             f"({dep} → {ret})! 🎉 Fetching flights and hotels first...\n\n"
#         )

#         try:
#             flights = search_flight(src, dst, dep, ret)
#         except Exception as e:
#             flights = f"(Flights unavailable: {e})"
#         try:
#             hotels = search_hotel(dst, dep, ret)
#         except Exception as e:
#             hotels = f"(Hotels unavailable: {e})"

#         yield from build_itnerary(
#             {"source": src, "destination": dst,
#              "departure_date": dep, "return_date": ret, "days": days},
#             flights, hotels,
#         )
#         return


# def travel_agent(chat_id: str, message: str, db):
#     history = get_chat_history(db=db, chat_id=chat_id)
#     messages = _build_messages(history, message)

#     print(f"\n[AGENT] chat={chat_id} history={len(history)}")

#     try:
#         decision = _llm_decide(messages)
#     except Exception as e:
#         yield f"Sorry, I can't reach the AI model right now. ({e})"
#         return

#     print(f"[AGENT] Decision → {decision[:300]}")

#     tool_calls = _extract_all_tools(decision)

#     # Retry if LLM gave plain text
#     if not tool_calls:
#         print("[AGENT] Parse failed — retrying")
#         tool_calls = _force_retry(messages, decision)

#     # Final fallback: stream conversational reply
#     if not tool_calls:
#         print("[AGENT] Retry failed — streaming plain reply")
#         try:
#             for token in _stream_chat(messages):
#                 yield token
#         except Exception:
#             yield decision
#         return

#     print(f"[AGENT] Tools → {[t.get('tool') for t in tool_calls]}")

#     for i, tool_call in enumerate(tool_calls):
#         if i > 0:
#             yield "\n\n---\n\n"
#         yield from _run_tool(tool_call, messages)


import json
import re
import requests
import calendar
from datetime import datetime, timedelta

from app.db.chat_repo import get_chat_history
from app.tools.search_flight import search_flight
from app.tools.search_hotel import search_hotel
from app.tools.build_itnerary import build_itnerary

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"
TODAY = datetime.now()

# ── Month lookup ──────────────────────────────────────────────────────────────
MONTH_MAP = {
    "jan": ("Jan", 1), "january": ("Jan", 1),
    "feb": ("Feb", 2), "february": ("Feb", 2),
    "mar": ("Mar", 3), "march": ("Mar", 3),
    "apr": ("Apr", 4), "april": ("Apr", 4),
    "may": ("May", 5),
    "jun": ("Jun", 6), "june": ("Jun", 6),
    "jul": ("Jul", 7), "july": ("Jul", 7),
    "aug": ("Aug", 8), "august": ("Aug", 8),
    "sep": ("Sep", 9), "sept": ("Sep", 9), "september": ("Sep", 9),
    "oct": ("Oct", 10), "october": ("Oct", 10),
    "nov": ("Nov", 11), "november": ("Nov", 11),
    "dec": ("Dec", 12), "december": ("Dec", 12),
}


def _validate_dates_in_message(message: str):
    """
    Scans message for date patterns and validates each one.
    Returns (valid_flag: bool, error_message: str | None)
    - invalid day for month (31 Jun, 30 Feb, 0 Aug, -1 Jul)
    - past date
    Auto-infers year for day+month patterns → nearest future date.
    """
    low = message.lower()

    # Match: DD Mon [YYYY] or Mon DD [YYYY]
    date_re = (
        r"\b(-?\d{1,2})(?:st|nd|rd|th)?\s+"
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
        r"(?:\s+(\d{4}))?\b"
        r"|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
        r"\s+(-?\d{1,2})(?:st|nd|rd|th)?(?:\s+(\d{4}))?\b"
    )

    for m in re.finditer(date_re, low):
        g = m.groups()
        # DD Mon [YYYY]
        if g[0] is not None:
            day_s, mon_key, yr_s = g[0], g[1], g[2]
        else:
            # Mon DD [YYYY]
            mon_key, day_s, yr_s = g[3], g[4], g[5]

        if mon_key not in MONTH_MAP:
            continue

        mon_label, mon_num = MONTH_MAP[mon_key]

        # Day must be positive integer
        try:
            day = int(day_s)
        except Exception:
            continue

        if day <= 0:
            return False, (
                f"⚠️ **{day_s} {mon_label}** is not a valid date. "
                f"Day must be between 1 and {calendar.monthrange(TODAY.year, mon_num)[1]}. "
                f"Please enter a valid date."
            )

        # Infer year
        if yr_s:
            year = int(yr_s)
        else:
            # Pick nearest future year
            year = None
            for yr in [TODAY.year, TODAY.year + 1]:
                max_d = calendar.monthrange(yr, mon_num)[1]
                if day > max_d:
                    # Invalid for both years — report error
                    return False, (
                        f"⚠️ **{day} {mon_label}** is not a valid date — "
                        f"{mon_label} only has {max_d} days. "
                        f"Did you mean **{max_d} {mon_label}**?"
                    )
                try:
                    dt = datetime(yr, mon_num, day)
                    if dt.date() >= TODAY.date():
                        year = yr
                        break
                except Exception:
                    pass
            if year is None:
                # All inferred dates are past
                return False, (
                    f"⚠️ **{day} {mon_label}** has already passed. "
                    f"Please provide a future date. 📅"
                )

        # Validate day against actual month length
        max_days = calendar.monthrange(year, mon_num)[1]
        if day > max_days:
            return False, (
                f"⚠️ **{day} {mon_label} {year}** is not valid — "
                f"{mon_label} {year} only has {max_days} days. "
                f"Did you mean **{max_days} {mon_label} {year}**?"
            )

        # Check if past
        try:
            dt = datetime(year, mon_num, day)
            if dt.date() < TODAY.date():
                return False, (
                    f"⚠️ **{day} {mon_label} {year}** has already passed. "
                    f"Today is {TODAY.strftime('%-d %b %Y')}. Please provide a future date. 📅"
                )
        except Exception:
            return False, f"⚠️ **{day_s} {mon_label}** is not a valid date."

    return True, None


def _build_system() -> str:
    today = TODAY.strftime("%d %b %Y")
    return f"""You are a friendly AI travel assistant. CURRENT DATE is {today}.

You MUST always respond with ONLY a JSON object — never plain text, never explanation.

═══════════════════════════════════════════════════════
TOOLS
═══════════════════════════════════════════════════════

{{"tool":"chat","message":"..."}}
  → For ALL questions, clarifications, confirmations, and conversational replies.
  → message must be warm, natural, 1–2 sentences. Like texting a friend.

{{"tool":"search_flights","source":"...","destination":"...","departure_date":"...","return_date":""}}
  → Search for flights. Set return_date="" unless user explicitly gave one.

{{"tool":"search_hotels","destination":"...","check_in":"...","check_out":"..."}}
  → Search for hotels.

{{"tool":"build_itinerary","source":"...","destination":"...","departure_date":"...","return_date":"...","days":0}}
  → Build a full trip plan with flights, hotels, and day-by-day itinerary.

═══════════════════════════════════════════════════════
STRICT CONVERSATION WORKFLOW
═══════════════════════════════════════════════════════

Follow these steps IN ORDER. Never skip. Never combine steps.

STEP 1 — Need source + destination
  If missing → {{"tool":"chat","message":"Where are you flying from and to? 🌍"}}

STEP 2 — Need departure date
  Have source + destination but no departure date →
  {{"tool":"chat","message":"When are you planning to depart? 📅"}}

STEP 3 — Need return date or days
  Have source + destination + departure but no return →
  {{"tool":"chat","message":"What's your return date? Or how many days are you staying? 🗓️"}}

STEP 4 — All 4 fields collected. Ask what they want:
  {{"tool":"chat","message":"Perfect! 🎉 Here's your trip summary:\\n✅ [source] → [destination]\\n📅 [departure] → [return]\\n\\nWhat would you like?\\n✈️ Flights\\n🏨 Hotels\\n📋 Full Itinerary\\n\\n(You can pick one, two, or all three!)"}}

STEP 5 — Call the right tool(s) based on user choice.

═══════════════════════════════════════════════════════
DATE RULES (for LLM)
═══════════════════════════════════════════════════════

1. Today is {today}. Any date before today is a PAST DATE — reject it.
2. If user gives only day + month (e.g. "20 Jul"), assume the nearest future occurrence. Do NOT ask for year.
3. If user gives "N days", compute return_date = departure_date + N days yourself.
4. Always store dates as "D Mon YYYY" e.g. "20 Jul 2026".

═══════════════════════════════════════════════════════
TOOL CALLING RULES
═══════════════════════════════════════════════════════

- User says "flights" → search_flights only
- User says "hotels" → search_hotels only
- User says "itinerary" or "plan" → build_itinerary only
- User says "flights and hotels" → search_flights JSON on line 1, search_hotels JSON on line 2
- User says "flights and itinerary" → search_flights on line 1, build_itinerary on line 2
- User says "all" or "everything" → all 3 tools, one per line
- User asks "show me flights from X to Y on DATE" → call search_flights with that date, return_date=""

═══════════════════════════════════════════════════════
ABSOLUTE RULES
═══════════════════════════════════════════════════════

1. NEVER output plain text. Every single response must be a JSON object.
2. NEVER skip STEP 2 or STEP 3 — always ask for missing fields one at a time.
3. NEVER add return_date to search_flights unless user explicitly gave one.
4. NEVER call build_itinerary without all 4 fields confirmed.
5. NEVER call any tool before completing STEP 4 (unless user directly asked for flights/hotels with enough info).
6. Multiple tools = one JSON per line, nothing else between them.
7. Dates always in "D Mon YYYY" format.
8. chat messages: short, warm, friendly — 1–2 sentences max.
"""


def _stream_generate(prompt: str):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": True},
        stream=True, timeout=300,
    )
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            token = json.loads(line).get("response", "")
            if token:
                yield token
        except Exception:
            continue


def _stream_chat(messages: list):
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": True},
        stream=True, timeout=300,
    )
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            token = json.loads(line).get("message", {}).get("content", "")
            if token:
                yield token
        except Exception:
            continue


def _llm_decide(messages: list) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def _extract_all_tools(text: str) -> list:
    text = re.sub(r"```(?:json)?|```", "", text).strip()
    try:
        d = json.loads(text)
        if isinstance(d, dict) and "tool" in d:
            return [d]
    except Exception:
        pass
    results = []
    for m in re.finditer(r'\{[^{}]+\}', text, re.DOTALL):
        try:
            d = json.loads(m.group())
            if isinstance(d, dict) and "tool" in d:
                results.append(d)
        except Exception:
            pass
    if results:
        return results
    fixed = re.sub(r"'", '"', text)
    fixed = re.sub(r',\s*([}\]])', r'\1', fixed)
    try:
        d = json.loads(fixed)
        if isinstance(d, dict) and "tool" in d:
            return [d]
    except Exception:
        pass
    return []


def _force_retry(messages: list, original: str) -> list:
    retry = messages + [
        {"role": "assistant", "content": original},
        {"role": "user", "content":
            "REMINDER: You must respond with ONLY a JSON object. "
            "Wrap your previous reply as: "
            '{"tool":"chat","message":"<your reply here>"} '
            "Output only the JSON, nothing else."
        }
    ]
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": retry, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return _extract_all_tools(r.json()["message"]["content"].strip())


def _build_messages(history_rows, new_message: str) -> list:
    msgs = [{"role": "system", "content": _build_system()}]
    for row in history_rows:
        role = "assistant" if row.role == "assistant" else "user"
        content = row.message
        if role == "assistant" and len(content) > 600:
            content = "[Full travel response shown to user]"
        msgs.append({"role": role, "content": content})
    msgs.append({"role": "user", "content": new_message})
    return msgs


def _days_between(dep: str, ret: str) -> int:
    for fmt in ["%d %b %Y", "%d %B %Y", "%d %b", "%d %B"]:
        try:
            return max(
                (datetime.strptime(ret.strip(), fmt) - datetime.strptime(dep.strip(), fmt)).days, 1
            )
        except Exception:
            pass
    return 3


def _add_days(dep: str, days: int) -> str:
    for fmt in ["%d %b %Y", "%d %b"]:
        try:
            return (datetime.strptime(dep.strip(), fmt) + timedelta(days=days)).strftime("%-d %b %Y")
        except Exception:
            pass
    return ""


def _stream_text(text: str):
    for ch in text:
        yield ch


def _run_tool(tool_call: dict, all_messages: list):
    tool = tool_call.get("tool")

    # ── chat ──────────────────────────────────────────────────────────────────
    if tool == "chat":
        yield from _stream_text(tool_call.get("message", ""))
        return

    # ── search_flights ────────────────────────────────────────────────────────
    if tool == "search_flights":
        src  = tool_call.get("source", "")
        dst  = tool_call.get("destination", "")
        dep  = tool_call.get("departure_date", "")
        ret  = tool_call.get("return_date") or ""
        days = tool_call.get("days")
        if days and dep and not ret:
            ret = _add_days(dep, int(days))

        yield from _stream_text(
            f"Searching flights from **{src}** to **{dst}** on {dep}... ✈️\n\n"
        )

        try:
            raw = search_flight(src, dst, dep, ret)
        except Exception as e:
            yield f"Sorry, couldn't fetch flights: {e}"
            return

        yield from _stream_generate(f"""You are a friendly travel assistant. Present these flight results in warm, clear Markdown. Stream naturally like a human typing.

Route: {src} → {dst}
{f"Departure: {dep} | Return: {ret}" if ret else f"Departure: {dep} (one-way — show departure flights only, no return section)"}

Raw flight data:
{raw}

## 🛫 Departure Flights ({dep})
✈️ **Airline · Flight No** | `HH:MM → HH:MM` | ⏱ Duration | 💰 ₹Price

{"## 🛬 Return Flights (" + ret + ")" if ret else ""}

End with:
⭐ **Best Pick:** [Airline · reason in one sentence]

Be warm and conversational.
""")
        return

    # ── search_hotels ─────────────────────────────────────────────────────────
    if tool == "search_hotels":
        dst       = tool_call.get("destination", "")
        check_in  = tool_call.get("check_in", "")
        check_out = tool_call.get("check_out", "")
        nights    = _days_between(check_in, check_out)

        yield from _stream_text(
            f"Searching hotels in **{dst}** ({check_in} → {check_out})... 🏨\n\n"
        )

        try:
            raw = search_hotel(dst, check_in, check_out)
        except Exception as e:
            yield f"Sorry, couldn't fetch hotels: {e}"
            return

        yield from _stream_generate(f"""You are a friendly travel assistant. Present these hotel options in warm, clear Markdown. Stream naturally.

Destination: {dst} | {check_in} – {check_out} | {nights} nights

Raw hotel data:
{raw}

### 💚 Budget
### 🌟 Mid-Range
### 👑 Luxury

Each hotel:
🏨 **Hotel Name** ⭐Rating | ₹X,XXX/night | ₹X,XXX total ({nights} nights) | 📌 Best feature

End with:
⭐ **Top Pick:** [Hotel name · reason in one sentence]

Be warm and conversational.
""")
        return

    # ── build_itinerary ───────────────────────────────────────────────────────
    if tool == "build_itinerary":
        src  = tool_call.get("source", "")
        dst  = tool_call.get("destination", "")
        dep  = tool_call.get("departure_date", "")
        ret  = tool_call.get("return_date", "")
        days = tool_call.get("days")

        if days and dep and not ret:
            ret = _add_days(dep, int(days))
        if not days:
            days = _days_between(dep, ret)
        try:
            days = int(days)
        except Exception:
            days = 3

        yield from _stream_text(
            f"Let's build your **{days}-day trip** from **{src}** to **{dst}** "
            f"({dep} → {ret})! 🎉 Fetching flights and hotels first...\n\n"
        )

        try:
            flights = search_flight(src, dst, dep, ret)
        except Exception as e:
            flights = f"(Flights unavailable: {e})"
        try:
            hotels = search_hotel(dst, dep, ret)
        except Exception as e:
            hotels = f"(Hotels unavailable: {e})"

        yield from build_itnerary(
            {"source": src, "destination": dst,
             "departure_date": dep, "return_date": ret, "days": days},
            flights, hotels,
        )
        return


def travel_agent(chat_id: str, message: str, db):
    history = get_chat_history(db=db, chat_id=chat_id)

    # ── DATE VALIDATION (Python-side, before LLM sees anything) ───────────────
    valid, error_msg = _validate_dates_in_message(message)
    if not valid:
        yield from _stream_text(error_msg)
        return

    messages = _build_messages(history, message)

    print(f"\n[AGENT] chat={chat_id} history={len(history)}")

    try:
        decision = _llm_decide(messages)
    except Exception as e:
        yield f"Sorry, I can't reach the AI model right now. ({e})"
        return

    print(f"[AGENT] Decision → {decision[:300]}")

    tool_calls = _extract_all_tools(decision)

    if not tool_calls:
        print("[AGENT] Parse failed — retrying")
        tool_calls = _force_retry(messages, decision)

    if not tool_calls:
        print("[AGENT] Retry failed — streaming plain reply")
        try:
            for token in _stream_chat(messages):
                yield token
        except Exception:
            yield decision
        return

    print(f"[AGENT] Tools → {[t.get('tool') for t in tool_calls]}")

    for i, tool_call in enumerate(tool_calls):
        if i > 0:
            yield "\n\n---\n\n"
        yield from _run_tool(tool_call, messages)