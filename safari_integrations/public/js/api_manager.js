// API Manager JavaScript utilities
frappe.provide("safari_integrations.api");

safari_integrations.api = {
    call_api: function(provider, endpoint, method, data, callback) {
        frappe.call({
            method: "safari_integrations.utils.api_manager.call_external_api",
            args: {
                provider: provider,
                endpoint: endpoint,
                method: method || "GET",
                data: data || {}
            },
            callback: callback,
            freeze: true,
            freeze_message: __("Calling external API...")
        });
    },

    check_quota: function(provider, callback) {
        frappe.call({
            method: "safari_integrations.utils.usage_tracker.check_remaining_quota",
            args: {
                provider: provider
            },
            callback: callback
        });
    }
};