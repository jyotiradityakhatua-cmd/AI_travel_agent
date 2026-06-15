

# import streamlit as st
# import requests
# import uuid

# API_URL = "http://localhost:8000/chat"

# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="wide"
# )


# if "chat_id" not in st.session_state:
#     st.session_state.chat_id = str(uuid.uuid4())

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# st.title(" AI Travel Planner")
# st.markdown(
#     "Plan trips, find flights, hotels, and generate itineraries."
# )


# with st.sidebar:

#     st.header("Session")

#     st.text_input(
#         "Chat ID",
#         value=st.session_state.chat_id,
#         disabled=True
#     )

#     if st.button(" New Chat"):
#         st.session_state.chat_id = str(uuid.uuid4())
#         st.session_state.messages = []
#         st.rerun()


# for msg in st.session_state.messages:

#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])


# prompt = st.chat_input(
#     "Where would you like to travel?"
# )

# if prompt:

#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": prompt
#         }
#     )

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     try:

#         response = requests.post(
#             API_URL,
#             params={
#                 "chat_id": st.session_state.chat_id,
#                 "message": prompt
#             },
#             timeout=360
#         )

#         data = response.json()

#         bot_response = data.get(
#             "response",
#             "No response received."
#         )

#     except Exception as e:

#         bot_response = f" Error: {str(e)}"

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": bot_response
#         }
#     )

#     with st.chat_message("assistant"):
#         st.markdown(bot_response)
# 

# import uuid
# import requests
# import streamlit as st

# # ==========================================
# # CONFIGURATION
# # ==========================================

# API_URL = "http://localhost:8000"

# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="wide"
# )

# # ==========================================
# # SESSION STATE
# # ==========================================

# if "chat_id" not in st.session_state:
#     st.session_state.chat_id = str(uuid.uuid4())

# # ==========================================
# # API FUNCTIONS
# # ==========================================

# def load_chat_history(chat_id):

#     try:
#         response = requests.get(
#             f"{API_URL}/history/{chat_id}",
#             timeout=30
#         )

#         if response.status_code == 200:
#             return response.json()

#     except Exception as e:
#         st.sidebar.error(f"History Error: {e}")

#     return []


# def send_message(chat_id, message):

#     try:
#         response = requests.post(
#             f"{API_URL}/chat",
#             params={
#                 "chat_id": chat_id,
#                 "message": message
#             },
#             timeout=300
#         )

#         if response.status_code == 200:
#             return response.json()

#         return {
#             "response": f"Server Error ({response.status_code})"
#         }

#     except Exception as e:
#         return {
#             "response": f"Error: {str(e)}"
#         }


# def load_user_chats(user_id):

#     try:
#         response = requests.get(
#             f"{API_URL}/users/{user_id}/chats",
#             timeout=30
#         )

#         if response.status_code == 200:
#             return response.json()

#     except Exception as e:
#         st.sidebar.error(
#             f"Chat Load Error: {e}"
#         )

#     return []

# # ==========================================
# # LOAD DATA
# # ==========================================

# messages = load_chat_history(
#     st.session_state.chat_id
# )

# # ==========================================
# # SIDEBAR
# # ==========================================

# with st.sidebar:

#     st.title("✈️ Travel Agent")

#     st.subheader("Current Chat")

#     st.code(
#         st.session_state.chat_id,
#         language=None
#     )

#     if st.button(
#         "➕ New Chat",
#         use_container_width=True
#     ):
#         st.session_state.chat_id = str(uuid.uuid4())
#         st.rerun()

#     st.divider()

#     st.subheader("Recent Messages")

#     if messages:

#         for msg in messages[-10:]:

#             icon = (
#                 "🧑"
#                 if msg["role"] == "user"
#                 else "🤖"
#             )

#             preview = msg["message"][:50]

#             st.caption(
#                 f"{icon} {preview}..."
#             )

#     else:
#         st.caption("No chat history found.")

# # ==========================================
# # MAIN PAGE
# # ==========================================

# st.title("✈️ AI Travel Planner")

# st.markdown(
#     """
#     Plan trips, discover flights and hotels,
#     and generate personalized travel itineraries.
#     """
# )

# # ==========================================
# # DISPLAY CHAT HISTORY
# # ==========================================

# for msg in messages:

#     with st.chat_message(msg["role"]):
#         st.markdown(msg["message"])

# # ==========================================
# # CHAT INPUT
# # ==========================================

# prompt = st.chat_input(
#     "Where would you like to travel?"
# )

# if prompt:

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.spinner(
#         "Planning your trip..."
#     ):

#         result = send_message(
#             st.session_state.chat_id,
#             prompt
#         )

#         response_text = result.get(
#             "response",
#             "No response received."
#         )

#     with st.chat_message("assistant"):
#         st.markdown(response_text)

#     st.rerun()

# import uuid
# import requests
# import streamlit as st

# API_URL = "http://localhost:8000"

# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="wide"
# )



# if "user_id" not in st.session_state:
#     st.session_state.user_id = None

# if "username" not in st.session_state:
#     st.session_state.username = None

# if "chat_id" not in st.session_state:
#     st.session_state.chat_id = None



# def login(username, password):

#     response = requests.post(
#         f"{API_URL}/login",
#         params={
#             "username": username,
#             "password": password
#         }
#     )

#     return response


# def load_user_chats(user_id):

#     try:

#         response = requests.get(
#             f"{API_URL}/users/{user_id}/chats"
#         )

#         if response.status_code == 200:
#             return response.json()

#     except Exception:
#         pass

#     return []


# def load_chat_history(chat_id):

#     try:

#         response = requests.get(
#             f"{API_URL}/history/{chat_id}"
#         )

#         if response.status_code == 200:
#             return response.json()

#     except Exception:
#         pass

#     return []


# def send_message(chat_id, user_id, message):

#     response = requests.post(
#         f"{API_URL}/chat",
#         params={
#             "user_id": user_id,
#             "chat_id": chat_id,
#             "message": message
#         }
#     )

#     return response.json()



# if not st.session_state.user_id:

#     st.title("Travel Planner Login")

#     username = st.text_input("Username")

#     password = st.text_input(
#         "Password",
#         type="password"
#     )

#     if st.button("Login"):

#         response = login(
#             username,
#             password
#         )

#         if response.status_code == 200:

#             data = response.json()

#             st.session_state.user_id = data["user_id"]
#             st.session_state.username = data["username"]

#             st.rerun()

#         else:
#             st.error("Invalid credentials")

#     st.stop()



# with st.sidebar:

#     st.title("✈️ Travel Planner")

#     st.write(
#         f"Welcome {st.session_state.username}"
#     )

#     if st.button("Logout"):

#         st.session_state.clear()
#         st.rerun()

#     st.divider()

#     st.subheader("Chats")

#     chats = load_user_chats(
#         st.session_state.user_id
#     )

#     for chat in chats:

#         if st.button(
#             chat["title"],
#             key=chat["chat_id"]
#         ):

#             st.session_state.chat_id = chat["chat_id"]
#             st.rerun()



# st.title("AI Travel Planner")

# if not st.session_state.chat_id:

#     st.info(
#         "Start a conversation by sending a message."
#     )

#     st.session_state.chat_id = str(uuid.uuid4())



# messages = load_chat_history(
#     st.session_state.chat_id
# )

# for msg in messages:

#     with st.chat_message(
#         msg["role"]
#     ):
#         st.markdown(
#             msg["message"]
#         )



# prompt = st.chat_input(
#     "Where would you like to travel?"
# )

# if prompt:

#     result = send_message(
#         st.session_state.chat_id,
#         st.session_state.user_id,
#         prompt
#     )

#     if "chat_id" in result:
#         st.session_state.chat_id = result["chat_id"]

#     st.rerun()

# import uuid
# import requests
# import streamlit as st

# API_URL = "http://localhost:8000"

# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="wide"
# )

# # =========================
# # SESSION STATE
# # =========================
# if "user_id" not in st.session_state:
#     st.session_state.user_id = None

# if "username" not in st.session_state:
#     st.session_state.username = None

# if "chat_id" not in st.session_state:
#     st.session_state.chat_id = None

# if "auth_mode" not in st.session_state:
#     st.session_state.auth_mode = "login"   # login | register


# # =========================
# # API CALLS
# # =========================
# def login(username, password):
#     return requests.post(
#         f"{API_URL}/login",
#         params={"username": username, "password": password}
#     )


# def register(username, password):
#     return requests.post(
#         f"{API_URL}/register",
#         params={"username": username, "password": password}
#     )


# def load_user_chats(user_id):
#     try:
#         res = requests.get(f"{API_URL}/users/{user_id}/chats")
#         if res.status_code == 200:
#             return res.json()
#     except:
#         pass
#     return []


# def load_chat_history(chat_id):
#     try:
#         res = requests.get(f"{API_URL}/history/{chat_id}")
#         if res.status_code == 200:
#             return res.json()
#     except:
#         pass
#     return []


# def send_message(chat_id, user_id, message):
#     res = requests.post(
#         f"{API_URL}/chat",
#         params={
#             "user_id": user_id,
#             "chat_id": chat_id,
#             "message": message
#         }
#     )
#     return res.json()


# # =========================
# # AUTH UI (LOGIN / REGISTER)
# # =========================
# if not st.session_state.user_id:

#     st.title("✈️ Travel Planner Authentication")

#     tab1, tab2 = st.tabs(["Login", "Register"])

#     # ================= LOGIN =================
#     with tab1:
#         username = st.text_input("Username", key="login_user")
#         password = st.text_input("Password", type="password", key="login_pass")

#         if st.button("Login"):
#             res = login(username, password)

#             if res.status_code == 200:
#                 data = res.json()
#                 st.session_state.user_id = data["user_id"]
#                 st.session_state.username = data["username"]
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials")

#     # ================= REGISTER =================
#     with tab2:
#         new_username = st.text_input("New Username", key="reg_user")
#         new_password = st.text_input("New Password", type="password", key="reg_pass")

#         if st.button("Register"):
#             res = register(new_username, new_password)

#             if res.status_code == 200:
#                 st.success("Registration successful! Please login.")
#             else:
#                 st.error("Registration failed (user may already exist)")

#     st.stop()


# # =========================
# # SIDEBAR
# # =========================
# with st.sidebar:

#     st.title("✈️ Travel Planner")

#     st.write(f"Welcome {st.session_state.username}")

#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()

#     st.divider()

#     st.subheader("Chats")

#     chats = load_user_chats(st.session_state.user_id)

#     for chat in chats:
#         if st.button(chat["title"], key=chat["chat_id"]):
#             st.session_state.chat_id = chat["chat_id"]
#             st.rerun()


# # =========================
# # MAIN PAGE
# # =========================
# st.title("AI Travel Planner")

# if not st.session_state.chat_id:
#     st.info("Start a conversation by sending a message.")
#     st.session_state.chat_id = str(uuid.uuid4())


# messages = load_chat_history(st.session_state.chat_id)

# for msg in messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["message"])


# prompt = st.chat_input("Where would you like to travel?")

# if prompt:
#     result = send_message(
#         st.session_state.chat_id,
#         st.session_state.user_id,
#         prompt
#     )

#     if "chat_id" in result:
#         st.session_state.chat_id = result["chat_id"]

#     st.rerun()

# import uuid
# import requests
# import streamlit as st
# import time

# API_URL = "http://localhost:8000"

# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="wide"
# )

# def init_session():
#     defaults = {
#         "user_id": None,
#         "username": None,
#         "chat_id": None
#     }
#     for k, v in defaults.items():
#         st.session_state.setdefault(k, v)

# init_session()



# def stream_chat(chat_id, user_id, message):

#     response = requests.post(
#         f"{API_URL}/chat",
#         params={
#             "user_id": user_id,
#             "chat_id": chat_id,
#             "message": message
#         },
#         stream=True,
#         timeout=200
#     )

 
#     for line in response.iter_lines(decode_unicode=True):

#         if line:
#             yield line + "\n"



# def login(username, password):
#     return requests.post(
#         f"{API_URL}/login",
#         params={"username": username, "password": password}
#     )


# def register(username, password):
#     return requests.post(
#         f"{API_URL}/register",
#         params={"username": username, "password": password}
#     )


# def load_history(chat_id):
#     try:
#         res = requests.get(f"{API_URL}/history/{chat_id}")
#         return res.json() if res.status_code == 200 else []
#     except:
#         return []


# def load_chats(user_id):
#     try:
#         res = requests.get(f"{API_URL}/users/{user_id}/chats")
#         return res.json() if res.status_code == 200 else []
#     except:
#         return []


# def create_new_chat(user_id):
#     try:
#         res = requests.post(
#             f"{API_URL}/chat/new",
#             params={"user_id": user_id}
#         )
#         if res.status_code == 200:
#             return res.json()
#     except:
#         pass

#     return {"chat_id": str(uuid.uuid4())}


# def auth_page():
#     st.title("✈️ AI Travel Planner")

#     tab1, tab2 = st.tabs(["Login", "Register"])

#     with tab1:
#         u = st.text_input("Username")
#         p = st.text_input("Password", type="password")

#         if st.button("Login"):
#             res = login(u, p)
#             if res.status_code == 200:
#                 data = res.json()
#                 st.session_state.user_id = data["user_id"]
#                 st.session_state.username = data["username"]
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials")

#     with tab2:
#         u = st.text_input("New Username")
#         p = st.text_input("New Password", type="password")

#         if st.button("Register"):
#             res = register(u, p)
#             if res.status_code == 200:
#                 st.success("Registered successfully")
#             else:
#                 st.error("User already exists")

#     st.stop()

# def sidebar():
#     with st.sidebar:
#         st.title("✈️ Travel Planner")

#         st.write(f"Welcome **{st.session_state.username}**")

#         if st.button("Logout"):
#             st.session_state.clear()
#             st.rerun()

#         st.divider()


#         if st.button("➕ New Chat", use_container_width=True):
#             chat = create_new_chat(st.session_state.user_id)
#             st.session_state.chat_id = chat["chat_id"]
#             st.rerun()

#         st.divider()

#         st.subheader("Your Chats")

#         chats = load_chats(st.session_state.user_id)

#         for c in chats:
#             if st.button(c["title"], key=c["chat_id"]):
#                 st.session_state.chat_id = c["chat_id"]
#                 st.rerun()


# def chat_ui():
#     st.title("AI Travel Planner")

#     if not st.session_state.chat_id:
#         st.session_state.chat_id = str(uuid.uuid4())


#     messages = load_history(st.session_state.chat_id)

#     for msg in messages:
#         with st.chat_message(msg.get("role", "assistant")):
#             st.markdown(msg.get("message", ""))


#     if prompt := st.chat_input("Where would you like to travel?"):


#         with st.chat_message("user"):
#             st.markdown(prompt)

        
#         with st.chat_message("assistant"):
#             placeholder = st.empty()
#             full_response = ""

#             # for chunk in stream_chat(
#             #     st.session_state.chat_id,
#             #     st.session_state.user_id,
#             #     prompt
#             # ):
#             #     full_response += chunk
#             #     placeholder.markdown(full_response)
#             for chunk in stream_chat(
#     st.session_state.chat_id,
#     st.session_state.user_id,
#     prompt
#             ):
#              full_response += chunk
#              placeholder.markdown(full_response)

#              time.sleep(0.05)

#              st.rerun()


# if not st.session_state.user_id:
#     auth_page()
# else:
#     sidebar()
#     chat_ui()

import uuid
import time
import random
import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)


def init_session():
    defaults = {
        "user_id": None,
        "username": None,
        "chat_id": None
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

init_session()



def login(username, password):
    return requests.post(
        f"{API_URL}/login",
        params={"username": username, "password": password}
    )


def register(username, password):
    return requests.post(
        f"{API_URL}/register",
        params={"username": username, "password": password}
    )


def load_chats(user_id):
    try:
        r = requests.get(f"{API_URL}/users/{user_id}/chats")
        return r.json() if r.status_code == 200 else []
    except:
        return []


def load_history(chat_id):
    try:
        r = requests.get(f"{API_URL}/history/{chat_id}")
        return r.json() if r.status_code == 200 else []
    except:
        return []


def create_new_chat(user_id):
    try:
        r = requests.post(
            f"{API_URL}/chat/new",
            params={"user_id": user_id}
        )
        if r.status_code == 200:
            return r.json()
    except:
        pass

    return {"chat_id": str(uuid.uuid4())}


def stream_chat(chat_id, user_id, message):
    try:
        r = requests.post(
            f"{API_URL}/chat",
            params={
                "user_id": user_id,
                "chat_id": chat_id,
                "message": message
            },
            stream=True,
            timeout=300
        )

        for chunk in r.iter_content(chunk_size=8):
            if chunk:
                yield chunk.decode("utf-8", errors="ignore")

    except Exception as e:
        yield f"\nError: {str(e)}"



def auth_page():
    st.title("✈️ Travel Planner")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            res = login(u, p)
            if res.status_code == 200:
                data = res.json()
                st.session_state.user_id = data["user_id"]
                st.session_state.username = data["username"]
                st.session_state.chat_id = None
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")

        if st.button("Register"):
            res = register(u, p)
            if res.status_code == 200:
                st.success("Registered successfully")
            else:
                st.error("User already exists")

    st.stop()



def sidebar():
    with st.sidebar:
        st.title("✈️ Travel Planner")

        st.write(f"Welcome **{st.session_state.username}**")

        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

        st.divider()


        if st.button("➕ New Chat", use_container_width=True):
            chat = create_new_chat(st.session_state.user_id)
            st.session_state.chat_id = chat["chat_id"]
            st.rerun()

        st.divider()

        st.subheader("Your Chats")

        chats = load_chats(st.session_state.user_id)

        for c in chats:
            if st.button(c["title"], key=c["chat_id"]):
                st.session_state.chat_id = c["chat_id"]
                st.rerun()



def chat_ui():
    st.title("AI Travel Planner")

    
    if not st.session_state.chat_id:
        st.session_state.chat_id = create_new_chat(
            st.session_state.user_id
        )["chat_id"]

    messages = load_history(st.session_state.chat_id)

    for msg in messages:
        with st.chat_message(msg.get("role", "assistant")):
            st.markdown(msg.get("message", ""))

    if prompt := st.chat_input("Where would you like to travel?"):

  
        with st.chat_message("user"):
            st.markdown(prompt)

   
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            for chunk in stream_chat(
                st.session_state.chat_id,
                st.session_state.user_id,
                prompt
            ):
                for char in chunk:
                    full_response += char
                    placeholder.markdown(full_response)

          
                    if char in ".!?":
                        time.sleep(0.15)
                    elif char == ",":
                        time.sleep(0.06)
                    else:
                        time.sleep(random.uniform(0.005, 0.02))



if not st.session_state.user_id:
    auth_page()
else:
    sidebar()
    chat_ui()