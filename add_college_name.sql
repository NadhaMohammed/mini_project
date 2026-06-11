-- Run this in your Supabase SQL Editor to add the missing 'college_name' column
ALTER TABLE public.admin_username_pass ADD COLUMN IF NOT EXISTS college_name text;
