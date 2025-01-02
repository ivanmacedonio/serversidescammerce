from fastapi import APIRouter, Depends
from ..utils.custom_responses import make_response, abort
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..config.database_config import get_db
from ..models.models import Shop
from ..schemas.shop import ShopCreateDTO, ShopUpdateDTO

router = APIRouter()

@router.get("/shops")
async def get_shops(db: Session = Depends(get_db)):
    try:
        response = db.query(Shop).all()
        return make_response([shop.to_json() for shop in response], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/shops GET")
    
@router.post("/shops")
async def create_shop(body:ShopCreateDTO, db:Session = Depends(get_db)):
    try:
        shop_instance = Shop(body)
        db.add(shop_instance)
        db.commit()
        db.refresh(shop_instance)
        
        return make_response("Shop created successfully", 201)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/shops POST")
    
@router.put("/shops/{shop_id}")
async def update_shop(shop_id:int, body:ShopUpdateDTO, db:Session = Depends(get_db)):
    try:
        shop_q = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop_q: abort(404, f"Invalid shop id {shop_id}")
        db.query(Shop).filter(Shop.id == shop_id).update({
            "telegram_id": body.telegram_id,
            "name": body.name
        })
        db.commit()
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/shops/{shop_id} PUT")

@router.delete("/shops/{shop_id}")
async def delete_shop(shop_id:int, db:Session = Depends(get_db)):
    try:
        shop_q = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop_q: abort(404, f"Invalid shop id {shop_id}")
        db.query(Shop).filter(Shop.id == shop_id).update({
            "deleted":True
        })
        db.commit()
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/shops/{shop_id} DELETE")