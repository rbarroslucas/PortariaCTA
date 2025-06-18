from models import AccessBase, UberBuilder, DeliveryGuyBuilder, GuestBuilder
from schemas import AccessRequestSchema

class AccessFactory:
    @staticmethod
    def create_access(schema: AccessRequestSchema, dweller_id: int) -> AccessBase:
        if schema.access_type == "guest":
            builder = GuestBuilder()\
                .with_address(schema.address)\
                .with_user(schema.user)\
                .with_dweller_id(dweller_id)\
                .with_name(schema.name)\
                .with_is_driving(schema.is_driving)
            return builder.build()

        elif schema.access_type == "uber":
            builder = UberBuilder()\
                .with_address(schema.address)\
                .with_user(schema.user)\
                .with_dweller_id(dweller_id)\
                .with_name(schema.name)\
                .with_license_plate(schema.license_plate)
            return builder.build()

        elif schema.access_type == "delivery":
            builder = DeliveryGuyBuilder()\
                .with_address(schema.address)\
                .with_user(schema.user)\
                .with_dweller_id(dweller_id)\
                .with_name(schema.name)\
                .with_establishment(schema.establishment)
            return builder.build()

        else:
            raise ValueError(f"Tipo de acesso inexistente: {access_type}")
