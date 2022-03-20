import requests
from loan_orders.customer.customer import Customer
from loan_orders.fraud.customer_verification_result import CustomerVerificationResult
from loan_orders.fraud.schemas import CustomerSchema, CustomerVerificationResultSchema


def verify_customer(customer: Customer) -> CustomerVerificationResult:
    input_schema = CustomerSchema()
    input_json = input_schema.dump(customer)

    response = requests.post("http://localhost:9090/customers/verify", json=input_json)
    response.raise_for_status()

    result_schema = CustomerVerificationResultSchema()
    return result_schema.load(response.json())
