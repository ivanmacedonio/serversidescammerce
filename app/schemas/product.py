from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    name:str
    description:str
    price:float
    offer:Optional[bool] = False
    discount:Optional[float] = 0
    category_id:int
    image_url:str
    
    class Config:
        orm_mode = True
    
class ProductCreateDTO(ProductSchema):
    pass

class ProductUpdateDTO(ProductSchema):
    pass
 