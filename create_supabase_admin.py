import os
from supabase import create_client, Client
from werkzeug.security import generate_password_hash

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', "https://jhdxzuguiwexjranriru.supabase.co")
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpoZHh6dWd1aXdleGpyYW5yaXJ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDk1MjczMSwiZXhwIjoyMDY2NTI4NzMxfQ.KN8j8JT56p-LyU7CJU9rStsncqFNcRGVcqMU3LYoYlE")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create admin user with hashed password
admin_username = "admin"
admin_password = "adminpass"  # This is the correct password
admin_email = "admin@walmart.com"
hashed_password = generate_password_hash(admin_password)

try:
    # Check if admin user already exists
    existing_user = supabase.table("users").select("*").eq("username", admin_username).execute()
    
    if existing_user.data:
        print(f"Admin user '{admin_username}' already exists in Supabase")
    else:
        # Create admin user
        admin_user = {
            "username": admin_username,
            "password": hashed_password,
            "email": admin_email,
            "is_admin": True,
            "totp_secret": None  # Admin doesn't need 2FA
        }
        
        result = supabase.table("users").insert(admin_user).execute()
        print(f"Admin user '{admin_username}' created successfully in Supabase")
        print(f"Username: {admin_username}")
        print(f"Password: {admin_password}")
        print(f"Email: {admin_email}")
        print(f"Is Admin: True")
        
except Exception as e:
    print(f"Error creating admin user: {e}") 