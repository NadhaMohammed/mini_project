-- Run this entire script in your Supabase SQL Editor to fix the RLS issues!

-- 1. Enable RLS on the tables (just in case they aren't already)
ALTER TABLE public.admin_username_pass ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.event_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscribers ENABLE ROW LEVEL SECURITY;

-- 2. Drop existing policies to avoid conflicts
DROP POLICY IF EXISTS "Allow public access to admin_username_pass" ON public.admin_username_pass;
DROP POLICY IF EXISTS "Allow public access to events" ON public.events;
DROP POLICY IF EXISTS "Allow public access to event_registrations" ON public.event_registrations;
DROP POLICY IF EXISTS "Allow public access to subscribers" ON public.subscribers;

-- 3. Create new policies that allow the 'anon' role full access
-- (Since your Flask backend uses the anon/publishable key, it needs these permissions)

CREATE POLICY "Allow public access to admin_username_pass"
ON public.admin_username_pass
FOR ALL
TO anon
USING (true)
WITH CHECK (true);

CREATE POLICY "Allow public access to events"
ON public.events
FOR ALL
TO anon
USING (true)
WITH CHECK (true);

CREATE POLICY "Allow public access to event_registrations"
ON public.event_registrations
FOR ALL
TO anon
USING (true)
WITH CHECK (true);

CREATE POLICY "Allow public access to subscribers"
ON public.subscribers
FOR ALL
TO anon
USING (true)
WITH CHECK (true);
