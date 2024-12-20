from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..config.database_config import get_db
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import Card
from ..schemas.card import *

router = APIRouter()

@router.get("/cards")
async def get_cards(db: Session = Depends(get_db)):
    try:
        response = db.query(Card).all()
        return JSONResponse(content={"data": list(response)})
    except SQLAlchemyError as e:
        return JSONResponse(content={"message": str(e), "status": 400, "scope": "/cards GET"})
    except Exception as e:
        return JSONResponse(content={"message": f'Unexpected internal error: {str(e)}', "status": 500, "scope": "/cards GET"})
