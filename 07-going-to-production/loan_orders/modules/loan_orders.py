import injector

from loan_orders.order.loan_order_service import LoanOrderService
from loan_orders.repositories.loan_order_repository import LoanOrderRepository


class LoanOrdersModule(injector.Module):
    @injector.provider
    def loan_order_service(self, repo: LoanOrderRepository) -> LoanOrderService:
        return LoanOrderService(repo)
