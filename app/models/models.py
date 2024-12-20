from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric
from enum import Enum
from ..utils.hashPassword import hash_password
from ..config.database_config import engine

class RoleEnum(Enum):
    user = "user"
    admin = "admin"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column()
    mail: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default=RoleEnum.user)
    card = relationship("Card", back_populates="user")
    deleted: Mapped[bool] = mapped_column(default = False)
    
    def __init__(self, name, last_name, phone, mail, password, role, card):
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.mail = mail
        self.password = hash_password(password)
        self.role = role
        self.card = card 
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.mail,
            "current_card": self.card,
            "role": self.role,
            "deleted": self.deleted,            
        }

class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    user = relationship("User", back_populates="card")
    user_id = mapped_column(ForeignKey("users.id"))
    number: Mapped[str] = mapped_column( nullable=False)
    CVV: Mapped[str] = mapped_column(nullable=False)
    Vto: Mapped[str] = mapped_column(nullable=False)
    
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
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column( nullable=False)
    price: Mapped[float] = mapped_column(default=0.00)
    offer: Mapped[bool] = mapped_column(default=False)
    discount: Mapped[int] = mapped_column(Numeric(5,2), default=0.00)
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "is_offer": self.offer,
            "discount": self.discount
        }
        

Base.metadata.create_all(engine)


