# Safari Integrations Report Export System

This document explains how the report export system works for the Safari Integrations app and how to ensure your custom reports are exported when pushing to GitHub.

## Overview

The report export system consists of several components:

1. **Report Fixtures** (`report_fixtures.py`) - Defines all custom reports
2. **Install Script** (`setup/install.py`) - Installs report components during app installation
3. **Hooks Configuration** (`hooks.py`) - Configures fixtures for export
4. **Setup Scripts** (`utils/`) - Manual setup and verification scripts

## Files Created/Modified

### 1. Report Fixtures
- **File**: `safari_integrations/report_fixtures.py`
- **Purpose**: Defines all custom reports for export
- **Usage**: Automatically loaded during app installation

### 2. Updated Install Script
- **File**: `safari_integrations/setup/install.py`
- **Changes**: Added `install_report_fixtures()` function
- **Purpose**: Installs report components during app installation

### 3. Updated Hooks
- **File**: `safari_integrations/hooks.py`
- **Changes**: Added report components to fixtures list
- **Purpose**: Ensures reports are exported with the app

### 4. Setup Scripts
- **File**: `safari_integrations/utils/setup_all_reports.py`
- **Purpose**: Manual setup of all report components
- **File**: `safari_integrations/utils/verify_report_exports.py`
- **Purpose**: Verification and testing of export functionality

## How It Works

### 1. Automatic Export
When you push to GitHub, the following components are automatically exported:

- **Reports**: API Usage Analytics, API Cost Analysis, Provider Performance Report, etc.

### 2. Automatic Installation
When someone installs your app, the report components are automatically created:

```python
# This happens automatically during app installation
after_install = "safari_integrations.setup.install.after_install"
```

### 3. Fixtures Configuration
The `hooks.py` file includes report components in the fixtures list:

```python
fixtures = [
    # ... other fixtures ...
    {
        "doctype": "Report",
        "filters": [
            [
                "name",
                "in",
                [
                    "API Usage Analytics",
                    "API Cost Analysis",
                    "Provider Performance Report",
                    "Company API Access Report",
                    "API Quota Usage Report"
                ]
            ]
        ]
    }
]
```

## Reports Exported

### Safari Integrations Reports
- **API Usage Analytics**: Analytics report for API usage patterns
- **API Cost Analysis**: Cost analysis and reporting
- **Provider Performance Report**: Performance metrics for API providers
- **Company API Access Report**: Access control and permissions report
- **API Quota Usage Report**: Quota usage and monitoring report

## Usage

### 1. Manual Setup
To manually set up all report components:

```bash
# Run the setup script
bench --site safarierp console
```

```python
# In the console
from safari_integrations.utils.setup_all_reports import setup_all_reports
setup_all_reports()
```

### 2. Verification
To verify that all components are properly exported:

```bash
# Run the verification script
bench --site safarierp console
```

```python
# In the console
from safari_integrations.utils.verify_report_exports import verify_report_exports
verify_report_exports()
```

### 3. Manual Export
To manually export report components:

```bash
# Export Reports
bench --site safarierp export-doc "Report" "API Usage Analytics" safari_integrations/fixtures/
bench --site safarierp export-doc "Report" "API Cost Analysis" safari_integrations/fixtures/
bench --site safarierp export-doc "Report" "Provider Performance Report" safari_integrations/fixtures/
bench --site safarierp export-doc "Report" "Company API Access Report" safari_integrations/fixtures/
bench --site safarierp export-doc "Report" "API Quota Usage Report" safari_integrations/fixtures/
```

## Adding New Reports

### 1. Add to Report Fixtures
Edit `report_fixtures.py` and add your new report to the `get_reports()` function:

```python
def get_reports():
    return [
        # ... existing reports ...
        {
            "doctype": "Report",
            "name": "Your New Report",
            "report_name": "Your New Report",
            "module": "Safari Integrations",
            "is_standard": "Yes",
            "disabled": 0,
            "report_type": "Script Report",
            "ref_doctype": "Your Document Type",
            "query": "",
            "json": "{}",
            "roles": [
                {"role": "API Manager"},
                {"role": "System Manager"}
            ]
        }
    ]
```

### 2. Update Hooks
Add the new report to the fixtures list in `hooks.py`:

```python
fixtures = [
    # ... existing fixtures ...
    {
        "doctype": "Report",
        "filters": [
            [
                "name",
                "in",
                [
                    "API Usage Analytics",
                    "Your New Report",
                    # ... other reports
                ]
            ]
        ]
    }
]
```

### 3. Update Setup Scripts
Add the new report to the verification lists in the setup scripts.

## Report Types Supported

### 1. Script Reports
- **Type**: `Script Report`
- **Usage**: Custom Python scripts for complex reporting
- **Example**: API Usage Analytics, Cost Analysis

### 2. Query Reports
- **Type**: `Query Report`
- **Usage**: SQL-based reports
- **Example**: Simple data queries

### 3. Report Builder Reports
- **Type**: `Report Builder`
- **Usage**: Drag-and-drop report builder
- **Example**: Simple table reports

## Report Permissions

### Default Roles
All reports are configured with these default roles:
- **API Manager**: Primary role for API management
- **System Manager**: Administrative access

### Customizing Permissions
To customize report permissions, modify the `roles` field in the report fixture:

```python
"roles": [
    {"role": "API Manager"},
    {"role": "System Manager"},
    {"role": "Your Custom Role"}
]
```

## Testing

### 1. Test Installation
```bash
# Install the app in a test environment
bench --site test-site install-app safari_integrations
```

### 2. Test Export
```bash
# Export the app and check if report components are included
bench --site test-site export-app safari_integrations
```

### 3. Test Import
```bash
# Import the app in another environment and verify reports exist
bench --site another-site import-app safari_integrations
```

## Troubleshooting

### 1. Reports Not Exported
- Check that reports are listed in `hooks.py` fixtures
- Verify reports exist in the database
- Check for any errors in the install script

### 2. Reports Not Installed
- Check the `after_install` hook is properly configured
- Verify the report fixtures file is accessible
- Check for any errors during installation

### 3. Missing Dependencies
- Ensure all required doctypes exist
- Check that module names are correct
- Verify document types referenced in reports exist

### 4. Permission Issues
- Ensure required roles exist
- Check role permissions are properly set
- Verify user has appropriate role assignments

## Best Practices

1. **Always test** your report components before pushing to GitHub
2. **Use descriptive names** for your reports
3. **Include proper documentation** for complex reports
4. **Version control** your report fixtures along with your code
5. **Test installation** in a clean environment before releasing
6. **Set appropriate permissions** for each report
7. **Use standard report types** when possible

## Extending to Other Apps

To implement the same system for other Safari apps:

1. **Create Report Fixtures**: Copy `report_fixtures.py` to the other app
2. **Update Install Script**: Add report installation to the app's `setup/install.py`
3. **Update Hooks**: Add report fixtures to the app's `hooks.py`
4. **Create Setup Scripts**: Copy setup and verification scripts to the app's `utils/` directory

## Report Structure

### Required Fields
```python
{
    "doctype": "Report",
    "name": "Report Name",
    "report_name": "Report Display Name",
    "module": "Module Name",
    "is_standard": "Yes",
    "disabled": 0,
    "report_type": "Script Report",
    "ref_doctype": "Reference Document Type",
    "query": "",
    "json": "{}",
    "roles": [
        {"role": "Role Name"}
    ]
}
```

### Optional Fields
```python
{
    "add_total_row": 1,
    "disable_prepared_report": 0,
    "letter_head": "",
    "prepared_report": 0
}
```

This ensures all your custom report components are properly exported and can be reinstalled on other systems. 