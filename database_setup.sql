-- Walmart RBAC System Database Setup
-- Run these commands in your Supabase SQL Editor

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    failed_attempts INTEGER DEFAULT 0,
    geo_distance_km DECIMAL(10,2) DEFAULT 0.0,
    access_time VARCHAR(10),
    api_rate INTEGER DEFAULT 0,
    trust_score DECIMAL(3,2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create login_attempts table
CREATE TABLE IF NOT EXISTS login_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address VARCHAR(45),
    location VARCHAR(255),
    success BOOLEAN DEFAULT FALSE,
    reason VARCHAR(255),
    trust_score DECIMAL(3,2)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_login_attempts_user_id ON login_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_login_attempts_timestamp ON login_attempts(timestamp);

-- Insert a default admin user (password will be hashed by the application)
-- You should change this password after first login
INSERT INTO users (username, password, email, is_admin, trust_score) 
VALUES (
    'admin', 
    'pbkdf2:sha256:600000$your_hashed_password_here', 
    'admin@walmart.com', 
    TRUE,
    1.0
) ON CONFLICT (username) DO NOTHING;

-- Enable Row Level Security (RLS) for better security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE login_attempts ENABLE ROW LEVEL SECURITY;

-- Create policies for users table
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Admins can view all users" ON users
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid()::integer 
            AND is_admin = true
        )
    );

-- Create policies for login_attempts table
CREATE POLICY "Users can view their own login attempts" ON login_attempts
    FOR SELECT USING (user_id = auth.uid()::integer);

CREATE POLICY "Admins can view all login attempts" ON login_attempts
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid()::integer 
            AND is_admin = true
        )
    );

-- Grant necessary permissions
GRANT USAGE ON SEQUENCE users_id_seq TO anon, authenticated;
GRANT USAGE ON SEQUENCE login_attempts_id_seq TO anon, authenticated;
GRANT ALL ON users TO anon, authenticated;
GRANT ALL ON login_attempts TO anon, authenticated; 