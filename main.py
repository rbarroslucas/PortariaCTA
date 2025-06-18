from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.auth_routes import router as auth_router
from controllers.order_routes import router as order_router

app = FastAPI()

# Protótipo de CORS
# Permite que o frontend acesse a API de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(order_router)
