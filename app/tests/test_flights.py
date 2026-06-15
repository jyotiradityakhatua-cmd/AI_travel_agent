
from fastapi import APIRouter

from app.services.serp_service import search_flights

router = APIRouter()


@router.get("/test-flights")
def test_flights():

    source = "DEL"
    destination = "GOA"
    departure_date = "2026-09-06"
    return_date = "2026-09-11"

    try:
        flights = search_flights(
            source=source,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date
        )

        return {
            "success": True,
            "source": source,
            "destination": destination,
            "count": len(flights),
            "flights": flights[:5] 
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
