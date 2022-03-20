import marshmallow
import marshmallow_dataclass
from loan_orders.order.loan_order import LoanOrder
from marshmallow.fields import Field


class PrivateFieldsCapableSchema(marshmallow.Schema):
    def on_bind_field(self, field_name: str, field_obj: Field) -> None:
        # Dataclasses (w przeciwieństwie do attrs) nie aliasują prywatnych pól
        # w __init__, więc żeby API nie wymagało podawania pól w formacie "_uuid",
        # aliasujemy je usuwając podkreślnik
        field_obj.data_key = field_name.lstrip("_")


LoanOrderSchema = marshmallow_dataclass.class_schema(
    LoanOrder, base_schema=PrivateFieldsCapableSchema
)
