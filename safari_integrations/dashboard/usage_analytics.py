# safari_integrations/dashboard/usage_analytics.py

@frappe.whitelist()
def get_api_usage_analytics(safari_company, period="monthly"):
    """Get comprehensive API usage analytics."""
    
    date_filter = get_date_filter(period)
    
    usage_data = frappe.db.sql("""
        SELECT 
            api_provider,
            COUNT(*) as total_calls,
            SUM(cost_incurred) as total_cost,
            AVG(response_time_ms) as avg_response_time,
            COUNT(CASE WHEN response_status >= 400 THEN 1 END) as error_count
        FROM `tabAPI Usage Log`
        WHERE safari_company = %s 
        AND creation >= %s
        GROUP BY api_provider
    """, (safari_company, date_filter), as_dict=True)
    
    return {
        "usage_summary": usage_data,
        "cost_trend": get_cost_trend(safari_company, period),
        "quota_status": get_quota_status(safari_company),
        "performance_metrics": get_performance_metrics(safari_company, period)
    }