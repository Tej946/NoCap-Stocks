-- ==============================================================================
-- NoCap Stocks — Supabase Database Migration & Permissions Setup
-- Run this in your Supabase Dashboard SQL Editor
-- "No fake predictions. Just historical data."
-- ==============================================================================

-- 1. Ensure public.companies table exists with primary key and unique ticker
CREATE TABLE IF NOT EXISTS public.companies (
    id BIGSERIAL PRIMARY KEY,
    ticker TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    country TEXT NOT NULL,
    exchange TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Add extended optional fields if not already present
ALTER TABLE public.companies ADD COLUMN IF NOT EXISTS yahoo_ticker TEXT;
ALTER TABLE public.companies ADD COLUMN IF NOT EXISTS region TEXT;
ALTER TABLE public.companies ADD COLUMN IF NOT EXISTS currency TEXT;
ALTER TABLE public.companies ADD COLUMN IF NOT EXISTS logo_url TEXT;

-- 3. Indexes for fast search & filtering
CREATE INDEX IF NOT EXISTS idx_companies_ticker ON public.companies(ticker);
CREATE INDEX IF NOT EXISTS idx_companies_country ON public.companies(country);
CREATE INDEX IF NOT EXISTS idx_companies_exchange ON public.companies(exchange);
CREATE INDEX IF NOT EXISTS idx_companies_company_name ON public.companies(company_name);

-- 4. Historical stock_prices table for caching
CREATE TABLE IF NOT EXISTS public.stock_prices (
    id BIGSERIAL PRIMARY KEY,
    ticker TEXT NOT NULL,
    trading_date DATE NOT NULL,
    open NUMERIC(12, 4),
    high NUMERIC(12, 4),
    low NUMERIC(12, 4),
    close NUMERIC(12, 4),
    adjusted_close NUMERIC(12, 4),
    volume BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(ticker, trading_date)
);

CREATE INDEX IF NOT EXISTS idx_stock_prices_ticker_date ON public.stock_prices(ticker, trading_date);

-- 5. CRITICAL PRIVILEGE GRANTS:
-- Grant full DML privileges to service_role, anon, authenticated, and postgres
GRANT USAGE ON SCHEMA public TO postgres, service_role, anon, authenticated;
GRANT ALL ON TABLE public.companies TO postgres, service_role, anon, authenticated;
GRANT ALL ON TABLE public.stock_prices TO postgres, service_role, anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres, service_role, anon, authenticated;

-- 6. Row Level Security Policies (Read for all, Insert/Update for service_role)
ALTER TABLE public.companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.stock_prices ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow full access for service_role on companies" ON public.companies;
CREATE POLICY "Allow full access for service_role on companies" ON public.companies
    FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read on companies" ON public.companies;
CREATE POLICY "Allow public read on companies" ON public.companies
    FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Allow full access for service_role on stock_prices" ON public.stock_prices;
CREATE POLICY "Allow full access for service_role on stock_prices" ON public.stock_prices
    FOR ALL TO service_role USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read on stock_prices" ON public.stock_prices;
CREATE POLICY "Allow public read on stock_prices" ON public.stock_prices
    FOR SELECT TO anon, authenticated USING (true);
