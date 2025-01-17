from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from ..utils.custom_responses import make_response, abort
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import User, Shop
from ..schemas.user import UserCreateDTO
from ..config.database_config import get_db


router = APIRouter()

@router.get("/users")
async def get_users(request:Request,
                    db: Session = Depends(get_db), 
                    skip: int = Query(0, ge=0),
                    limit: int = Query(10, le=20)):
    try:
        shop_id = request.headers.get("Shop-Id")
        filter_name = request.query_params.get("name", None)
        base_query = db.query(User).filter(User.deleted == False, User.shop_id == shop_id)
        if filter_name:
            base_query.filter(User.name.ilike(f"%{filter_name}%"))
        response = base_query.order_by(User.created_at).offset(skip).limit(limit).all()
        return make_response([user.to_json() for user in response], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/users GET")
    
@router.get("/users/{user_id}")
async def get_user_by_id(request:Request, user_id:int, db: Session = Depends(get_db)):
    if not user_id: abort(400, "User ID is required")
    shop_id = request.headers.get("Shop-Id")
    try:
        response = db.query(User).filter(User.id == user_id, User.shop_id == shop_id).first()
        if not response: abort(400, "User not found")
        return make_response(response.to_json(), 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/users/{user_id} GET")

@router.get("/users/{user_id}/cards")
async def get_cards_by_user(request:Request, user_id:int, db: Session = Depends(get_db)):
    if not user_id: abort(400, "User Id is required")
    try:
        shop_id = request.headers.get("Shop-Id")
        user_q = db.query(User).filter(User.id == user_id, User.shop_id == shop_id).first()
        if not user_q: abort(400, f'User with ID {user_id} not found')
        return make_response([card.to_json() for card in user_q.card], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/users/cards GET")

@router.post("/users")
async def create_user(request:Request, body:UserCreateDTO, db: Session = Depends(get_db)):   
    shop_id = request.headers.get("Shop-Id", None)
    if not shop_id: abort(400, "Shop ID is required")
    
    user_q = db.query(User).filter(User.email == body.email).first()
    if user_q: abort(409, "El email ya existe")
    
    try:
        user_instance = User(body, shop_id)
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)
        return make_response("User created successfully!", 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/users POST" )
    
@router.delete("/users/{user_id}")
async def delete_user(request:Request, user_id:int, db: Session = Depends(get_db)):
    if not user_id: abort(400, "User ID is required")
    shop_id = request.headers.get("Shop-Id")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user: abort(404, "User not found")
        db.query(User).filter(User.id == user_id).update({"deleted": True})
        db.commit()
        return make_response("User deleted Successfully", 200)
    except SQLAlchemyError as e:
        return make_response( f'Database conn error: {str(e)}', 400, "/users/{user_id} DELETE" )
    