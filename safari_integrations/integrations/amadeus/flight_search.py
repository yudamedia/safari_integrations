# ~/frappe-bench/apps/safari_integrations/safari_integrations/integrations/amadeus/flight_search.py

from safari_integrations.utils.api_manager import SafariAPIManager

class AmadeusFlightSearch:
    def __init__(self, safari_company):
        self.api_manager = SafariAPIManager(safari_company)
        
    def search_flights(self, origin, destination, departure_date, return_date=None, passengers=1):
        """Search for flights using Amadeus API."""
        
        search_params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": passengers
        }
        
        if return_date:
            search_params["returnDate"] = return_date
            
        return self.api_manager.call_api(
            provider="Amadeus",
            endpoint="shopping/flight-offers",
            method="GET",
            data=search_params
        )
        
    def get_hotel_offers(self, city_code, check_in, check_out, guests=1):
        """Search for hotel offers using Amadeus API."""
        
        search_params = {
            "cityCode": city_code,
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "roomQuantity": 1,
            "adults": guests
        }
        
        return self.api_manager.call_api(
            provider="Amadeus",
            endpoint="shopping/hotel-offers",
            method="GET", 
            data=search_params
        )
