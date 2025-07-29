# Safari Integrations Dashboard Export System

This document explains how the dashboard export system works for the Safari Integrations app and how to ensure your custom number cards and dashboards are exported when pushing to GitHub.

## Overview

The dashboard export system consists of several components:

1. **Dashboard Fixtures** (`dashboard_fixtures.py`) - Defines all dashboard components
2. **Install Script** (`setup/install.py`) - Installs dashboard components during app installation
3. **Hooks Configuration** (`hooks.py`) - Configures fixtures for export
4. **Setup Scripts** (`utils/`) - Manual setup and verification scripts

## Files Created/Modified

### 1. Dashboard Fixtures
- **File**: `safari_integrations/dashboard_fixtures.py`
- **Purpose**: Defines all number cards, dashboard charts, and dashboards
- **Usage**: Automatically loaded during app installation

### 2. Updated Install Script
- **File**: `safari_integrations/setup/install.py`
- **Changes**: Added `after_install()` and `install_dashboard_fixtures()` functions
- **Purpose**: Installs dashboard components during app installation

### 3. Updated Hooks
- **File**: `safari_integrations/hooks.py`
- **Changes**: Added dashboard components to fixtures list
- **Purpose**: Ensures components are exported with the app

### 4. Setup Scripts
- **File**: `safari_integrations/utils/setup_all_dashboards.py`
- **Purpose**: Manual setup of all dashboard components
- **File**: `safari_integrations/utils/verify_exports.py`
- **Purpose**: Verification and testing of export functionality

## How It Works

### 1. Automatic Export
When you push to GitHub, the following components are automatically exported:

- **Number Cards**: Active API Providers, Total API Calls Today, Monthly API Costs, etc.
- **Dashboard Charts**: API Usage Trends, Cost by Provider, Monthly Quota Usage, etc.
- **Dashboards**: Integrations Management dashboard

### 2. Automatic Installation
When someone installs your app, the dashboard components are automatically created:

```python
# This happens automatically during app installation
after_install = "safari_integrations.setup.install.after_install"
```

### 3. Fixtures Configuration
The `hooks.py` file includes dashboard components in the fixtures list:

```python
fixtures = [
    # ... other fixtures ...
    {
        "doctype": "Number Card",
        "filters": [
            ["name", "in", ["Active API Providers", "Total API Calls Today", ...]]
        ]
    },
    {
        "doctype": "Dashboard Chart", 
        "filters": [
            ["name", "in", ["API Usage Trends", "Cost by Provider", ...]]
        ]
    },
    {
        "doctype": "Dashboard",
        "filters": [["name", "=", "Integrations Management"]]
    }
]
```

## Usage

### 1. Manual Setup
To manually set up all dashboard components:

```bash
# Run the setup script
bench --site safarierp console
```

```python
# In the console
from safari_integrations.utils.setup_all_dashboards import setup_all_dashboards
setup_all_dashboards()
```

### 2. Verification
To verify that all components are properly exported:

```bash
# Run the verification script
bench --site safarierp console
```

```python
# In the console
from safari_integrations.utils.verify_exports import verify_dashboard_exports
verify_dashboard_exports()
```

### 3. Manual Export
To manually export dashboard components:

```bash
# Export Number Cards
bench --site safarierp export-doc "Number Card" "Active API Providers" safari_integrations/fixtures/

# Export Dashboard Charts
bench --site safarierp export-doc "Dashboard Chart" "API Usage Trends" safari_integrations/fixtures/

# Export Dashboards
bench --site safarierp export-doc "Dashboard" "Integrations Management" safari_integrations/fixtures/
```

## Adding New Components

### 1. Add to Dashboard Fixtures
Edit `dashboard_fixtures.py` and add your new component to the appropriate function:

```python
def get_number_cards():
    return [
        # ... existing cards ...
        {
            "doctype": "Number Card",
            "name": "Your New Card",
            "label": "Your New Card",
            # ... other properties ...
        }
    ]
```

### 2. Update Hooks
Add the new component to the fixtures list in `hooks.py`:

```python
fixtures = [
    # ... existing fixtures ...
    {
        "doctype": "Number Card",
        "filters": [
            ["name", "in", ["Active API Providers", "Your New Card", ...]]
        ]
    }
]
```

### 3. Update Setup Scripts
Add the new component to the verification lists in the setup scripts.

## Testing

### 1. Test Installation
```bash
# Install the app in a test environment
bench --site test-site install-app safari_integrations
```

### 2. Test Export
```bash
# Export the app and check if dashboard components are included
bench --site test-site export-app safari_integrations
```

### 3. Test Import
```bash
# Import the app in another environment and verify components exist
bench --site another-site import-app safari_integrations
```

## Troubleshooting

### 1. Components Not Exported
- Check that components are listed in `hooks.py` fixtures
- Verify components exist in the database
- Check for any errors in the install script

### 2. Components Not Installed
- Check the `after_install` hook is properly configured
- Verify the dashboard fixtures file is accessible
- Check for any errors during installation

### 3. Missing Dependencies
- Ensure all required doctypes exist
- Check that module names are correct
- Verify document types referenced in filters exist

## Best Practices

1. **Always test** your dashboard components before pushing to GitHub
2. **Use descriptive names** for your components
3. **Include proper documentation** for complex filters or configurations
4. **Version control** your dashboard fixtures along with your code
5. **Test installation** in a clean environment before releasing

## Extending to Other Apps

To implement the same system for other Safari apps:

1. Create `dashboard_fixtures.py` in the app directory
2. Update the app's `setup/install.py` with dashboard installation
3. Update the app's `hooks.py` with dashboard fixtures
4. Create setup and verification scripts in `utils/`

This ensures all your custom dashboard components are properly exported and can be reinstalled on other systems. 