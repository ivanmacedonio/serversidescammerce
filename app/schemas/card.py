from pydantic import BaseModel

class CardSchema(BaseModel):
    number:str
    DNI:str
    CVV:str
    Vto:str
    full_name:str
    phone:str
    email:str
    
    class Config:
        orm_mode = True

class CardCreateDTO(CardSchema):
    pass
        
