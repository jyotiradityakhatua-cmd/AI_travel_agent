
from fastapi import APIRouter, Request

from app.services.chat_service import handle_chat

router = APIRouter()


@router.post("/test-chat")
async def test_chat(request: Request):

    body = await request.json()

    user_id = body.get("user_id", "test-user")
    chat_id = body.get("chat_id")
    message = body.get("message", "Hello")

    response = await handle_chat(
        user_id=user_id,
        chat_id=chat_id,
        message=message
    )

    return response

