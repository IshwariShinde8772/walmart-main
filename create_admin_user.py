#!/usr/bin/env python3
"""
Script to create an admin user with properly hashed password
Run this script to generate the SQL command for creating an admin user
"""

from werkzeug.security import generate_password_hash
import sys

def create_admin_user(username="admin", email="admin@walmart.com", password=None):
    """Generate SQL command to create admin user with hashed password"""
    
    if not password:
        print("Please provide a password for the admin user.")
        print("Usage: python create_admin_user.py <password>")
        print("Example: python create_admin_user.py myadminpassword123")
        sys.exit(1)
    
    # Generate hashed password
    hashed_password = generate_password_hash(password)
    
    # Generate SQL command
    sql_command = f"""
-- Admin user creation SQL command
-- Run this in your Supabase SQL Editor

INSERT INTO users (username, password, email, is_admin, trust_score) 
VALUES (
    '{username}', 
    '{hashed_password}', 
    '{email}', 
    TRUE,
    1.0
) ON CONFLICT (username) DO UPDATE SET
    password = EXCLUDED.password,
    email = EXCLUDED.email,
    is_admin = EXCLUDED.is_admin,
    trust_score = EXCLUDED.trust_score;
"""
    
    print("=" * 60)
    print("ADMIN USER CREATION SQL COMMAND")
    print("=" * 60)
    print(sql_command)
    print("=" * 60)
    print("Instructions:")
    print("1. Copy the SQL command above")
    print("2. Go to your Supabase project dashboard")
    print("3. Click on 'SQL Editor' in the left sidebar")
    print("4. Paste the command and click 'Run'")
    print("5. Your admin user will be created with the password you provided")
    print("=" * 60)
    print(f"Admin credentials:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Password is required")
        print("Usage: python create_admin_user.py <password>")
        sys.exit(1)
    
    password = sys.argv[1]
    create_admin_user(password=password) 