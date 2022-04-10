import marshmallow
import marshmallow_dataclass
from marshmallow.fields import Field

from fraud_verifier.customer.customer import Customer
from fraud_verifier.customer.customer_verification_result import (
    CustomerVerificationResult,
)


class PrivateFieldsCapableSchema(marshmallow.Schema):
    def on_bind_field(self, field_name: str, field_obj: Field) -> None:
        # Dataclasses (w przeciwieństwie do attrs) nie aliasują prywatnych pól
        # w __init__, więc żeby API nie wymagało podawania pól w formacie "_uuid",
        # aliasujemy je usuwając podkreślnik
        field_obj.data_key = field_name.lstrip("_")


CustomerSchema = marshmallow_dataclass.class_schema(
    Customer, base_schema=PrivateFieldsCapableSchema
)

CustomerVerificationResultSchema = marshmallow_dataclass.class_schema(
    CustomerVerificationResult, base_schema=PrivateFieldsCapableSchema
)
