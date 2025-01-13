from fastapi import APIRouter, Depends, Request
from ..utils.custom_responses import make_response, abort
from sqlalchemy.orm import Session
from ..config.database_config import get_db
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import Category, Shop
from ..schemas.categories import CategorySchema

router = APIRouter()

@router.get("/categories")
async def get_categories(request:Request ,db: Session = Depends(get_db)):
    try:
        shop_id = request.headers.get("Shop-Id")
        categories_q = db.query(Category).filter(Category.deleted == False, Category.shop_id == shop_id)
        return make_response([category.to_json() for category in categories_q], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/categories GET")
    
@router.get("/categories/{category_id}")
async def get_category_by_id(request:Request, category_id:int, db:Session = Depends(get_db)):
    if not category_id: abort(400, "Category ID is required")
    try:
        shop_id = request.headers.get("Shop-Id")
        category_q = db.query(Category).filter(Category.id == category_id, Category.shop_id == shop_id).first()
        if not category_q: abort(404, f"Category with ID {category_id} not found!")
        return make_response(category_q.to_json(), 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/categories/{category_id} GET")

@router.post("/categories")
async def create_category(request:Request ,body:CategorySchema, db:Session = Depends(get_db)):
    shop_id = request.headers.get("Shop-Id", None)
    if not shop_id: abort(400, "Shop ID is required")
    shop_q = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop_q: abort(404, f"Shop with ID {shop_id} not found!")
    
    try:
        category_instance = Category(body, shop_id)
        db.add(category_instance)
        db.commit()
        db.refresh(category_instance)
        return make_response("Category created successfully!", 201)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/categories POST")
    
@router.put("/categories/{category_id}")
async def update_category(request:Request, category_id:int, body:CategorySchema, db:Session = Depends(get_db)):
    try:
        shop_id = request.headers.get("Shop-Id")
        category_instance = db.query(Category).filter(Category.id == category_id, Category.shop_id == shop_id).first()
        if not category_instance: abort(404, f"Category with ID {category_id} not found!")
        db.query(Category).filter(Category.id == category_id).update({
            "name": body.name
        })
        db.commit()
        return make_response("Category updated successfully!", 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/categories/{category_id} PUT")
    
@router.delete("/categories/{category_id}")
async def delete_category(request:Request, category_id:int, db:Session = Depends(get_db)):
    try:
        shop_id = request.headers.get("Shop-Id")
        category_instance = db.query(Category).filter(Category.id == category_id, Category.shop_id == shop_id).first()
        if not category_instance: abort(404, f"Category with ID {category_id} not found!")
        db.query(Category).filter(Category.id == category_id).update({
            "deleted": True
        })
        db.commit()
        return make_response("Category deleted successfully!", 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/categories/{category_id} DELETE")
    