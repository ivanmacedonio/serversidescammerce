from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name:str
    last_name:str
    phone:str
    email:str
    password:str
    role:str
    deleted:bool
    
    class Config:
        orm_mode = True
        
class UserToLogin(BaseModel):
    email:EmailStr
    password:str
    
    class Config:
        orm_mode = True

class UserCreateDTO(UserSchema):
    deleted:bool = False
    
    class Config:
        orm_mode = True
        
class UserUpdateDTO(UserCreateDTO):
    pass