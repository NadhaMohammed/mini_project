-- ==============================================================================
-- Multi-Tenant Migration Script
-- Run this in your Supabase SQL Editor
-- ==============================================================================

-- 1. Add college_code to admin_username_pass
ALTER TABLE admin_username_pass
ADD COLUMN IF NOT EXISTS college_code VARCHAR(50);

-- Provide a default college code for the existing admin user
UPDATE admin_username_pass SET college_code = 'DEFAULT-123' WHERE username = 'admin' AND college_code IS NULL;

-- Now make it unique and not null
ALTER TABLE admin_username_pass
ADD CONSTRAINT unique_college_code UNIQUE (college_code);

ALTER TABLE admin_username_pass
ALTER COLUMN college_code SET NOT NULL;

-- 2. Add admin_id to events table
ALTER TABLE events
ADD COLUMN IF NOT EXISTS admin_id BIGINT REFERENCES admin_username_pass(id) ON DELETE CASCADE;

-- Assign all existing events to the default admin (assuming ID 1 is the default admin)
UPDATE events SET admin_id = (SELECT id FROM admin_username_pass WHERE username = 'admin' LIMIT 1) WHERE admin_id IS NULL;

ALTER TABLE events
ALTER COLUMN admin_id SET NOT NULL;

-- 3. Add admin_id to subscribers table
ALTER TABLE subscribers
ADD COLUMN IF NOT EXISTS admin_id BIGINT REFERENCES admin_username_pass(id) ON DELETE CASCADE;

-- Assign all existing subscribers to the default admin
UPDATE subscribers SET admin_id = (SELECT id FROM admin_username_pass WHERE username = 'admin' LIMIT 1) WHERE admin_id IS NULL;

ALTER TABLE subscribers
ALTER COLUMN admin_id SET NOT NULL;

-- Also remove the UNIQUE constraint on subscriber email, because the same student
-- might subscribe to multiple different colleges.
ALTER TABLE subscribers DROP CONSTRAINT IF EXISTS subscribers_email_key;
ALTER TABLE subscribers ADD CONSTRAINT unique_email_per_admin UNIQUE (email, admin_id);
