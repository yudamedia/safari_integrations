import frappe
from frappe import _
from frappe.utils import now_datetime, add_to_date
import json

def reset_hourly_limits():
    """Reset hourly rate limits for all API providers - called by scheduler"""
    try:
        # Clear expired rate limit entries from cache
        frappe.cache().delete_keys("api_rate_limit:*")
        
        # Log the reset
        frappe.logger().info("Hourly API rate limits reset successfully")
        
    except Exception as e:
        frappe.log_error(f"Error resetting hourly limits: {str(e)}", "Rate Limiter Error")

def check_rate_limit(safari_company, api_provider):
    """Check if API call is within rate limits"""
    try:
        # Get provider rate limits
        provider = frappe.get_doc("API Provider", api_provider)
        rate_limit = provider.rate_limit_per_minute or 100
        
        # Create cache key
        cache_key = f"api_rate_limit:{safari_company}:{api_provider}"
        current_minute = now_datetime().strftime("%Y-%m-%d %H:%M")
        minute_key = f"{cache_key}:{current_minute}"
        
        # Get current minute's usage
        current_usage = frappe.cache().get(minute_key) or 0
        
        if current_usage >= rate_limit:
            return {
                "allowed": False,
                "remaining": 0,
                "reset_time": add_to_date(now_datetime(), minutes=1)
            }
        
        # Increment usage
        frappe.cache().set(minute_key, current_usage + 1, expires_in_sec=60)
        
        return {
            "allowed": True,
            "remaining": rate_limit - current_usage - 1,
            "reset_time": add_to_date(now_datetime(), minutes=1)
        }
        
    except Exception as e:
        frappe.log_error(f"Error checking rate limit: {str(e)}", "Rate Limiter Error")
        # Default to allow if there's an error
        return {"allowed": True, "remaining": 100, "reset_time": now_datetime()}

def get_rate_limit_status(safari_company, api_provider):
    """Get current rate limit status for display"""
    try:
        provider = frappe.get_doc("API Provider", api_provider)
        rate_limit = provider.rate_limit_per_minute or 100
        
        cache_key = f"api_rate_limit:{safari_company}:{api_provider}"
        current_minute = now_datetime().strftime("%Y-%m-%d %H:%M")
        minute_key = f"{cache_key}:{current_minute}"
        
        current_usage = frappe.cache().get(minute_key) or 0
        
        return {
            "rate_limit": rate_limit,
            "current_usage": current_usage,
            "remaining": max(0, rate_limit - current_usage),
            "percentage_used": (current_usage / rate_limit) * 100 if rate_limit > 0 else 0
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting rate limit status: {str(e)}")
        return {"rate_limit": 0, "current_usage": 0, "remaining": 0, "percentage_used": 0}

@frappe.whitelist()
def get_company_rate_limits(safari_company):
    """Get rate limit status for all APIs accessible by a company"""
    try:
        api_accesses = frappe.get_all("Company API Access", 
            filters={"safari_company": safari_company, "is_active": 1},
            fields=["api_provider"]
        )
        
        rate_limits = []
        for access in api_accesses:
            status = get_rate_limit_status(safari_company, access.api_provider)
            status["api_provider"] = access.api_provider
            rate_limits.append(status)
            
        return rate_limits
        
    except Exception as e:
        frappe.log_error(f"Error getting company rate limits: {str(e)}")
        return []