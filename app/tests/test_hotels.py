
from fastapi import APIRouter

from app.services.serp_service import search_hotels

router = APIRouter()


@router.get("/test-hotels")
def test_hotels():

    destination = "Goa"
    check_in = "2026-09-06"
    check_out = "2026-09-11"

    try:
        hotels = search_hotels(
            destination=destination,
            check_in=check_in,
            check_out=check_out
        )

        return {
            "success": True,
            "destination": destination,
            "count": len(hotels),
            "hotels": hotels[:5] 
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

