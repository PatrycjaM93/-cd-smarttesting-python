from loan_orders.customer.customer import Customer
from loan_orders.repositories.base import MongoRepository


class CustomerRepository(MongoRepository[Customer]):
    _collection_name = "customers"
