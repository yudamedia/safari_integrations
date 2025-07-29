import frappe
from frappe import _
from cryptography.fernet import Fernet
import base64
import os

def get_encryption_key():
    """Get or create encryption key for API credentials"""
    try:
        # Check if key exists in site config
        encryption_key = frappe.conf.get("api_encryption_key")
        
        if not encryption_key:
            # Generate new key
            key = Fernet.generate_key()
            encryption_key = key.decode('utf-8')
            
            # Store in site config (you should manually add this to site_config.json)
            frappe.logger().warning(f"Add this to your site_config.json: 'api_encryption_key': '{encryption_key}'")
            
        return encryption_key.encode('utf-8')
        
    except Exception as e:
        frappe.log_error(f"Error getting encryption key: {str(e)}")
        # Return a default key for development (NOT for production)
        return Fernet.generate_key()

def encrypt_credential(credential_value):
    """Encrypt API credential value"""
    try:
        if not credential_value:
            return credential_value
            
        key = get_encryption_key()
        f = Fernet(key)
        
        encrypted_value = f.encrypt(credential_value.encode('utf-8'))
        return base64.b64encode(encrypted_value).decode('utf-8')
        
    except Exception as e:
        frappe.log_error(f"Error encrypting credential: {str(e)}")
        return credential_value  # Return original if encryption fails

def decrypt_credential(encrypted_value):
    """Decrypt API credential value"""
    try:
        if not encrypted_value:
            return encrypted_value
            
        key = get_encryption_key()
        f = Fernet(key)
        
        encrypted_bytes = base64.b64decode(encrypted_value.encode('utf-8'))
        decrypted_value = f.decrypt(encrypted_bytes)
        return decrypted_value.decode('utf-8')
        
    except Exception as e:
        frappe.log_error(f"Error decrypting credential: {str(e)}")
        return encrypted_value  # Return original if decryption fails

@frappe.whitelist()
def test_encryption():
    """Test encryption/decryption functionality"""
    try:
        test_value = "test-api-key-12345"
        
        encrypted = encrypt_credential(test_value)
        decrypted = decrypt_credential(encrypted)
        
        return {
            "success": decrypted == test_value,
            "original": test_value,
            "encrypted": encrypted,
            "decrypted": decrypted
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }