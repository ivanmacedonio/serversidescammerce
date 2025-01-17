from fastapi import APIRouter, Depends, Query, Request
from ..utils.custom_responses import make_response, abort
from sqlalchemy.orm import Session
from ..config.database_config import get_db
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import Product, Category, Shop
from ..schemas.product import ProductCreateDTO, ProductUpdateDTO

router = APIRouter()

@router.get("/products")
async def get_products(request:Request,
                       skip: int = Query(0, ge=0),
                       limit: int = Query(10, le=20 ),
                       db: Session = Depends(get_db)):
    try:
        shop_id = request.headers.get("Shop-Id")
        filter_name = request.query_params.get("name", None)
        query = db.query(Product).filter(Product.deleted == False)
        if filter_name:
            query.filter(Product.name.ilike(f"%{filter_name}%"))
        response = query.order_by(Product.created_at).offset(skip).limit(limit).all()
        return make_response([product.to_json() for product in response], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/products GET")
        
@router.get("/products/{product_id}")
async def get_product_by_id(request:Request, product_id:int, db: Session = Depends(get_db)):
    if not id: abort(400, "Product ID is required")
    try:
        shop_id = request.headers.get("Shop-Id")
        product_q = db.query(Product).filter(Product.id == product_id).first()
        if not product_q: abort(404, f"Product with ID {product_id} not found")
        return make_response(product_q.to_json(), 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/products/{product_id} GET")
        
@router.post("/products")
async def create_product(request:Request, body:ProductCreateDTO, db: Session = Depends(get_db)):
    shop_id = request.headers.get("Shop-Id", None)
    if not shop_id: abort(400, "Shop ID is required")
    shop_q = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop_q: abort(404, f"Shop with ID {shop_id} not found!")
    
    product_q = db.query(Product).filter(Product.name == body.name).first()
    category_q = db.query(Category).filter(Category.id == body.category_id).first()
    
    if not category_q: abort(404, f"Category with ID {body.category_id} not found!")
    if product_q: abort(400, "Product name already exists")
    try:
        product_instance = Product(body, shop_id)
        db.add(product_instance)
        db.commit()
        db.refresh(product_instance)
        return make_response("Product created successfully", 201)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/products POST")
        
@router.put("/products/{product_id}")
async def update_product(request:Request, product_id:int, body:ProductUpdateDTO, db: Session = Depends(get_db)):
    if not product_id: abort(400, "Product ID is required")
    shop_id = request.headers.get("Shop-Id")
    product_q = db.query(Product).filter(Product.id == product_id).first()
    if not product_q: abort(404, f"Product with ID {product_id} not found")
    category_q = db.query(Category).filter(Category.id == body.category_id).first()
    if not category_q: abort(404, f'Category with ID {body.category_id} not found!')
    
    try:
        db.query(Product).filter(Product.id == product_id).update({
            "name": body.name,
            "description": body.description,
            "price": body.price,
            "offer": body.offer,
            "discount": body.discount
        })
        db.commit()
        return make_response("Product updated successfully", 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/products/{product_id} PUT")
    
@router.delete("/products/{product_id}")
async def delete_product(request:Request, product_id:int, db:Session = Depends(get_db)):
    if not product_id: abort(400, "Product ID is required")
    try:
        shop_id = request.headers.get("Shop-Id")
        product_q = db.query(Product).filter(Product.id == product_id).first()
        if not product_q: abort(404, f"Product with ID {product_q} not exists")
        db.query(Product).filter(Product.id == product_id).update({
            "deleted": True
        })
        db.commit()
        make_response("Product deleted successfully", 200)
    except SQLAlchemyError as e:
        make_response(str(e), 500, "/products/{product_id} DELETE")