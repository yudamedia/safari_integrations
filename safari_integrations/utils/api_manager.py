# safari_integrations/utils/api_manager.py

import frappe
from frappe import _
import requests
import json
from datetime import datetime, timedelta

class SafariAPIManager:
    def __init__(self, safari_company):
        self.safari_company = safari_company
        self.session = requests.Session()
        
    def call_api(self, provider, endpoint, method="GET", data=None, **kwargs):
        """Central API calling method with logging and cost tracking."""
        
        # Check company access permissions
        access = self.get_company_access(provider)
        if not access or not access.is_active:
            frappe.throw(_("No access to {0} API").format(provider))
            
        # Check usage quotas
        if not self.check_quota(provider):
            frappe.throw(_("API quota exceeded for {0}").format(provider))
            
        # Get API credentials
        credentials = self.get_api_credentials(provider)
        
        # Make API call
        start_time = datetime.now()
        try:
            response = self.execute_request(provider, endpoint, method, data, credentials, **kwargs)
            
            # Log successful usage
            self.log_api_usage(provider, endpoint, method, response, start_time)
            
            return response.json()
            
        except Exception as e:
            # Log failed usage
            self.log_api_usage(provider, endpoint, method, None, start_time, error=str(e))
            raise
            
    def execute_request(self, provider, endpoint, method, data, credentials, **kwargs):
        """Execute the actual API request with proper authentication."""
        
        provider_config = frappe.get_doc("API Provider", provider)
        url = f"{provider_config.base_url}/{endpoint}"
        
        headers = self.build_headers(provider_config, credentials)
        
        if method == "GET":
            response = self.session.get(url, headers=headers, params=data, **kwargs)
        elif method == "POST":
            response = self.session.post(url, headers=headers, json=data, **kwargs)
        
        response.raise_for_status()
        return response
        
    def get_company_access(self, provider):
        """Get company's access configuration for API provider."""
        return frappe.get_doc("Company API Access", {
            "safari_company": self.safari_company,
            "api_provider": provider
        })
        
    def check_quota(self, provider):
        """Check if company has remaining quota for this API."""
        access = self.get_company_access(provider)
        
        # Get current month usage
        usage_count = frappe.db.count("API Usage Log", {
            "safari_company": self.safari_company,
            "api_provider": provider,
            "creation": [">=", frappe.utils.get_first_day(frappe.utils.today())]
        })
        
        return usage_count < access.monthly_quota
        
    def log_api_usage(self, provider, endpoint, method, response, start_time, error=None):
        """Log API usage for tracking and billing."""
        
        end_time = datetime.now()
        response_time = int((end_time - start_time).total_seconds() * 1000)
        
        # Calculate cost
        provider_config = frappe.get_doc("API Provider", provider)
        cost = provider_config.cost_per_request or 0
        
        usage_log = frappe.get_doc({
            "doctype": "API Usage Log",
            "safari_company": self.safari_company,
            "api_provider": provider,
            "endpoint": endpoint,
            "request_method": method,
            "response_status": response.status_code if response else 0,
            "response_time_ms": response_time,
            "cost_incurred": cost,
            "user": frappe.session.user,
            "error_message": error
        })
        
        usage_log.insert(ignore_permissions=True)
        
    def get_api_credentials(self, provider):
        """Get encrypted API credentials for provider."""
        
        credentials = frappe.get_doc("API Credential", {
            "api_provider": provider
        })
        
        if not credentials:
            frappe.throw(_("No credentials found for {0}").format(provider))
            
        return credentials
        
    def build_headers(self, provider_config, credentials):
        """Build request headers based on provider configuration."""
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "SafariERP/1.0"
        }
        
        # Handle different authentication methods
        auth_method = provider_config.auth_type
        
        if auth_method == "Bearer Token":
            # For OAuth2 providers like Amadeus
            token = self.get_access_token(provider_config, credentials)
            headers["Authorization"] = f"Bearer {token}"
            
        elif auth_method == "API Key":
            # Direct API key authentication
            api_key = credentials.get_password("api_key")
            headers[provider_config.api_key_header or "X-API-Key"] = api_key
            
        elif auth_method == "Basic Auth":
            # Basic authentication
            import base64
            api_key = credentials.get_password("api_key")
            api_secret = credentials.get_password("api_secret")
            credentials_str = f"{api_key}:{api_secret}"
            encoded = base64.b64encode(credentials_str.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
            
        return headers
        
    def get_access_token(self, provider_config, credentials):
        """Get OAuth2 access token for providers like Amadeus."""
        
        # Check if we have a cached valid token
        cache_key = f"api_token_{provider_config.name}"
        cached_token = frappe.cache().get_value(cache_key)
        
        if cached_token:
            return cached_token
            
        # Get new token
        token_url = provider_config.token_endpoint
        api_key = credentials.get_password("api_key")
        api_secret = credentials.get_password("api_secret")
        
        token_data = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": api_secret
        }
        
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        
        token_response = response.json()
        access_token = token_response.get("access_token")
        expires_in = token_response.get("expires_in", 3600)
        
        # Cache token for 90% of its lifetime
        cache_duration = int(expires_in * 0.9)
        frappe.cache().set_value(cache_key, access_token, expires_in_sec=cache_duration)
        
        return access_token