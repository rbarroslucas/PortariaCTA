from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.dependencies import verify_token, get_session
from models import Dweller, Uber, DeliveryGuy
from schemas import UberSchema, DeliverySchema

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verify_token)])

@order_router.post("/request-uber-access")
async def request_uber_acces(uber_schema: UberSchema, dweller: Dweller = Depends(verify_token), session: Session = Depends(get_session)):
    if not dweller.id == uber_schema.dweller_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_uber = Uber(uber_schema.name, uber_schema.license_plate, uber_schema.address, uber_schema.user, uber_schema.dweller_id)
    session.add(new_uber)
    session.commit()
    return {
        "Message" : f"Access granted for Uber driver {new_uber.name}.",
        "Uber" : new_uber
    }

@order_router.post("/request-delivery-access")
async def request_delivery_access(delivery_schema: DeliverySchema, dweller: Dweller = Depends(verify_token), session: Session = Depends(get_session)):
    if not dweller.id == delivery_schema.dweller_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_delivery = DeliveryGuy(delivery_schema.name, delivery_schema.establishment, delivery_schema.address, delivery_schema.user, delivery_schema.dweller_id)
    session.add(new_delivery)
    session.commit()
    return {
        "Message" : f"Access granted for Delivery Guy {new_delivery.name}.",
        "Delivery" : new_delivery
    }