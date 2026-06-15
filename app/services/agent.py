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














import json
import re
import requests
from datetime import datetime, timedelta

from app.db.chat_repo import get_chat_history
from app.tools.search_flight import search_flight
from app.tools.search_hotel import search_hotel
from app.tools.build_itnerary import build_itnerary

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"


def _build_system() -> str:
    today = datetime.now().strftime("%d %b %Y")
    return f"""You are a friendly AI travel assistant. Today is {today}.

You have exactly 3 tools. You MUST output ONLY a JSON object — no text before or after it, ever.

═══════════════════════════════════════════════
TOOL 1 — search_flights
Use when: user asks about flights, wants to see flight options
Required: source, destination, departure_date
Optional: return_date (only include if user explicitly gave a return date)
Output: {{"tool":"search_flights","source":"...","destination":"...","departure_date":"...","return_date":"..."}}

TOOL 2 — search_hotels
Use when: user asks about hotels, accommodation, where to stay
Required: destination, check_in, check_out
Output: {{"tool":"search_hotels","destination":"...","check_in":"...","check_out":"..."}}

TOOL 3 — build_itinerary
Use when: user asks for a trip plan, itinerary, travel plan
Required: source, destination, departure_date, return_date, days
Output: {{"tool":"build_itinerary","source":"...","destination":"...","departure_date":"...","return_date":"...","days":<number>}}

TOOL 4 — chat
Use when: info is missing OR you need to ask something OR user is just chatting
Output: {{"tool":"chat","message":"<your natural conversational reply here>"}}
═══════════════════════════════════════════════

CONVERSATION FLOW — follow this strictly:

STEP 1: If user gives source + destination but no dates → ask departure date only.
STEP 2: After getting departure date → ask "What's your return date? Or how many days are you staying?"
STEP 3: After getting return date/days → ask "Got it! Would you like to see flights, hotels, or a full itinerary?"
STEP 4: Call the tool the user chooses.

SPECIAL CASES:
- If user asks for BOTH flights and hotels → output TWO JSON objects, one per line.
- If user asks for itinerary → call build_itinerary (it includes flights + hotels internally).
- If user asks for flights on a specific date → call search_flights with ONLY that date as departure_date. Do NOT add return_date unless user gave one.
- If user gives ALL info (source, destination, departure, return) upfront → go to STEP 3 immediately.
- If user says "N days" → compute return_date = departure_date + N days yourself before calling the tool.

STRICT RULES:
- Output ONLY JSON. Never output plain text outside a JSON object.
- Use chat tool for ALL conversational replies, questions, and clarifications.
- Never call search_flights with a return_date the user did not provide.
- Never call build_itinerary unless you have source, destination, departure_date AND return_date.
- Dates format: "D Mon YYYY" e.g. "15 Jun 2025".
- chat tool messages should be warm, short, human — like texting a knowledgeable friend.
"""


def _stream_generate(prompt: str):
    """Stream tokens from /api/generate."""
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


def _stream_chat(messages: list):
    """Stream tokens from /api/chat."""
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": True},
        stream=True,
        timeout=300,
    )
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue
        try:
            chunk = json.loads(line)
            token = chunk.get("message", {}).get("content", "")
            if token:
                yield token
        except Exception:
            continue


def _llm_decide(messages: list) -> str:
    """Non-streaming call to get tool decision JSON."""
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def _extract_all_tools(text: str) -> list[dict]:
    """Extract one or more tool JSON objects from LLM output."""
    text = re.sub(r"```(?:json)?|```", "", text).strip()
    results = []
    # Try whole text as single JSON
    try:
        d = json.loads(text)
        if "tool" in d:
            return [d]
    except Exception:
        pass
    # Find all JSON objects
    for m in re.finditer(r'\{[^{}]*"tool"\s*:\s*"[^"]*"[^{}]*\}', text, re.DOTALL):
        try:
            d = json.loads(m.group())
            if "tool" in d:
                results.append(d)
        except Exception:
            pass
    return results


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
            return max((datetime.strptime(ret.strip(), fmt) - datetime.strptime(dep.strip(), fmt)).days, 1)
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
    """Stream text character by character for human-like feel."""
    for ch in text:
        yield ch


def _run_tool(tool_call: dict, all_messages: list):
    """Execute a single tool and stream its output."""
    tool = tool_call.get("tool")

    # ── chat (conversational reply) ───────────────────────────────────────────
    if tool == "chat":
        msg = tool_call.get("message", "")
        yield from _stream_text(msg)
        return

    # ── search_flights ────────────────────────────────────────────────────────
    if tool == "search_flights":
        src = tool_call.get("source", "")
        dst = tool_call.get("destination", "")
        dep = tool_call.get("departure_date", "")
        ret = tool_call.get("return_date") or ""
        days = tool_call.get("days")
        if days and dep and not ret:
            ret = _add_days(dep, int(days))

        header = f"Searching flights from **{src}** to **{dst}** on {dep}... ✈️\n\n"
        yield from _stream_text(header)

        try:
            raw = search_flight(src, dst, dep, ret)
        except Exception as e:
            yield f"Sorry, couldn't fetch flights: {e}"
            return

        prompt = f"""You are a friendly travel assistant. Present these flight options in warm, clear Markdown.

Route: {src} → {dst}
Date: {dep}{(" | Return: " + ret) if ret else " (one-way)"}

Raw flight data:
{raw}

Format each flight as:
✈️ **Airline · Flight No** | `HH:MM → HH:MM` | ⏱ Duration | 💰 ₹Price

Separate departure and return flights with a clear heading if return flights exist.
At the end, highlight your best value pick with a short reason.
Be warm and conversational — like texting a knowledgeable friend.
"""
        yield from _stream_generate(prompt)
        return

    # ── search_hotels ─────────────────────────────────────────────────────────
    if tool == "search_hotels":
        dst      = tool_call.get("destination", "")
        check_in = tool_call.get("check_in", "")
        check_out= tool_call.get("check_out", "")
        nights   = _days_between(check_in, check_out)

        header = f"Searching hotels in **{dst}** ({check_in} → {check_out})... 🏨\n\n"
        yield from _stream_text(header)

        try:
            raw = search_hotel(dst, check_in, check_out)
        except Exception as e:
            yield f"Sorry, couldn't fetch hotels: {e}"
            return

        prompt = f"""You are a friendly travel assistant. Present these hotel options in warm, clear Markdown.

Destination: {dst}
Check-in: {check_in} | Check-out: {check_out} | {nights} nights

Raw hotel data:
{raw}

Group hotels as:
### 💚 Budget
### 🌟 Mid-Range  
### 👑 Luxury

For each hotel:
🏨 **Hotel Name** ⭐ Rating | ₹X,XXX/night | ₹X,XXX total | 📌 Standout feature

End with your top pick and a short reason why.
Be warm and conversational — like advising a friend.
"""
        yield from _stream_generate(prompt)
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

        header = f"Planning your **{days}-day trip** from **{src}** to **{dst}** ({dep} → {ret})! Let me search flights and hotels...\n\n"
        yield from _stream_text(header)

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
    messages = _build_messages(history, message)

    print(f"\n[AGENT] chat={chat_id} history={len(history)}")

    try:
        decision = _llm_decide(messages)
    except Exception as e:
        yield f"Sorry, I can't reach the AI model right now. ({e})"
        return

    print(f"[AGENT] Decision → {decision[:300]}")

    tool_calls = _extract_all_tools(decision)

    # No tool found — stream a plain conversational reply
    if not tool_calls:
        print("[AGENT] No tool call — streaming plain reply")
        try:
            for token in _stream_chat(messages):
                yield token
        except Exception:
            yield decision
        return

    print(f"[AGENT] Tools to run: {[t.get('tool') for t in tool_calls]}")

    # Run each tool — supports multiple tools (e.g. flights + hotels together)
    for i, tool_call in enumerate(tool_calls):
        if i > 0:
            yield "\n\n---\n\n"  # separator between multiple tool outputs
        yield from _run_tool(tool_call, messages)
#     itinerary_text = ""

#     for chunk in build_itnerary(state, flights, hotels):
#         itinerary_text += chunk
#         yield chunk   


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