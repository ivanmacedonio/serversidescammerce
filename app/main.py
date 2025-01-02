from .controllers.users import router as users_router
from .controllers.cards import router as cards_router
from .controllers.products import router as products_router
from .controllers.auth import router as auth_router
from .controllers.shops import router as shops_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(cards_router)
app.include_router(products_router)
app.include_router(shops_router)

@app.get("/")
def root():
    return {"message": "server alive", "code": 200}




