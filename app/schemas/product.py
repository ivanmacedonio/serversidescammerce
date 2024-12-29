from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    name:str
    description:str
    price:float
    offer:Optional[bool]
    discount:Optional[float]
    
    class Config:
        orm_mode = True
    
class ProductCreateDTO(ProductSchema):
    pass

class ProductUpdateDTO(ProductSchema):
    pass
 