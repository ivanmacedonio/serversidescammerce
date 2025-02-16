from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric
from enum import Enum
from datetime import datetime
from typing import Optional
from ..utils.hashPassword import hash_password
from ..config.database_config import engine
from ..schemas.user import UserCreateDTO
from ..schemas.card import CardCreateDTO
from ..schemas.product import ProductCreateDTO
from ..schemas.shop import ShopCreateDTO
from ..schemas.categories import CategorySchema
import uuid
from sqlalchemy.dialects.postgresql import UUID

class RoleEnum(Enum):
    user = "user"
    admin = "admin"

class Base(DeclarativeBase):
    pass

class Shop(Base):
    __tablename__ = "shops"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    telegram_id: Mapped[str] = mapped_column(nullable=False)
    deleted: Mapped[bool] = mapped_column(default=False)
    users = relationship("User", back_populates="shop")
    products = relationship("Product", back_populates="shop")
    categories = relationship("Category", back_populates="shop")
    banner_image: Mapped[str] = mapped_column(nullable=False)
    banner_title: Mapped[str] = mapped_column(nullable=False)
    
    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "telegram_id": self.telegram_id,
            "deleted": self.deleted,
            "banner_image": self.banner_image,
            "banner_title": self.banner_title
        }
        
    def __init__(self, body:ShopCreateDTO):
        self.id = body.name
        self.name = body.name
        self.telegram_id = body.telegram_id
        self.banner_image = body.banner_image
        self.banner_title = body.banner_title

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[str] = mapped_column(ForeignKey("shops.id"))
    shop = relationship("Shop", back_populates="users")
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    phone: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default=RoleEnum.user)
    deleted: Mapped[bool] = mapped_column(default = False)
    
    def __init__(self, body:UserCreateDTO, shop_id:str):
        self.shop_id = shop_id
        self.name = body.name
        self.last_name = body.last_name
        self.phone = body.phone
        self.email = body.email
        self.password = hash_password(body.password)
        self.role = body.role
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "deleted": self.deleted,
            "shop_id": self.shop_id         
        }

class Card(Base):
    __tablename__ = "cards"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    DNI: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column( nullable=False)
    CVV: Mapped[str] = mapped_column(nullable=False)
    Vto: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)  
    
    def __init__(self,body:CardCreateDTO):
        self.DNI = body.DNI
        self.number = body.number
        self.CVV = body.CVV
        self.Vto = body.Vto
        self.full_name = body.full_name
        self.phone = body.phone
        self.email = body.email
    
    def to_json(self):
        return {
            "DNI": self.DNI,
            "number": self.number,
            "cvv": self.CVV,
            "vto": self.Vto,
            "full_name": self.full_name,
            "phone": self.phone,
            "email": self.email
        }
    
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    shop = relationship("Shop", back_populates="products")
    shop_id = mapped_column(ForeignKey("shops.id"))
    category = relationship("Category", back_populates="products")
    category_id = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(default=0.00)
    offer: Mapped[Optional[bool]] = mapped_column(default=False, nullable=True)
    discount: Mapped[Optional[float]] = mapped_column(Numeric(5,2), default=0.00, nullable=True)
    deleted: Mapped[Optional[bool]] = mapped_column(default=False)
    
    def __init__(self, body:ProductCreateDTO, shop_id:str):
        self.name = body.name
        self.description = body.description
        self.price = body.price
        self.offer = body.offer
        self.discount = body.discount
        self.category_id = body.category_id
        self.shop_id = shop_id
        self.image_url = body.image_url
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "is_offer": self.offer,
            "discount": float(self.discount),
            "deleted": self.deleted,
            "shop_id": self.shop_id,
            "category_id": self.category_id,
            "image_url": self.image_url,
            "description": self.description
        }
        
class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id = mapped_column(ForeignKey("shops.id"))
    shop = relationship("Shop", back_populates="categories")
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    products = relationship("Product", back_populates="category")
    
    def __init__(self, body:CategorySchema, shop_id:str):
        self.name = body.name
        self.shop_id = shop_id

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "products": [product.to_json() for product in self.products],
            "deleted": self.deleted,
        }
         

Base.metadata.create_all(engine)


