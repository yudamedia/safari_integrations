import frappe
from frappe import _
from frappe.utils import today, get_first_day, get_last_day, flt, add_days
from datetime import datetime, timedelta

def calculate_daily_costs():
    """Calculate daily API costs for all companies - called by scheduler"""
    try:
        yesterday = add_days(today(), -1)
        
        # Get all API usage from yesterday
        usage_logs = frappe.get_all("API Usage Log",
            filters={"creation": ["between", [yesterday, today()]]},
            fields=["safari_company", "api_provider", "cost_incurred"]
        )
        
        # Group by company and provider
        company_costs = {}
        for log in usage_logs:
            company = log.safari_company
            provider = log.api_provider
            cost = flt(log.cost_incurred)
            
            if company not in company_costs:
                company_costs[company] = {}
            if provider not in company_costs[company]:
                company_costs[company][provider] = 0
                
            company_costs[company][provider] += cost
        
        # Create daily cost summary records
        for company, providers in company_costs.items():
            total_daily_cost = sum(providers.values())
            
            # Log daily summary
            frappe.logger().info(f"Daily API costs for {company}: ${total_daily_cost:.4f}")
            
            # Check if daily costs exceed any thresholds
            check_daily_cost_alerts(company, total_daily_cost, providers)
            
        frappe.logger().info("Daily cost calculation completed successfully")
        
    except Exception as e:
        frappe.log_error(f"Error calculating daily costs: {str(e)}", "Cost Calculator Error")

def check_daily_cost_alerts(safari_company, total_cost, provider_costs):
    """Check if daily costs trigger any alerts"""
    try:
        # Get company's cost alert thresholds (you can customize this)
        daily_cost_threshold = 50.0  # $50 daily threshold
        
        if total_cost > daily_cost_threshold:
            # Send alert
            frappe.log_error(
                f"Daily cost alert: {safari_company} spent ${total_cost:.2f} on {today()}",
                "High Daily API Costs"
            )
            
            # You can add email notification here
            send_cost_alert_email(safari_company, total_cost, provider_costs)
            
    except Exception as e:
        frappe.log_error(f"Error checking cost alerts: {str(e)}")

def send_cost_alert_email(safari_company, total_cost, provider_costs):
    """Send cost alert email to company administrators"""
    try:
        # Get company admin emails
        company_doc = frappe.get_doc("Safari Company", safari_company)
        recipients = [company_doc.email] if hasattr(company_doc, 'email') and company_doc.email else []
        
        if not recipients:
            return
            
        # Prepare cost breakdown
        cost_breakdown = "\n".join([f"  {provider}: ${cost:.2f}" for provider, cost in provider_costs.items()])
        
        subject = f"Daily API Cost Alert - {safari_company}"
        message = f"""
        <h3>Daily API Cost Alert</h3>
        <p>Your API usage costs for {today()} have exceeded the daily threshold.</p>
        
        <p><strong>Total Daily Cost: ${total_cost:.2f}</strong></p>
        
        <h4>Cost Breakdown by Provider:</h4>
        <pre>{cost_breakdown}</pre>
        
        <p>Please review your API usage and consider optimizing calls if necessary.</p>
        """
        
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message
        )
        
    except Exception as e:
        frappe.log_error(f"Error sending cost alert email: {str(e)}")

@frappe.whitelist()
def get_monthly_cost_summary(safari_company, month=None, year=None):
    """Get monthly cost summary for a company"""
    try:
        if not month:
            month = datetime.now().month
        if not year:
            year = datetime.now().year
            
        # Get first and last day of month
        first_day = get_first_day(f"{year}-{month:02d}-01")
        last_day = get_last_day(f"{year}-{month:02d}-01")
        
        # Get usage logs for the month
        usage_logs = frappe.db.sql("""
            SELECT 
                api_provider,
                COUNT(*) as total_calls,
                SUM(cost_incurred) as total_cost,
                AVG(response_time_ms) as avg_response_time
            FROM `tabAPI Usage Log`
            WHERE safari_company = %s
            AND DATE(creation) BETWEEN %s AND %s
            GROUP BY api_provider
        """, (safari_company, first_day, last_day), as_dict=True)
        
        total_monthly_cost = sum(flt(log.total_cost) for log in usage_logs)
        
        return {
            "month": month,
            "year": year,
            "total_cost": total_monthly_cost,
            "provider_breakdown": usage_logs,
            "period": f"{first_day} to {last_day}"
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting monthly cost summary: {str(e)}")
        return {"total_cost": 0, "provider_breakdown": [], "error": str(e)}

@frappe.whitelist()
def get_cost_trends(safari_company, days=30):
    """Get cost trends over specified number of days"""
    try:
        end_date = today()
        start_date = add_days(end_date, -days)
        
        daily_costs = frappe.db.sql("""
            SELECT 
                DATE(creation) as date,
                SUM(cost_incurred) as daily_cost,
                COUNT(*) as daily_calls
            FROM `tabAPI Usage Log`
            WHERE safari_company = %s
            AND DATE(creation) BETWEEN %s AND %s
            GROUP BY DATE(creation)
            ORDER BY DATE(creation)
        """, (safari_company, start_date, end_date), as_dict=True)
        
        return {
            "period_days": days,
            "start_date": start_date,
            "end_date": end_date,
            "daily_trends": daily_costs,
            "total_period_cost": sum(flt(day.daily_cost) for day in daily_costs),
            "total_period_calls": sum(day.daily_calls for day in daily_costs)
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting cost trends: {str(e)}")
        return {"daily_trends": [], "total_period_cost": 0, "error": str(e)}

def format_api_cost(amount, currency="USD"):
    """Format API cost for display"""
    try:
        return f"{currency} {flt(amount, 4):.4f}"
    except:
        return f"{currency} 0.0000"