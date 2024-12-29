from fastapi import APIRouter, Depends
from ..utils.custom_responses import make_response, abort
from sqlalchemy.orm import Session
from ..config.database_config import get_db
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import Card, User
from ..schemas.card import CardCreateDTO

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

@router.post("/cards")
async def create_card(body:CardCreateDTO, db: Session = Depends(get_db)):
    user_id = body.user_id
    if not user_id: abort(400, "User ID is required")
    try:
        user_q = db.query(User).filter(User.id == user_id, User.deleted == False).first()
        if not user_q: abort(404, f"User with ID {user_id} not found")
        
        card_instance = Card(body)
        db.add(card_instance)
        db.commit()
        db.refresh(card_instance)
        
        return make_response("Card created successfully", 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/cards POST")
    

