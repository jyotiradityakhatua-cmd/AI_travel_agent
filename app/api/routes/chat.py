
# import uuid

# from fastapi import APIRouter

# from app.schemas.chat_schema import ChatRequest
# from app.agents.travel_agents import process_chat


# router = APIRouter()




# def generate_chat_id():

#     return str(uuid.uuid4())



# @router.post("/")
# async def chat(req: ChatRequest):

#     chat_id = req.chat_id

#     if not chat_id:

#         chat_id = generate_chat_id()



#     response = await process_chat(
#         user_id=req.user_id,
#         chat_id=chat_id,
#         message=req.message
#     )



#     return {
#         "chat_id": chat_id,
#         "response": response
#     }

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.db.database import get_db
# from app.agents.travel_agents import process_chat

# router = APIRouter()


# @router.post("/chat")
# async def chat(
#     message: str,
#     chat_id: str | None = None,
#     db: Session = Depends(get_db)
   
# ):

#     response = await process_chat(
#         user_id="demo_user",   
#         chat_id=chat_id,
#         message=message
#     )

#     return response

# @router.get("/test")
# def test(db: Session = Depends(get_db)):

#     return {
#         "status": "ok"
#     }


# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from typing import Optional

# from app.db.session import get_db
# from app.agents.travel_agents import process_chat

# router = APIRouter()




# class ChatRequest(BaseModel):
#     message: str
#     chat_id: Optional[str] = None




# @router.post("/chat")
# async def chat(
# from fastapi import APIRouter
# from app.memory.chat_store import add, get
# from app.services.agent import travel_agent

# router = APIRouter()


# @router.post("/")
# def chat(message: str, chat_id: str = "default"):

#     add(chat_id, "user", message)

#     response = travel_agent(chat_id, message)

#     add(chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response,
#         "history": get(chat_id)
#     }


# import uuid
# from fastapi import APIRouter
# from app.memory.chat_store import add, get
# from app.services.agent import travel_agent

# router = APIRouter()


# @router.post("/")
# def chat(message: str, chat_id: str | None = None):


#     if not chat_id:
#         chat_id = str(uuid.uuid4())

#     add(chat_id, "user", message)

#     response = travel_agent(chat_id, message)

#     add(chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response,
#         "history": get(chat_id)
#     }



# from app.memory.chat_store import add, get
# from app.services.agent import travel_agent





# @router.post("/")
# def chat(message: str, chat_id: str | None = None):


#     if not chat_id:
#         chat_id = str(uuid.uuid4())


#     add(chat_id, "user", message)


#     history = get(chat_id)

#     response = travel_agent(chat_id, message, history)


#     add(chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response,
#         "history": get(chat_id)
#     }
from uuid import uuid4
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.chat_repo import save_message
from app.memory.chat_store import get as get_memory, add as add_memory
from app.services.agent import travel_agent
from app.db.chat_repo import get_chat_history
from app.db.chat_repo import  get_all_chat_ids
from app.db.models.chat_session import ChatSession
from app.db.models.user import User
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import uuid
from app.services.llm_service import run_chat_llm
# @router.post("/")
# def chat(message: str, chat_id: str | None = None, db: Session = Depends(get_db)):

#     if not chat_id:
#         chat_id = str(uuid.uuid4())


#     add_memory(chat_id, "user", message)


#     save_message(db, chat_id, "user", message)

#     history = get_memory(chat_id)

#     response = travel_agent(chat_id, message, history)


#     add_memory(chat_id, "assistant", response)


#     save_message(db, chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response
#     }

# @router.post("/")
# def chat(message: str, chat_id: str | None = None, db: Session = Depends(get_db)):

#     if not chat_id:
#         chat_id = str(uuid.uuid4())

   
#     save_message(db, chat_id, "user", message)

#     history = get(chat_id)


#     response = travel_agent(chat_id, message, history)


#     save_message(db, chat_id, "assistant", response)

#     return {
#         "chat_id": chat_id,
#         "response": response,
#         "db":db
#     }






# @router.post("/")
# def chat(
#     message: str,
#     chat_id: str,
#     db: Session = Depends(get_db)
# ):

#     response = travel_agent(
#         chat_id,
#         message,
#         db
#     )

#     return {
#         "chat_id": chat_id,
#         "response": response
#     }




router = APIRouter()




# @router.post("/")
# def chat(
#     message: str,
#     chat_id: str | None = None,
#     db: Session = Depends(get_db)
# ):

#     if not chat_id:
#         chat_id = str(uuid.uuid4())

#     response = travel_agent(chat_id, message, db)

#     return {
#         "chat_id": chat_id,
#         "response": response
#     }


# @router.post("/register")
# def register(
#     username: str,
#     password: str,
#     db: Session = Depends(get_db)
# ):

#     existing_user = (
#         db.query(User)
#         .filter(User.username == username)
#         .first()
#     )

#     if existing_user:
#         raise HTTPException(
#             status_code=400,
#             detail="Username already exists"
#         )

#     user = User(
#         username=username,
#         password=password
#     )

#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return {
#         "user_id": user.user_id,
#         "username": user.username
#     }

# @router.post("/login")
# def login(
#     username: str,
#     password: str,
#     db: Session = Depends(get_db)
# ):

#     user = (
#         db.query(User)
#         .filter(User.username == username)
#         .first()
#     )

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )

#     if user.password != password:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid password"
#         )

#     return {
#         "user_id": user.user_id,
#         "username": user.username
#     }







# @router.post("/")
# def chat(
#     message: str,
#     chat_id: str | None = None,
#     db: Session = Depends(get_db)
# ):

#     if not chat_id:
#         chat_id = str(uuid.uuid4())


#     save_message(
#         db=db,
#         chat_id=chat_id,
#         role="user",
#         message=message
#     )


#     response = travel_agent(
#         chat_id=chat_id,
#         message=message,
#         db=db
#     )


#     save_message(
#         db=db,
#         chat_id=chat_id,
#         role="assistant",
#         message=response
#     )

#     return {
#         "chat_id": chat_id,
#         "response": response
#     }


# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.db.session import get_db
# from app.db.chat_repo import save_message
# from app.db.models.chat_session import ChatSession
# from app.services.agent import travel_agent

# router = APIRouter()


# @router.post("/")
# def chat(
#     message: str,
#     user_id: str,
#     chat_id: str | None = None,
#     db: Session = Depends(get_db)
# ):


#     if not chat_id:
#         chat_id = str(uuid4())

   
#     chat_session = (
#         db.query(ChatSession)
#         .filter(ChatSession.chat_id == chat_id)
#         .first()
#     )

#     if not chat_session:

#         chat_session = ChatSession(
#             chat_id=chat_id,
#             user_id=user_id,
#             title=message[:50]
#         )

#         db.add(chat_session)
#         db.commit()


#     save_message(
#         db=db,
#         chat_id=chat_id,
#         role="user",
#         message=message
# #     )


# #     response = travel_agent(
# #         chat_id=chat_id,
# #         message=message,
# #         db=db
# #     )


# #     save_message(
# #         db=db,
# #         chat_id=chat_id,
# #         role="assistant",
# #         message=response
# #     )

# #     return {
# #         "user_id": user_id,
# #         "chat_id": chat_id,
# #         "response": response
# #     }



# # @router.post("/")
# # def chat(
# #     message: str,
# #     user_id: str,
# #     chat_id: str | None = None,
# #     db: Session = Depends(get_db)
# # ):

# #     if not chat_id:
# #         chat_id = str(uuid.uuid4())

# #     chat_session = (
# #         db.query(ChatSession)
# #         .filter(ChatSession.chat_id == chat_id)
# #         .first()
# #     )

# #     if not chat_session:
# #         chat_session = ChatSession(
# #             chat_id=chat_id,
# #             user_id=user_id,
# #             title=message[:50]
# #         )
# #         db.add(chat_session)
# #         db.commit()

# #     save_message(
# #         db=db,
# #         chat_id=chat_id,
# #         role="user",
# #         message=message
# #     )

   
#     # def stream_response():

#     #     full_response = ""

#     #     for chunk in travel_agent_stream(
#     #         chat_id=chat_id,
#     #         message=message,
#     #         db=db
#     #     ):
#     #         full_response += chunk
#     #         yield chunk

#     #     save_message(
#     #         db=db,
#     #         chat_id=chat_id,
#     #         role="assistant",
#     #         message=full_response
#     #     )

#     # return StreamingResponse(
#     #     stream_response(),
#     #     media_type="text/plain"
#     # )


# @router.post("/")
# def chat(
#     message: str,
#     user_id: str,
#     chat_id: str | None = None,
#     db: Session = Depends(get_db)
# ):

#     if not chat_id:
#         chat_id = str(uuid.uuid4())

#     chat_session = (
#         db.query(ChatSession)
#         .filter(ChatSession.chat_id == chat_id)
#         .first()
#     )

#     if not chat_session:
#         chat_session = ChatSession(
#             chat_id=chat_id,
#             user_id=user_id,
#             title=message[:50]
#         )
#         db.add(chat_session)
#         db.commit()

#     save_message(
#         db=db,
#         chat_id=chat_id,
#         role="user",
#         message=message
#     )


#     def stream():
#         full_response = ""

#         for chunk in travel_agent(chat_id, message, db):
#             full_response += chunk
#             yield chunk  
#         # for chunk in travel_agent(chat_id, message, db):
#         #      for word in chunk.split(" "):
#         #          full_response += word + " "
#         # yield word + " "
  
#         save_message(
#             db=db,
#             chat_id=chat_id,
#             role="assistant",
#             message=full_response
#         )

    
#         # yield f"\n[CHAT_ID:{chat_id}]"

#     return StreamingResponse(
#         stream(),
#         media_type="text/plain"
#     )

# @router.get("/history/{chat_id}")
# def history(
#     chat_id: str,
#     db: Session = Depends(get_db)
# ):

#     messages = get_chat_history(
#         db=db,
#         chat_id=chat_id
#     )

#     return [
#         {
#             "id": msg.id,
#             "role": msg.role,
#             "message": msg.message,
#             "created_at": msg.created_at
#         }
#         for msg in messages
#     ]

# @router.get("/chats")
# def get_chats(db: Session = Depends(get_db)):

#     chats = get_all_chat_ids(db)

#     return [
#         {
#             "chat_id": chat[0]
#         }
#         for chat in chats
#     ]


# @router.get("/users/{user_id}/chats")
# def get_user_chats(
#     user_id: str,
#     db: Session = Depends(get_db)
# ):

#     chats = (
#         db.query(ChatSession)
#         .filter(ChatSession.user_id == user_id)
#         .order_by(ChatSession.created_at.desc())
#         .all()
#     )

#     return [
#         {
#             "chat_id": chat.chat_id,
#             "title": chat.title,
#             "created_at": chat.created_at
#         }
#         for chat in chats
#     ]





# ── Auth ──────────────────────────────────────────────────────────────────────

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.user_id, "username": user.username}


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != password:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"user_id": user.user_id, "username": user.username}


# ── Chat ──────────────────────────────────────────────────────────────────────

@router.post("/")
def chat(
    message: str,
    user_id: str,
    chat_id: str | None = None,
    db: Session = Depends(get_db),
):
    is_new = not chat_id
    if is_new:
        chat_id = str(uuid.uuid4())

    # Create session row if needed
    if not db.query(ChatSession).filter(ChatSession.chat_id == chat_id).first():
        db.add(ChatSession(
            chat_id=chat_id,
            user_id=user_id,
            title=message[:50]
        ))
        db.commit()

    # Persist user message before streaming
    save_message(db=db, chat_id=chat_id, role="user", message=message)

    def stream():
        full = ""
        for chunk in travel_agent(chat_id, message, db):
            full += chunk
            yield chunk
        # Persist assistant reply
        save_message(db=db, chat_id=chat_id, role="assistant", message=full)
        # Send chat_id so frontend knows which session this is
        yield f"\n\n<!--CHAT_ID:{chat_id}-->"

    return StreamingResponse(stream(), media_type="text/plain")


# ── History & user chats ──────────────────────────────────────────────────────

@router.get("/history/{chat_id}")
def history(chat_id: str, db: Session = Depends(get_db)):
    msgs = get_chat_history(db=db, chat_id=chat_id)
    return [
        {"id": m.id, "role": m.role, "message": m.message, "created_at": m.created_at}
        for m in msgs
    ]


@router.get("/users/{user_id}/chats")
def get_user_chats(user_id: str, db: Session = Depends(get_db)):
    chats = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )
    return [
        {"chat_id": c.chat_id, "title": c.title, "created_at": c.created_at}
        for c in chats
    ]


@router.post("/chat")
def chat_endpoint(payload: dict):
    ctx = payload["ctx"]
    user_query = payload["message"]

    reply = run_chat_llm(ctx, user_query)

    return {"response": reply}