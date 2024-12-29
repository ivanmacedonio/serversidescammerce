from pydantic import BaseModel

class CardSchema(BaseModel):
    user_id:int
    number:str
    DNI:str
    CVV:str
    Vto:str
    
    class Config:
        orm_mode = True

class CardCreateDTO(CardSchema):
    pass
        
