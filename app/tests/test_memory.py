
from fastapi import APIRouter

from app.services.memory_service import build_memory_context

router = APIRouter()


@router.get("/test-memory")
async def test_memory():

    user_id = "test-user-123"
    chat_id = "test-chat-123"
    message = "I want a beach vacation in Goa"

    try:

        memory = await build_memory_context(
            user_id=user_id,
            chat_id=chat_id,
            message=message
        )

        return {
            "success": True,
            "memory": memory
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
