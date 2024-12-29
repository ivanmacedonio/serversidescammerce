from fastapi import APIRouter, Depends
from ..utils.custom_responses import make_response, abort
from sqlalchemy.orm import Session
from ..config.database_config import get_db
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import Product
from ..schemas.product import ProductCreateDTO, ProductUpdateDTO

router = APIRouter()

@router.get("/products")
async def get_products(db: Session = Depends(get_db)):
    try:
        response = db.query(Product).filter(Product.deleted == False)
        return make_response([product.to_json() for product in response], 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/products GET")
        
@router.get("/products/{product_id}")
async def get_product_by_id(product_id:int, db: Session = Depends(get_db)):
    if not id: abort(400, "Product ID is required")
    try:
        response = db.query(Product).filter(Product.id == product_id).first()
        return make_response(response.to_json(), 200)
    except SQLAlchemyError as e:
        return make_response(str(e), 500, "/products/{product_id} GET")
        
@router.post("/products")
async def create_product(body:ProductCreateDTO, db: Session = Depends(get_db)):
    product_q = db.query(Product).filter(Product.name == body.name).first()
    if product_q: abort(400, "Product name already exists")
    try:
        product_instance = Product(body)
        db.add(product_instance)
        db.commit()
        db.refresh(product_instance)
        return make_response("Product created successfully", 201)
    except SQLAlchemyError as e:
        return make_response(str(e), 400, "/products POST")
        
@router.put("/products/{product_id}")
async def update_product(product_id:int, body:ProductUpdateDTO, db: Session = Depends(get_db)):
    if not product_id: abort(400, "Product ID is required")
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
async def delete_product(product_id:int, db:Session = Depends(get_db)):
    if not product_id: abort(400, "Product ID is required")
    try:
        product_q = db.query(Product).filter(Product.id == product_id).first()
        if not product_q: abort(404, f"Product with ID {product_q} not exists")
        db.query(Product).filter(Product.id == product_id).update({
            "deleted": True
        })
        db.commit()
        make_response("Product deleted successfully", 200)
    except SQLAlchemyError as e:
        make_response(str(e), 500, "/products/{product_id} DELETE")