from pydantic import BaseModel

class CategorySchema(BaseModel):
    name:str
    
    class Config:
        orm_mode = True
        

