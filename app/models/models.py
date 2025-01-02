from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric
from enum import Enum
from typing import Optional
from ..utils.hashPassword import hash_password
from ..config.database_config import engine
from ..schemas.user import UserCreateDTO
from ..schemas.card import CardCreateDTO
from ..schemas.product import ProductCreateDTO
from ..schemas.shop import ShopCreateDTO

class RoleEnum(Enum):
    user = "user"
    admin = "admin"

class Base(DeclarativeBase):
    pass

class Shop(Base):
    __tablename__ = "shops"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    telegram_id: Mapped[str] = mapped_column(nullable=False)
    deleted: Mapped[bool] = mapped_column(default=False)
    users = relationship("User", back_populates="shop")
    products = relationship("Product", back_populates="shop")
    
    def to_json(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id
        }
        
    def __init__(self, body:ShopCreateDTO):
        self.name = body.name
        self.telegram_id = body.telegram_id

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
    shop = relationship("Shop", back_populates="users")
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default=RoleEnum.user)
    card = relationship("Card", back_populates="user")
    deleted: Mapped[bool] = mapped_column(default = False)
    
    def __init__(self, body:UserCreateDTO):
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
            "card": [card.to_json() for card in self.card],
            "role": self.role,
            "deleted": self.deleted         
        }

class Card(Base):
    __tablename__ = "cards"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user = relationship("User", back_populates="card")
    DNI: Mapped[str] = mapped_column(nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))
    number: Mapped[str] = mapped_column( nullable=False)
    CVV: Mapped[str] = mapped_column(nullable=False)
    Vto: Mapped[str] = mapped_column(nullable=False)
    
    def __init__(self,body:CardCreateDTO):
        self.user_id = body.user_id
        self.DNI = body.DNI
        self.number = body.number
        self.CVV = body.CVV
        self.Vto = body.Vto
    
    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "number": self.number,
            "cvv": self.CVV,
            "vto": self.Vto
        }
    
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    shop = relationship("Shop", back_populates="product")
    shop_id = mapped_column(ForeignKey("shops.id"))
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column( nullable=False)
    price: Mapped[float] = mapped_column(default=0.00)
    offer: Mapped[Optional[bool]] = mapped_column(default=False, nullable=True)
    discount: Mapped[Optional[float]] = mapped_column(Numeric(5,2), default=0.00, nullable=True)
    deleted: Mapped[Optional[bool]] = mapped_column(default=False)
    
    def __init__(self, body:ProductCreateDTO):
        self.name = body.name
        self.description = body.description
        self.price = body.price
        self.offer = body.offer
        self.discount = body.discount
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "is_offer": self.offer,
            "discount": float(self.discount),
            "deleted": self.deleted
        }
         

Base.metadata.create_all(engine)


