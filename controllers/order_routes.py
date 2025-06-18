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

        #Access Factory
        #access_object = AccessFactory.create_access(schema, self.dweller.id)
        #self.session.add(access_object)

        response = {}

        if schema.access_type == "uber":
            if not validator.perform_validation(schema.license_plate):
                raise HTTPException(status_code=400, detail="Placa inválida")

            new_transport = Uber(
                name=schema.name,
                license_plate=schema.license_plate,
                address=schema.address,
                user=schema.user,
                dweller_id=self.dweller.id
            )
            self.session.add(new_transport)

            response = {
                "message": f"Acesso liberado para transporte {new_transport.name}",
                "uber": {
                    "name": new_transport.name,
                    "license_plate": new_transport.license_plate,
                    "address": new_transport.address
                }
            }

        elif schema.access_type == "delivery":
            new_delivery = DeliveryGuy(
                name=schema.name,
                establishment=schema.establishment,
                address=schema.address,
                user=schema.user,
                dweller_id=self.dweller.id
            )
            self.session.add(new_delivery)

            response = {
                "message": f"Acesso liberado para entregador {new_delivery.name}",
                "delivery": {
                    "name": new_delivery.name,
                    "establishment": new_delivery.establishment,
                    "address": new_delivery.address
                }
            }

        elif schema.access_type == "guest":
            new_guest = Guest(
                name=schema.name,
                is_driving=schema.is_driving,
                address=schema.address,
                user=schema.user,
                dweller_id=self.dweller.id
            )
            self.session.add(new_guest)

            response = {
                "message": f"Acesso liberado para visitante {new_guest.name}",
                "guest": {
                    "name": new_guest.name,
                    "is_driving": new_guest.is_driving,
                    "address": new_guest.address
                }
            }

        else:
            raise HTTPException(status_code=400, detail="Tipo de acesso inválido")

        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail="Erro ao processar solicitação")

        self.mailNotice.update_admins(self.session)
        self.mailNotice.send_notices(response, "uber")

        return response
