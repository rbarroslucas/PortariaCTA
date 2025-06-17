from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
import httpx
from config.settings import API_URL


router = InferringRouter()
templates = Jinja2Templates(directory="templates")


@cbv(router)
class SiteView:

    @router.get("/", response_class=HTMLResponse)
    def home(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse("/login")
        return templates.TemplateResponse("home.html", {"request": request})

    @router.get("/login", response_class=HTMLResponse)
    def login_get(self, request: Request):
        return templates.TemplateResponse("login.html", {"request": request, "message": ""})

    @router.post("/login")
    async def login_post(
        self,
        request: Request,
        response: Response,
        username: str = Form(...),
        password: str = Form(...)
    ):
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(f"{API_URL}/auth/login", json={
                    "cpf": username,
                    "password": password
                })

                if res.status_code == 200:
                    data = res.json()
                    redirect = RedirectResponse("/", status_code=302)
                    redirect.set_cookie(
                        key="access_token",
                        value=data["access_token"],
                        httponly=True
                    )
                    return redirect
                else:
                    return templates.TemplateResponse("login.html", {
                        "request": request,
                        "message": "CPF ou senha inválidos"
                    })
            except httpx.RequestError:
                return templates.TemplateResponse("login.html", {
                    "request": request,
                    "message": "Erro ao conectar na API"
                })

    @router.get("/logout")
    def logout(self):
        redirect = RedirectResponse("/login")
        redirect.delete_cookie("access_token")
        return redirect

    @router.get("/solicitar", response_class=HTMLResponse)
    def solicitar_get(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse("/login")
        return templates.TemplateResponse("solicitar.html", {"request": request, "message": ""})

    @router.post("/solicitar")
    async def solicitar_post(
        self,
        request: Request,
        tipo: str = Form(...),
        nome_uber: str = Form(None),
        placa: str = Form(None),
        endereco_uber: str = Form(None),
        solicitante_uber: str = Form(None),
        nome_entregador: str = Form(None),
        empresa_entregador: str = Form(None),
        endereco_entregador: str = Form(None),
        solicitante_entregador: str = Form(None)
    ):
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse("/login")

        async with httpx.AsyncClient() as client:
            if tipo == "uber":
                res = await client.post(f"{API_URL}/order/request-uber-access",
                    json={
                        "name": nome_uber,
                        "license_plate": placa,
                        "address": endereco_uber,
                        "user": solicitante_uber
                    },
                    headers={"Authorization": f"Bearer {token}"}
                )
            elif tipo == "entregador":
                res = await client.post(f"{API_URL}/order/request-delivery-access",
                    json={
                        "name": nome_entregador,
                        "establishment": empresa_entregador,
                        "address": endereco_entregador,
                        "user": solicitante_entregador
                    },
                    headers={"Authorization": f"Bearer {token}"}
                )
            else:
                return templates.TemplateResponse("solicitar.html", {
                    "request": request,
                    "message": "Selecione um tipo de solicitação válido."
                })

            if res.status_code == 200:
                return RedirectResponse("/sucesso", status_code=302)
            else:
                return templates.TemplateResponse("solicitar.html", {
                    "request": request,
                    "message": "Erro ao processar a solicitação."
                })

    @router.get("/sucesso", response_class=HTMLResponse)
    def sucesso(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse("/login")
        return templates.TemplateResponse("sucesso.html", {"request": request})
