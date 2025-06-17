from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.settings import SECRET_KEY, ALG, ACCESS_TOKEN_DURATION


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

from controllers.auth_routes import auth_router
from controllers.order_routes import order_router
from controllers.site_routes import site_router

app.include_router(auth_router)
app.include_router(order_router)
