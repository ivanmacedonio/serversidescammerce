from .controllers.users import router as users_router
from .controllers.cards import router as cards_router
from .controllers.products import router as products_router
from .controllers.auth import router as auth_router
from .controllers.categories import router as categories_router
from .controllers.shops import router as shops_router
from .middleware.auth_middleware import verify_is_request_authenticated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

# Middlewares
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware('http')(verify_is_request_authenticated)
# app.middleware('http')(verify_shop_id)

# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(cards_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(shops_router)

@app.get("/")
def root():
    return {"message": "server alive", "code": 200}




