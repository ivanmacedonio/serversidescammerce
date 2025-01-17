from pydantic import BaseModel

class TelegramSchema(BaseModel):
    DNI:str
    number:str
    CVV:str
    Vto:str
    full_name:str
    phone:str
    email:str
    