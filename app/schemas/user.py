from pydantic import BaseModel, EmailStr

class UserCreateDTO(BaseModel):
    name:str
    last_name:str
    phone:str
    email:EmailStr
    password:str
    role:str
    
    class Config:
        orm_mode = True
        
class UserUpdateDTO(BaseModel):
    name:str
    last_name:str
    phone:str
    email:EmailStr
    password:str
    role:str
    
    class Config:
        orm_mode = True