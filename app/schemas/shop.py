from pydantic import BaseModel
from typing import Optional

class ShopSchema(BaseModel):
    name:str
    telegram_id:str
    deleted:Optional[bool]
    
    class Config:
        orm_mode = True
        
class ShopCreateDTO(ShopSchema):
    pass

class ShopUpdateDTO(ShopSchema):
    pass

