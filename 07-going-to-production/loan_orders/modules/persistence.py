import injector
import pymongo
from pymongo.database import Database

from loan_orders.repositories.loan_order_repository import LoanOrderRepository


class PersistenceModule(injector.Module):
    @injector.singleton
    @injector.provider
    def database(self) -> Database:
        client = pymongo.MongoClient("mongodb://mongo:27017/")
        return client.get_database("loanordersdb")

    @injector.provider
    def loan_orders_repo(self, database: Database) -> LoanOrderRepository:
        return LoanOrderRepository(database)
