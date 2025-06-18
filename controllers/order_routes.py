from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from config.dependencies import verify_token, get_session
from factories import AccessFactory
from models import Dweller, Uber, DeliveryGuy, Guest 
from schemas import AccessRequestSchema
from utils.utils import Validator, PlateValidation
from services.notice import MailNotice


router = InferringRouter(
    prefix="/order",
    tags=["order"],
    dependencies=[Depends(verify_token)]
)
@cbv(router)
class OrderView:
    session: Session = Depends(get_session)
    dweller: Dweller = Depends(verify_token)
    mailNotice: MailNotice = Depends(MailNotice)

    @router.post("/request-access")
    async def request_access(self, schema: AccessRequestSchema):
        validator = Validator(PlateValidation())

        if schema.access_type == "uber" and not validator.perform_validation(schema.license_plate):
            raise HTTPException(status_code=400, detail="Placa inválida")

        try:
            access_object = AccessFactory.create_access(schema, self.dweller.id)
            self.session.add(access_object)
            self.session.commit()

        except ValueError as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Erro ao processar solicitação")

        response = {
            "message": f"Acesso liberado para {schema.access_type} {schema.name or ''}",
            schema.access_type: {
                "name": schema.name,
                "address": schema.address,
                **({"license_plate": schema.license_plate} if schema.access_type == "uber" else {}),
                **({"establishment": schema.establishment} if schema.access_type == "delivery" else {}),
                **({"is_driving": schema.is_driving} if schema.access_type == "guest" else {}),
            }
        }

        self.mailNotice.update_admins(self.session)
        self.mailNotice.send_notices(response, schema.access_type)

        return response