from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.custom_responses import make_response, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
from ..models.models import User
from ..schemas.user import UserCreateDTO
from ..config.database_config import get_db

router = APIRouter()

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    try:
        response = db.query(User).filter(User.deleted == False)
        return make_response([user.to_json() for user in response], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/users GET")
    
@router.get("/users/{user_id}")
async def get_user_by_id(user_id:int, db: Session = Depends(get_db)):
    if not user_id: abort(400, "User ID is required")
    try:
        response = db.query(User).filter(User.id == user_id).first()
        if not response: abort(400, "User not found")
        return make_response(response.to_json(), 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/users/{user_id} GET")

@router.get("/users/{user_id}/cards")
async def get_cards_by_user(user_id:int, db: Session = Depends(get_db)):
    if not user_id: abort(400, "User Id is required")
    try:
        user_q = db.query(User).filter(User.id == user_id).first()
        if not user_q: abort(400, f'User with ID {user_id} not found')
        return make_response([card.to_json() for card in user_q.card], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/users/cards GET")

@router.post("/users")
async def create_user(body:UserCreateDTO, db: Session = Depends(get_db)):
    try:
        user_instance = User(body)
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)
        return make_response("User created successfully!", 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/users POST" )
    
@router.delete("/users/{user_id}")
async def delete_user(user_id:int, db: Session = Depends(get_db)):
    if not user_id: abort(400, "User ID is required")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user: abort(404, "User not found")
        db.query(User).filter(User.id == user_id).update({"deleted": True})
        db.commit()
        return make_response("User deleted Successfully", 200)
    except SQLAlchemyError as e:
        return make_response( f'Database conn error: {str(e)}', 400, "/users/{user_id} DELETE" )
    