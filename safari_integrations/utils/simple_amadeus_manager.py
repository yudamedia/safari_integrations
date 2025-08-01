# Simple API Manager for Amadeus
import frappe
import requests
from datetime import datetime, timedelta

class SimpleAmadeusManager:
    def __init__(self, safari_company):
        self.safari_company = safari_company
        self.cache_duration = 1800  # 30 minutes
        
    def get_access_token(self):
        """Get OAuth access token for Amadeus"""
        
        # Check cache first
        cache_key = "amadeus_token"
        cached_token = frappe.cache().get_value(cache_key)
        
        if cached_token:
            return cached_token
        
        # Get credentials
        try:
            access_doc = frappe.get_doc("Company API Access", f"{self.safari_company}-Amadeus")
            
            api_key = None
            api_secret = None
            
            for cred in access_doc.api_credentials:
                if cred.credential_type == "Client ID":
                    api_key = cred.get_password("credential_value")
                elif cred.credential_type == "Client Secret":
                    api_secret = cred.get_password("credential_value")
            
            if not api_key or not api_secret:
                frappe.throw("Missing Amadeus credentials")
            
            # Get token
            token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            token_data = {
                "grant_type": "client_credentials",
                "client_id": api_key,
                "client_secret": api_secret
            }
            
            response = requests.post(token_url, data=token_data, timeout=30)
            
            if response.status_code == 200:
                token_response = response.json()
                access_token = token_response.get('access_token')
                expires_in = token_response.get('expires_in', 1800)
                
                # Cache token for 90% of its lifetime
                cache_duration = int(expires_in * 0.9)
                frappe.cache().set_value(cache_key, access_token, expires_in_sec=cache_duration)
                
                return access_token
            else:
                frappe.throw(f"Token request failed: {response.status_code}")
                
        except Exception as e:
            frappe.throw(f"Error getting token: {str(e)}")
    
    def search_flights(self, origin, destination, departure_date, return_date=None, passengers=1):
        """Search for flights using Amadeus API"""
        
        try:
            access_token = self.get_access_token()
            
            search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            params = {
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departure_date,
                "adults": passengers,
                "max": 10
            }
            
            if return_date:
                params["returnDate"] = return_date
            
            response = requests.get(search_url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                frappe.throw(f"Flight search failed: {response.status_code}")
                
        except Exception as e:
            frappe.throw(f"Error searching flights: {str(e)}")
