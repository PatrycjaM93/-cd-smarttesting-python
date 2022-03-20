from loan_orders.order.loan_order import LoanOrder
from loan_orders.repositories.base import MongoRepository


class LoanOrderRepository(MongoRepository[LoanOrder]):
    _collection_name = "loan_orders"
