from .controllers.users import router as users_router
from .controllers.cards import router as cards_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(users_router)
app.include_router(cards_router)

@app.get("/")
def root():
    return {"message": "server alive", "code": 200}




