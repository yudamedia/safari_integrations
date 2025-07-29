# Copyright (c) 2024, Safari ERP and Contributors
# License: MIT

import json
import frappe
from frappe import _

def get_data():
    return frappe._dict({
        "reports": get_reports(),
    })

def get_reports():
    return [
        {
            "doctype": "Report",
            "name": "API Usage Analytics",
            "report_name": "API Usage Analytics",
            "module": "Safari Integrations",
            "is_standard": "Yes",
            "disabled": 0,
            "report_type": "Script Report",
            "ref_doctype": "API Usage Log",
            "query": "",
            "json": "{}",
            "roles": [
                {"role": "API Manager"},
                {"role": "System Manager"}
            ]
        },
        {
            "doctype": "Report",
            "name": "API Cost Analysis",
            "report_name": "API Cost Analysis",
            "module": "Safari Integrations",
            "is_standard": "Yes",
            "disabled": 0,
            "report_type": "Script Report",
            "ref_doctype": "API Usage Log",
            "query": "",
            "json": "{}",
            "roles": [
                {"role": "API Manager"},
                {"role": "System Manager"}
            ]
        },
        {
            "doctype": "Report",
            "name": "Provider Performance Report",
            "report_name": "Provider Performance Report",
            "module": "Safari Integrations",
            "is_standard": "Yes",
            "disabled": 0,
            "report_type": "Script Report",
            "ref_doctype": "API Provider",
            "query": "",
            "json": "{}",
            "roles": [
                {"role": "API Manager"},
                {"role": "System Manager"}
            ]
        },
        {
            "doctype": "Report",
            "name": "Company API Access Report",
            "report_name": "Company API Access Report",
            "module": "Safari Integrations",
            "is_standard": "Yes",
            "disabled": 0,
            "report_type": "Script Report",
            "ref_doctype": "Company API Access",
            "query": "",
            "json": "{}",
            "roles": [
                {"role": "API Manager"},
                {"role": "System Manager"}
            ]
        },
        {
            "doctype": "Report",
            "name": "API Quota Usage Report",
            "report_name": "API Quota Usage Report",
            "module": "Safari Integrations",
            "is_standard": "Yes",
            "disabled": 0,
            "report_type": "Script Report",
            "ref_doctype": "API Usage Log",
            "query": "",
            "json": "{}",
            "roles": [
                {"role": "API Manager"},
                {"role": "System Manager"}
            ]
        }
    ] 