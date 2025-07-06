# Walmart RBAC System - Render Deployment Guide

## Prerequisites

- Render account (free tier available)
- Supabase project (for database)
- Gmail account (for SMTP email)

## Step 1: Prepare Your Supabase Database

1. Go to [Supabase](https://supabase.com) and create a new project
2. Create the following tables in your Supabase database:

### Users Table

```sql
CREATE TABLE users (
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
```

### Login Attempts Table

```sql
CREATE TABLE login_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address VARCHAR(45),
    location VARCHAR(255),
    success BOOLEAN DEFAULT FALSE,
    reason VARCHAR(255),
    trust_score DECIMAL(3,2)
);
```

3. Create an admin user:

```sql
INSERT INTO users (username, password, email, is_admin)
VALUES ('admin', 'hashed_password_here', 'admin@walmart.com', TRUE);
```

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file
6. Configure environment variables (see Step 3)

### Option B: Manual Deployment

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `walmart-rbac-system`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Set environment variables (see Step 3)

## Step 3: Configure Environment Variables

In your Render service settings, add these environment variables:

### Required Variables

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon/public key

### Optional Variables (for email functionality)

- `SMTP_EMAIL`: Your Gmail address
- `SMTP_PASSWORD`: Your Gmail app password

### How to get Supabase credentials:

1. Go to your Supabase project dashboard
2. Click "Settings" → "API"
3. Copy the "Project URL" and "anon public" key

### How to get Gmail app password:

1. Enable 2-factor authentication on your Gmail account
2. Go to Google Account settings → Security
3. Generate an "App password" for your application

## Step 4: Deploy and Test

1. Click "Create Web Service"
2. Wait for the build to complete (usually 2-5 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

## Step 5: Initial Setup

1. Visit your deployed application
2. Create an admin account or use the one you created in Supabase
3. Test the login functionality
4. Verify that the ML trust scoring is working

## Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **Database connection error**: Verify Supabase URL and key are correct
3. **Email not working**: Check SMTP credentials and ensure Gmail app password is used
4. **App crashes**: Check Render logs for error messages

### Checking Logs:

1. Go to your Render service dashboard
2. Click "Logs" tab
3. Look for error messages in the build or runtime logs

## Security Notes

- Never commit sensitive credentials to your repository
- Use environment variables for all secrets
- Consider using Render's secret management for production
- Regularly update dependencies for security patches

## Cost Optimization

- Free tier includes 750 hours/month
- Service sleeps after 15 minutes of inactivity
- Consider upgrading to paid plan for production use

## Support

If you encounter issues:

1. Check Render documentation: https://render.com/docs
2. Review Flask deployment best practices
3. Check Supabase documentation for database issues
