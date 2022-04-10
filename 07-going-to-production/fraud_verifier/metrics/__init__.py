from prometheus_client import Summary

verify_customer_timer = Summary("verifyCustomerTimer", "Time spent verifying customers")
