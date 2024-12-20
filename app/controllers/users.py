from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
from ..models.models import User
from ..schemas.user import UserCreateDTO, UserUpdateDTO
from ..config.database_config import get_db
from ..utils.to_update import to_update

router = APIRouter()

@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    try:
        response = db.query(User).all()
        return JSONResponse(content={"data": list(response), "status": 200})
    except (Exception, SQLAlchemyError) as e:
        return JSONResponse(content={"message": str(e), "status": 500, "scope": "/users GET"})
    
@router.get("/users/{user_id}")
async def get_user_by_id(user_id:int, db: Session = Depends(get_db)):
    try:
        response = db.query(User).filter(User.id == user_id).first()
        if not response: raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(content={"data": response.to_json(), "status": 200})
    except SQLAlchemyError as e:
        return JSONResponse(content={"message": str(e), "status": 404, "scope": "/users/user_id GET"})
    except Exception as e:
        return JSONResponse(content={"message": str(e), "status": 500, "scope": "/users/user_id GET"})
    
@router.post("/users")
async def create_user(user:UserCreateDTO, db: Session = Depends(get_db)):
    try:
        print(user)
        user_instance = User(name=user.name,
                             last_name=user.last_name,
                             phone=user.phone,
                             mail=user.email,
                             password=user.password,
                             role=user.role,
                             card=[])
        
        db.add(user_instance)
        db.commit()
        db.refresh(user_instance)
        return JSONResponse(content={"message": "User created successfully!"}, status_code=201)
    
    except SQLAlchemyError as e:
        return JSONResponse(content={"message": str(e), "status": 400, "scope": "/users POST"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message": "Internal server error", "details": str(e)}, status_code=500)
    
'''
Deberia considerar utilizar sqlalchemy.update
para ejecutar la query de update, El metodo 
no esta probado
'''
@router.put("/users/{user_id}") 
async def update_user(user_id:int, user:UserUpdateDTO, db: Session = Depends(get_db)):
    try:
        if not user_id: raise HTTPException(status_code=400, detail="User ID is required")
        user_q = db.query(User).filter(User.id == user_id).first()   
        if not user_q: raise HTTPException(status_code=404, detail=f"User with ID {user_id} not Found") 
        to_update(user_q, user)
        
        db.commit()
        return JSONResponse(content={"message": "User updated Successfully!", "status": 204})
    except SQLAlchemyError as e:
        return JSONResponse(content={"message": f'Database conn error: {str(e)}', "status": 400, "scope": "/users PUT"})
    except Exception as e:
        return JSONResponse(content={"message":f'Unexpected error: {str(e)}', "status": 500, "scope": "/users PUT"})
    
@router.delete("/users/{user_id}")
async def delete_user(user_id:int, db: Session = Depends(get_db)):
    try:
        if not user_id: raise HTTPException(status_code=400, detail="User ID is required")
        user = db.query(User).filter(User.id == user_id).first()
        if not user: raise HTTPException(status_code=404, detail="User not found")
        
        statement = update(User).where(User.id == user_id).values(deleted = True)
        db.execute(statement)
        return JSONResponse(content={"message": "User deleted Successfully", "code": 200})
    except SQLAlchemyError as e:
        return JSONResponse(content={"message": f'Database conn error: {str(e)}', "status": 400, "scope": "/users/{user_id} DELETE"})
    except Exception as e:
        return JSONResponse(content={"message": f"Unexpected error: {str(e)}", "status": 500, "scope": "/users/{user_id} DELETE"})
    