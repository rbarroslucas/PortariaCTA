from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from config.dependencies import verify_token, get_session
from models import Dweller, Uber, DeliveryGuy
from schemas import UberSchema, DeliverySchema
from utils.utils import Validator, PlateValidation

router = InferringRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

@cbv(router)
class OrderView:
    session: Session = Depends(get_session)
    dweller: Dweller = Depends(verify_token)

    @router.post("/get-admin")
    async def get_admin(self):
        admins = self.session.query(Dweller).filter(Dweller.admin == True)
        dic = {}
        for admin in admins:
            dic.update({"admin_{}".format(admin.id): {
                "name": admin.name,
                "email": admin.email,
                "cpf": admin.cpf,
                "id": admin.id
            }})
        return dic

    @router.post("/request-uber-access")
    async def request_uber_access(self, uber_schema: UberSchema):
        validator = Validator(PlateValidation)

        new_uber = Uber(
            name=uber_schema.name,
            license_plate=uber_schema.license_plate,
            address=uber_schema.address,
            user=uber_schema.user,
            dweller_id=self.dweller.id
        )
        
        if not validator.perform_validation(uber_schema.license_plate):
            raise HTTPException(status_code=400, detail="Placa inválido")

        self.session.add(new_uber)
        self.session.commit()
        return {
            "message": f"Acesso liberado para Uber {new_uber.name}",
            "uber": {
                "name": new_uber.name,
                "license_plate": new_uber.license_plate,
                "address": new_uber.address
            }
        }

    @router.post("/request-delivery-access")
    async def request_delivery_access(self, delivery_schema: DeliverySchema):
        new_delivery = DeliveryGuy(
            name=delivery_schema.name,
            establishment=delivery_schema.establishment,
            address=delivery_schema.address,
            user=delivery_schema.user,
            dweller_id=self.dweller.id
        )
        self.session.add(new_delivery)
        self.session.commit()
        return {
            "message": f"Acesso liberado para {new_delivery.name}",
            "delivery": {
                "name": new_delivery.name,
                "establishment": new_delivery.establishment,
                "address": new_delivery.address
            }
        }
