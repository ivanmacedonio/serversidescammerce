from fastapi import APIRouter, Depends, Request
import datetime
from ..utils.custom_responses import make_response, abort
from sqlalchemy.orm import Session
from ..config.database_config import get_db
from sqlalchemy.exc import SQLAlchemyError
from ..models.models import User, Shop
from ..schemas.user import UserToLogin
from pydantic import EmailStr
from ..utils.hashPassword import verify_hash
from ..config.settings import Settings
import jwt

router = APIRouter()
settings = Settings()

def verify_user_exists(db: Session, email:EmailStr, shop_id:str):
    if not email: abort(400, "User email is Required")
    try:
        user_q = db.query(User).filter(User.email == email, User.shop_id == shop_id).first()
        return user_q
    except SQLAlchemyError as e:
        make_response(str(e), 500, "get_user_or_404")    
        
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=int(settings.jwt_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_secret_algorithm)
    #encoded jwt should have shop id in payload
    return encoded_jwt

def verify_access_token(token):
    if not token: abort(401, "Token is required")
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_secret_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        abort(401, "Token is expired")
    except jwt.JWTError as e:
        abort(401, "Could not validate credentials")

@router.post("/login")
async def login(request:Request ,body:UserToLogin, db: Session = Depends(get_db)):
    shop_id = request.headers.get("Shop-Id", None)
    db_user = verify_user_exists(db, body.email, shop_id)
    if not db_user: abort(401, "Invalid email or password")
    
    shop_q = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop_q: abort(404, f"Shop with ID {shop_id} not found")
    
    is_password_valid = verify_hash(body.password, db_user.password)
    if not is_password_valid: abort(401, "Invalid password")
    access_token = create_access_token(data={"email":body.email, "role": db_user.role}) 
    return make_response({"access_token": access_token, "token_type": "bearer"}, 200) 

    
