import marshmallow
import marshmallow_dataclass
from e2e.smarttesting.customer.customer import Customer
from e2e.smarttesting.order.loan_order import LoanOrder
from marshmallow.fields import Field


class PrivateFieldsCapableSchema(marshmallow.Schema):
    def on_bind_field(self, field_name: str, field_obj: Field) -> None:
        # Dataclasses (w przeciwieństwie do attrs) nie aliasują prywatnych pól
        # w __init__, więc żeby API nie wymagało podawania pól w formacie "_uuid",
        # aliasujemy je usuwając podkreślnik
        field_obj.data_key = field_name.lstrip("_")


CustomerSchema = marshmallow_dataclass.class_schema(
    Customer, base_schema=PrivateFieldsCapableSchema
)


LoanOrderSchema = marshmallow_dataclass.class_schema(
    LoanOrder, base_schema=PrivateFieldsCapableSchema
)
