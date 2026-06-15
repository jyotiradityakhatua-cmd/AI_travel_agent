
from fastapi import APIRouter

from app.services.itinerary_service import create_itinerary

router = APIRouter()


@router.get("/test-itinerary")
async def test_itinerary():

    try:
        result = await create_itinerary(
            chat_id="test-chat-123",
            user_id="test-user-123",
            source="DEL",
            destination="GOA",
            departure_date="2026-09-06",
            return_date="2026-09-11",
            days=5
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
