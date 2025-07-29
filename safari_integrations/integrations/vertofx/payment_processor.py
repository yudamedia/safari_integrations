# safari_integrations/integrations/vertofx/payment_processor.py

class VertoFxPaymentProcessor:
    def __init__(self, safari_company):
        self.api_manager = SafariAPIManager(safari_company)
        
    def get_exchange_rates(self, base_currency="USD", target_currencies=["KES", "EUR", "GBP"]):
        """Get real-time exchange rates."""
        
        return self.api_manager.call_api(
            provider="VertoFx",
            endpoint="rates",
            data={"base": base_currency, "symbols": ",".join(target_currencies)}
        )
        
    def create_payment_intent(self, amount, currency, customer_details):
        """Create payment intent for booking."""
        
        payment_data = {
            "amount": amount,
            "currency": currency,
            "customer": customer_details,
            "metadata": {"source": "safari_erp"}
        }
        
        return self.api_manager.call_api(
            provider="VertoFx",
            endpoint="payment-intents",
            method="POST",
            data=payment_data
        )