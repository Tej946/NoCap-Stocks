"""
NoCap Stocks â€” Global Companies Catalog & Registry
Comprehensive seed dataset of major publicly traded global companies across 23+ countries and 20+ exchanges.
All tickers adhere strictly to official Yahoo Finance symbology.
"""

GLOBAL_COMPANIES = [
    # =========================================================================
    # UNITED STATES (NASDAQ / NYSE)
    # =========================================================================
    {"ticker": "AAPL", "yahoo_ticker": "AAPL", "company_name": "Apple Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "MSFT", "yahoo_ticker": "MSFT", "company_name": "Microsoft Corporation", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "NVDA", "yahoo_ticker": "NVDA", "company_name": "NVIDIA Corporation", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "AMZN", "yahoo_ticker": "AMZN", "company_name": "Amazon.com, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "GOOGL", "yahoo_ticker": "GOOGL", "company_name": "Alphabet Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "META", "yahoo_ticker": "META", "company_name": "Meta Platforms, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "TSLA", "yahoo_ticker": "TSLA", "company_name": "Tesla, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "AVGO", "yahoo_ticker": "AVGO", "company_name": "Broadcom Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "AMD", "yahoo_ticker": "AMD", "company_name": "Advanced Micro Devices, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "NFLX", "yahoo_ticker": "NFLX", "company_name": "Netflix, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "ORCL", "yahoo_ticker": "ORCL", "company_name": "Oracle Corporation", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "CRM", "yahoo_ticker": "CRM", "company_name": "Salesforce, Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "ADBE", "yahoo_ticker": "ADBE", "company_name": "Adobe Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "INTC", "yahoo_ticker": "INTC", "company_name": "Intel Corporation", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "QCOM", "yahoo_ticker": "QCOM", "company_name": "Qualcomm Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "CSCO", "yahoo_ticker": "CSCO", "company_name": "Cisco Systems, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "IBM", "yahoo_ticker": "IBM", "company_name": "International Business Machines", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "UBER", "yahoo_ticker": "UBER", "company_name": "Uber Technologies, Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "PYPL", "yahoo_ticker": "PYPL", "company_name": "PayPal Holdings, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "COST", "yahoo_ticker": "COST", "company_name": "Costco Wholesale Corporation", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "WMT", "yahoo_ticker": "WMT", "company_name": "Walmart Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "KO", "yahoo_ticker": "KO", "company_name": "The Coca-Cola Company", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "PEP", "yahoo_ticker": "PEP", "company_name": "PepsiCo, Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "MCD", "yahoo_ticker": "MCD", "company_name": "McDonald's Corporation", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "NKE", "yahoo_ticker": "NKE", "company_name": "NIKE, Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "DIS", "yahoo_ticker": "DIS", "company_name": "The Walt Disney Company", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "JPM", "yahoo_ticker": "JPM", "company_name": "JPMorgan Chase & Co.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "BAC", "yahoo_ticker": "BAC", "company_name": "Bank of America Corporation", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "GS", "yahoo_ticker": "GS", "company_name": "The Goldman Sachs Group, Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "V", "yahoo_ticker": "V", "company_name": "Visa Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "MA", "yahoo_ticker": "MA", "company_name": "Mastercard Incorporated", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "JNJ", "yahoo_ticker": "JNJ", "company_name": "Johnson & Johnson", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "PFE", "yahoo_ticker": "PFE", "company_name": "Pfizer Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "MRK", "yahoo_ticker": "MRK", "company_name": "Merck & Co., Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "XOM", "yahoo_ticker": "XOM", "company_name": "Exxon Mobil Corporation", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "CVX", "yahoo_ticker": "CVX", "company_name": "Chevron Corporation", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "LLY", "yahoo_ticker": "LLY", "company_name": "Eli Lilly and Company", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "UNH", "yahoo_ticker": "UNH", "company_name": "UnitedHealth Group Incorporated", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "HD", "yahoo_ticker": "HD", "company_name": "The Home Depot, Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "PG", "yahoo_ticker": "PG", "company_name": "The Procter & Gamble Company", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "TXN", "yahoo_ticker": "TXN", "company_name": "Texas Instruments Incorporated", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "NOW", "yahoo_ticker": "NOW", "company_name": "ServiceNow, Inc.", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},
    {"ticker": "INTU", "yahoo_ticker": "INTU", "company_name": "Intuit Inc.", "country": "United States", "exchange": "NASDAQ", "currency": "USD", "region": "Americas"},
    {"ticker": "ACN", "yahoo_ticker": "ACN", "company_name": "Accenture plc", "country": "United States", "exchange": "NYSE", "currency": "USD", "region": "Americas"},

    # =========================================================================
    # INDIA (NSE / BSE)
    # =========================================================================
    {"ticker": "TCS.NS", "yahoo_ticker": "TCS.NS", "company_name": "Tata Consultancy Services", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "INFY.NS", "yahoo_ticker": "INFY.NS", "company_name": "Infosys Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "RELIANCE.NS", "yahoo_ticker": "RELIANCE.NS", "company_name": "Reliance Industries Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "HDFCBANK.NS", "yahoo_ticker": "HDFCBANK.NS", "company_name": "HDFC Bank Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "ICICIBANK.NS", "yahoo_ticker": "ICICIBANK.NS", "company_name": "ICICI Bank Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "SBIN.NS", "yahoo_ticker": "SBIN.NS", "company_name": "State Bank of India", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "BHARTIARTL.NS", "yahoo_ticker": "BHARTIARTL.NS", "company_name": "Bharti Airtel Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "ITC.NS", "yahoo_ticker": "ITC.NS", "company_name": "ITC Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "LT.NS", "yahoo_ticker": "LT.NS", "company_name": "Larsen & Toubro Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "HCLTECH.NS", "yahoo_ticker": "HCLTECH.NS", "company_name": "HCL Technologies Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "WIPRO.NS", "yahoo_ticker": "WIPRO.NS", "company_name": "Wipro Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "MARUTI.NS", "yahoo_ticker": "MARUTI.NS", "company_name": "Maruti Suzuki India Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "TATAMOTORS.NS", "yahoo_ticker": "TATAMOTORS.NS", "company_name": "Tata Motors Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "SUNPHARMA.NS", "yahoo_ticker": "SUNPHARMA.NS", "company_name": "Sun Pharmaceutical Industries", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "AXISBANK.NS", "yahoo_ticker": "AXISBANK.NS", "company_name": "Axis Bank Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "KOTAKBANK.NS", "yahoo_ticker": "KOTAKBANK.NS", "company_name": "Kotak Mahindra Bank Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "ASIANPAINT.NS", "yahoo_ticker": "ASIANPAINT.NS", "company_name": "Asian Paints Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "BAJFINANCE.NS", "yahoo_ticker": "BAJFINANCE.NS", "company_name": "Bajaj Finance Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "ADANIENT.NS", "yahoo_ticker": "ADANIENT.NS", "company_name": "Adani Enterprises Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "ZOMATO.NS", "yahoo_ticker": "ZOMATO.NS", "company_name": "Zomato Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "TRENT.NS", "yahoo_ticker": "TRENT.NS", "company_name": "Trent Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "TITAN.NS", "yahoo_ticker": "TITAN.NS", "company_name": "Titan Company Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "ULTRACEMCO.NS", "yahoo_ticker": "ULTRACEMCO.NS", "company_name": "UltraTech Cement Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "POWERGRID.NS", "yahoo_ticker": "POWERGRID.NS", "company_name": "Power Grid Corporation of India", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},
    {"ticker": "NTPC.NS", "yahoo_ticker": "NTPC.NS", "company_name": "NTPC Limited", "country": "India", "exchange": "NSE", "currency": "INR", "region": "Asia-Pacific"},

    # =========================================================================
    # JAPAN (TSE)
    # =========================================================================
    {"ticker": "7203.T", "yahoo_ticker": "7203.T", "company_name": "Toyota Motor Corporation", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "6758.T", "yahoo_ticker": "6758.T", "company_name": "Sony Group Corporation", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "9984.T", "yahoo_ticker": "9984.T", "company_name": "SoftBank Group Corp.", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "6861.T", "yahoo_ticker": "6861.T", "company_name": "Keyence Corporation", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "6902.T", "yahoo_ticker": "6902.T", "company_name": "Denso Corporation", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "6501.T", "yahoo_ticker": "6501.T", "company_name": "Hitachi, Ltd.", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "7267.T", "yahoo_ticker": "7267.T", "company_name": "Honda Motor Co., Ltd.", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "7974.T", "yahoo_ticker": "7974.T", "company_name": "Nintendo Co., Ltd.", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "8035.T", "yahoo_ticker": "8035.T", "company_name": "Tokyo Electron Limited", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "9432.T", "yahoo_ticker": "9432.T", "company_name": "Nippon Telegraph and Telephone", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "6098.T", "yahoo_ticker": "6098.T", "company_name": "Recruit Holdings Co., Ltd.", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "4063.T", "yahoo_ticker": "4063.T", "company_name": "Shin-Etsu Chemical Co., Ltd.", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "8306.T", "yahoo_ticker": "8306.T", "company_name": "Mitsubishi UFJ Financial Group", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "8058.T", "yahoo_ticker": "8058.T", "company_name": "Mitsubishi Corporation", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},
    {"ticker": "9983.T", "yahoo_ticker": "9983.T", "company_name": "Fast Retailing Co., Ltd.", "country": "Japan", "exchange": "TSE", "currency": "JPY", "region": "Asia-Pacific"},

    # =========================================================================
    # UNITED KINGDOM (LSE)
    # =========================================================================
    {"ticker": "AZN.L", "yahoo_ticker": "AZN.L", "company_name": "AstraZeneca PLC", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "SHEL.L", "yahoo_ticker": "SHEL.L", "company_name": "Shell plc", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "HSBA.L", "yahoo_ticker": "HSBA.L", "company_name": "HSBC Holdings plc", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "ULVR.L", "yahoo_ticker": "ULVR.L", "company_name": "Unilever PLC", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "BP.L", "yahoo_ticker": "BP.L", "company_name": "BP p.l.c.", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "GSK.L", "yahoo_ticker": "GSK.L", "company_name": "GSK plc", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "RIO.L", "yahoo_ticker": "RIO.L", "company_name": "Rio Tinto Group", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "BARC.L", "yahoo_ticker": "BARC.L", "company_name": "Barclays PLC", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "VOD.L", "yahoo_ticker": "VOD.L", "company_name": "Vodafone Group Plc", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "LSEG.L", "yahoo_ticker": "LSEG.L", "company_name": "London Stock Exchange Group plc", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "DGE.L", "yahoo_ticker": "DGE.L", "company_name": "Diageo plc", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "REL.L", "yahoo_ticker": "REL.L", "company_name": "RELX PLC", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "BATS.L", "yahoo_ticker": "BATS.L", "company_name": "British American Tobacco p.l.c.", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},
    {"ticker": "LLOY.L", "yahoo_ticker": "LLOY.L", "company_name": "Lloyds Banking Group plc", "country": "United Kingdom", "exchange": "LSE", "currency": "GBP", "region": "Europe"},

    # =========================================================================
    # GERMANY (XETRA)
    # =========================================================================
    {"ticker": "SAP.DE", "yahoo_ticker": "SAP.DE", "company_name": "SAP SE", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "SIE.DE", "yahoo_ticker": "SIE.DE", "company_name": "Siemens AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "DTE.DE", "yahoo_ticker": "DTE.DE", "company_name": "Deutsche Telekom AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "ALV.DE", "yahoo_ticker": "ALV.DE", "company_name": "Allianz SE", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "BMW.DE", "yahoo_ticker": "BMW.DE", "company_name": "Bayerische Motoren Werke AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "MBG.DE", "yahoo_ticker": "MBG.DE", "company_name": "Mercedes-Benz Group AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "VOW3.DE", "yahoo_ticker": "VOW3.DE", "company_name": "Volkswagen AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "BAYN.DE", "yahoo_ticker": "BAYN.DE", "company_name": "Bayer AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "DBK.DE", "yahoo_ticker": "DBK.DE", "company_name": "Deutsche Bank AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "PUM.DE", "yahoo_ticker": "PUM.DE", "company_name": "Puma SE", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "ADS.DE", "yahoo_ticker": "ADS.DE", "company_name": "Adidas AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "BAS.DE", "yahoo_ticker": "BAS.DE", "company_name": "BASF SE", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "IFX.DE", "yahoo_ticker": "IFX.DE", "company_name": "Infineon Technologies AG", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},
    {"ticker": "MUV2.DE", "yahoo_ticker": "MUV2.DE", "company_name": "Munich Re", "country": "Germany", "exchange": "XETRA", "currency": "EUR", "region": "Europe"},

    # =========================================================================
    # FRANCE (Euronext Paris)
    # =========================================================================
    {"ticker": "MC.PA", "yahoo_ticker": "MC.PA", "company_name": "LVMH MoÃ«t Hennessy Louis Vuitton", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "OR.PA", "yahoo_ticker": "OR.PA", "company_name": "L'OrÃ©al S.A.", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "TTE.PA", "yahoo_ticker": "TTE.PA", "company_name": "TotalEnergies SE", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "SAN.PA", "yahoo_ticker": "SAN.PA", "company_name": "Sanofi", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "AIR.PA", "yahoo_ticker": "AIR.PA", "company_name": "Airbus SE", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "BNP.PA", "yahoo_ticker": "BNP.PA", "company_name": "BNP Paribas S.A.", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "SU.PA", "yahoo_ticker": "SU.PA", "company_name": "Schneider Electric SE", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "RMS.PA", "yahoo_ticker": "RMS.PA", "company_name": "HermÃ¨s International", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "KER.PA", "yahoo_ticker": "KER.PA", "company_name": "Kering SA", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "AI.PA", "yahoo_ticker": "AI.PA", "company_name": "Air Liquide S.A.", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},
    {"ticker": "CS.PA", "yahoo_ticker": "CS.PA", "company_name": "AXA SA", "country": "France", "exchange": "Euronext Paris", "currency": "EUR", "region": "Europe"},

    # =========================================================================
    # SWITZERLAND (SIX)
    # =========================================================================
    {"ticker": "NESN.SW", "yahoo_ticker": "NESN.SW", "company_name": "Nestlé S.A.", "country": "Switzerland", "exchange": "SIX", "currency": "CHF", "region": "Europe"},
    {"ticker": "ROG.SW", "yahoo_ticker": "ROG.SW", "company_name": "Roche Holding AG", "country": "Switzerland", "exchange": "SIX", "currency": "CHF", "region": "Europe"},
    {"ticker": "NOVN.SW", "yahoo_ticker": "NOVN.SW", "company_name": "Novartis AG", "country": "Switzerland", "exchange": "SIX", "currency": "CHF", "region": "Europe"},
    {"ticker": "UBSG.SW", "yahoo_ticker": "UBSG.SW", "company_name": "UBS Group AG", "country": "Switzerland", "exchange": "SIX", "currency": "CHF", "region": "Europe"},
    {"ticker": "ABBN.SW", "yahoo_ticker": "ABBN.SW", "company_name": "ABB Ltd", "country": "Switzerland", "exchange": "SIX", "currency": "CHF", "region": "Europe"},
    {"ticker": "ZURN.SW", "yahoo_ticker": "ZURN.SW", "company_name": "Zurich Insurance Group AG", "country": "Switzerland", "exchange": "SIX", "currency": "CHF", "region": "Europe"},
    {"ticker": "CFR.SW", "yahoo_ticker": "CFR.SW", "company_name": "Compagnie FinanciÃ¨re Richemont SA", "country": "Switzerland", "exchange": "SIX", "currency": "CHF", "region": "Europe"},

    # =========================================================================
    # SOUTH KOREA (KRX)
    # =========================================================================
    {"ticker": "005930.KS", "yahoo_ticker": "005930.KS", "company_name": "Samsung Electronics Co., Ltd.", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "000660.KS", "yahoo_ticker": "000660.KS", "company_name": "SK Hynix Inc.", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "005380.KS", "yahoo_ticker": "005380.KS", "company_name": "Hyundai Motor Company", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "035420.KS", "yahoo_ticker": "035420.KS", "company_name": "NAVER Corporation", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "035720.KS", "yahoo_ticker": "035720.KS", "company_name": "Kakao Corp.", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "051910.KS", "yahoo_ticker": "051910.KS", "company_name": "LG Chem, Ltd.", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "000270.KS", "yahoo_ticker": "000270.KS", "company_name": "Kia Corporation", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "068270.KS", "yahoo_ticker": "068270.KS", "company_name": "Celltrion, Inc.", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "105560.KS", "yahoo_ticker": "105560.KS", "company_name": "KB Financial Group Inc.", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},
    {"ticker": "055550.KS", "yahoo_ticker": "055550.KS", "company_name": "Shinhan Financial Group", "country": "South Korea", "exchange": "KRX", "currency": "KRW", "region": "Asia-Pacific"},

    # =========================================================================
    # HONG KONG (HKEX)
    # =========================================================================
    {"ticker": "0700.HK", "yahoo_ticker": "0700.HK", "company_name": "Tencent Holdings Limited", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "9988.HK", "yahoo_ticker": "9988.HK", "company_name": "Alibaba Group Holding Limited", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "1810.HK", "yahoo_ticker": "1810.HK", "company_name": "Xiaomi Corporation", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "3690.HK", "yahoo_ticker": "3690.HK", "company_name": "Meituan", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "9618.HK", "yahoo_ticker": "9618.HK", "company_name": "JD.com, Inc.", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "1299.HK", "yahoo_ticker": "1299.HK", "company_name": "AIA Group Limited", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "0941.HK", "yahoo_ticker": "0941.HK", "company_name": "China Mobile Limited", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "0388.HK", "yahoo_ticker": "0388.HK", "company_name": "Hong Kong Exchanges and Clearing", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "2318.HK", "yahoo_ticker": "2318.HK", "company_name": "Ping An Insurance Group", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},
    {"ticker": "1211.HK", "yahoo_ticker": "1211.HK", "company_name": "BYD Company Limited", "country": "Hong Kong", "exchange": "HKEX", "currency": "HKD", "region": "Asia-Pacific"},

    # =========================================================================
    # CHINA (Yahoo-supported Global Listings)
    # =========================================================================
    {"ticker": "BABA", "yahoo_ticker": "BABA", "company_name": "Alibaba Group Holding Limited", "country": "China", "exchange": "NYSE", "currency": "USD", "region": "Asia-Pacific"},
    {"ticker": "PDD", "yahoo_ticker": "PDD", "company_name": "PDD Holdings Inc.", "country": "China", "exchange": "NASDAQ", "currency": "USD", "region": "Asia-Pacific"},
    {"ticker": "JD", "yahoo_ticker": "JD", "company_name": "JD.com, Inc.", "country": "China", "exchange": "NASDAQ", "currency": "USD", "region": "Asia-Pacific"},
    {"ticker": "BIDU", "yahoo_ticker": "BIDU", "company_name": "Baidu, Inc.", "country": "China", "exchange": "NASDAQ", "currency": "USD", "region": "Asia-Pacific"},
    {"ticker": "NTES", "yahoo_ticker": "NTES", "company_name": "NetEase, Inc.", "country": "China", "exchange": "NASDAQ", "currency": "USD", "region": "Asia-Pacific"},
    {"ticker": "NIO", "yahoo_ticker": "NIO", "company_name": "NIO Inc.", "country": "China", "exchange": "NYSE", "currency": "USD", "region": "Asia-Pacific"},
    {"ticker": "LI", "yahoo_ticker": "LI", "company_name": "Li Auto Inc.", "country": "China", "exchange": "NASDAQ", "currency": "USD", "region": "Asia-Pacific"},
    {"ticker": "XPEV", "yahoo_ticker": "XPEV", "company_name": "XPeng Inc.", "country": "China", "exchange": "NYSE", "currency": "USD", "region": "Asia-Pacific"},

    # =========================================================================
    # CANADA (TSX)
    # =========================================================================
    {"ticker": "SHOP.TO", "yahoo_ticker": "SHOP.TO", "company_name": "Shopify Inc.", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "RY.TO", "yahoo_ticker": "RY.TO", "company_name": "Royal Bank of Canada", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "TD.TO", "yahoo_ticker": "TD.TO", "company_name": "Toronto-Dominion Bank", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "ENB.TO", "yahoo_ticker": "ENB.TO", "company_name": "Enbridge Inc.", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "CNR.TO", "yahoo_ticker": "CNR.TO", "company_name": "Canadian National Railway", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "BNS.TO", "yahoo_ticker": "BNS.TO", "company_name": "Bank of Nova Scotia", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "BMO.TO", "yahoo_ticker": "BMO.TO", "company_name": "Bank of Montreal", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "CP.TO", "yahoo_ticker": "CP.TO", "company_name": "Canadian Pacific Kansas City", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "SU.TO", "yahoo_ticker": "SU.TO", "company_name": "Suncor Energy Inc.", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},
    {"ticker": "BAM.TO", "yahoo_ticker": "BAM.TO", "company_name": "Brookfield Asset Management", "country": "Canada", "exchange": "TSX", "currency": "CAD", "region": "Americas"},

    # =========================================================================
    # AUSTRALIA (ASX)
    # =========================================================================
    {"ticker": "BHP.AX", "yahoo_ticker": "BHP.AX", "company_name": "BHP Group Limited", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "CBA.AX", "yahoo_ticker": "CBA.AX", "company_name": "Commonwealth Bank of Australia", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "CSL.AX", "yahoo_ticker": "CSL.AX", "company_name": "CSL Limited", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "WBC.AX", "yahoo_ticker": "WBC.AX", "company_name": "Westpac Banking Corporation", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "ANZ.AX", "yahoo_ticker": "ANZ.AX", "company_name": "ANZ Group Holdings Limited", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "NAB.AX", "yahoo_ticker": "NAB.AX", "company_name": "National Australia Bank Limited", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "RIO.AX", "yahoo_ticker": "RIO.AX", "company_name": "Rio Tinto Limited", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "WES.AX", "yahoo_ticker": "WES.AX", "company_name": "Wesfarmers Limited", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "MQG.AX", "yahoo_ticker": "MQG.AX", "company_name": "Macquarie Group Limited", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},
    {"ticker": "FMG.AX", "yahoo_ticker": "FMG.AX", "company_name": "Fortescue Ltd", "country": "Australia", "exchange": "ASX", "currency": "AUD", "region": "Asia-Pacific"},

    # =========================================================================
    # SINGAPORE (SGX)
    # =========================================================================
    {"ticker": "D05.SI", "yahoo_ticker": "D05.SI", "company_name": "DBS Group Holdings Ltd", "country": "Singapore", "exchange": "SGX", "currency": "SGD", "region": "Asia-Pacific"},
    {"ticker": "O39.SI", "yahoo_ticker": "O39.SI", "company_name": "Oversea-Chinese Banking Corp", "country": "Singapore", "exchange": "SGX", "currency": "SGD", "region": "Asia-Pacific"},
    {"ticker": "U11.SI", "yahoo_ticker": "U11.SI", "company_name": "United Overseas Bank Limited", "country": "Singapore", "exchange": "SGX", "currency": "SGD", "region": "Asia-Pacific"},
    {"ticker": "Z74.SI", "yahoo_ticker": "Z74.SI", "company_name": "Singapore Telecommunications", "country": "Singapore", "exchange": "SGX", "currency": "SGD", "region": "Asia-Pacific"},
    {"ticker": "C6L.SI", "yahoo_ticker": "C6L.SI", "company_name": "Singapore Airlines Limited", "country": "Singapore", "exchange": "SGX", "currency": "SGD", "region": "Asia-Pacific"},
    {"ticker": "BN4.SI", "yahoo_ticker": "BN4.SI", "company_name": "Keppel Ltd.", "country": "Singapore", "exchange": "SGX", "currency": "SGD", "region": "Asia-Pacific"},

    # =========================================================================
    # TAIWAN (TWSE)
    # =========================================================================
    {"ticker": "2330.TW", "yahoo_ticker": "2330.TW", "company_name": "Taiwan Semiconductor Manufacturing (TSMC)", "country": "Taiwan", "exchange": "TWSE", "currency": "TWD", "region": "Asia-Pacific"},
    {"ticker": "2317.TW", "yahoo_ticker": "2317.TW", "company_name": "Hon Hai Precision Industry (Foxconn)", "country": "Taiwan", "exchange": "TWSE", "currency": "TWD", "region": "Asia-Pacific"},
    {"ticker": "2454.TW", "yahoo_ticker": "2454.TW", "company_name": "MediaTek Inc.", "country": "Taiwan", "exchange": "TWSE", "currency": "TWD", "region": "Asia-Pacific"},
    {"ticker": "2412.TW", "yahoo_ticker": "2412.TW", "company_name": "Chunghwa Telecom Co., Ltd.", "country": "Taiwan", "exchange": "TWSE", "currency": "TWD", "region": "Asia-Pacific"},
    {"ticker": "2881.TW", "yahoo_ticker": "2881.TW", "company_name": "Fubon Financial Holding Co.", "country": "Taiwan", "exchange": "TWSE", "currency": "TWD", "region": "Asia-Pacific"},
    {"ticker": "2882.TW", "yahoo_ticker": "2882.TW", "company_name": "Cathay Financial Holding Co.", "country": "Taiwan", "exchange": "TWSE", "currency": "TWD", "region": "Asia-Pacific"},
    {"ticker": "2308.TW", "yahoo_ticker": "2308.TW", "company_name": "Delta Electronics, Inc.", "country": "Taiwan", "exchange": "TWSE", "currency": "TWD", "region": "Asia-Pacific"},

    # =========================================================================
    # BRAZIL (B3)
    # =========================================================================
    {"ticker": "VALE3.SA", "yahoo_ticker": "VALE3.SA", "company_name": "Vale S.A.", "country": "Brazil", "exchange": "B3", "currency": "BRL", "region": "Americas"},
    {"ticker": "PETR3.SA", "yahoo_ticker": "PETR3.SA", "company_name": "PetrÃ³leo Brasileiro - Petrobras ON", "country": "Brazil", "exchange": "B3", "currency": "BRL", "region": "Americas"},
    {"ticker": "PETR4.SA", "yahoo_ticker": "PETR4.SA", "company_name": "PetrÃ³leo Brasileiro - Petrobras PN", "country": "Brazil", "exchange": "B3", "currency": "BRL", "region": "Americas"},
    {"ticker": "ITUB4.SA", "yahoo_ticker": "ITUB4.SA", "company_name": "ItaÃº Unibanco Holding S.A.", "country": "Brazil", "exchange": "B3", "currency": "BRL", "region": "Americas"},
    {"ticker": "BBDC4.SA", "yahoo_ticker": "BBDC4.SA", "company_name": "Banco Bradesco S.A.", "country": "Brazil", "exchange": "B3", "currency": "BRL", "region": "Americas"},
    {"ticker": "ABEV3.SA", "yahoo_ticker": "ABEV3.SA", "company_name": "Ambev S.A.", "country": "Brazil", "exchange": "B3", "currency": "BRL", "region": "Americas"},
    {"ticker": "WEGE3.SA", "yahoo_ticker": "WEGE3.SA", "company_name": "WEG S.A.", "country": "Brazil", "exchange": "B3", "currency": "BRL", "region": "Americas"},

    # =========================================================================
    # NETHERLANDS (Euronext Amsterdam)
    # =========================================================================
    {"ticker": "ASML.AS", "yahoo_ticker": "ASML.AS", "company_name": "ASML Holding N.V.", "country": "Netherlands", "exchange": "Euronext Amsterdam", "currency": "EUR", "region": "Europe"},
    {"ticker": "ADYEN.AS", "yahoo_ticker": "ADYEN.AS", "company_name": "Adyen N.V.", "country": "Netherlands", "exchange": "Euronext Amsterdam", "currency": "EUR", "region": "Europe"},
    {"ticker": "INGA.AS", "yahoo_ticker": "INGA.AS", "company_name": "ING Groep N.V.", "country": "Netherlands", "exchange": "Euronext Amsterdam", "currency": "EUR", "region": "Europe"},
    {"ticker": "PRX.AS", "yahoo_ticker": "PRX.AS", "company_name": "Prosus N.V.", "country": "Netherlands", "exchange": "Euronext Amsterdam", "currency": "EUR", "region": "Europe"},
    {"ticker": "HEIA.AS", "yahoo_ticker": "HEIA.AS", "company_name": "Heineken N.V.", "country": "Netherlands", "exchange": "Euronext Amsterdam", "currency": "EUR", "region": "Europe"},
    {"ticker": "UNA.AS", "yahoo_ticker": "UNA.AS", "company_name": "Unilever PLC (Amsterdam)", "country": "Netherlands", "exchange": "Euronext Amsterdam", "currency": "EUR", "region": "Europe"},

    # =========================================================================
    # SPAIN (BME)
    # =========================================================================
    {"ticker": "IBE.MC", "yahoo_ticker": "IBE.MC", "company_name": "Iberdrola, S.A.", "country": "Spain", "exchange": "BME", "currency": "EUR", "region": "Europe"},
    {"ticker": "SAN.MC", "yahoo_ticker": "SAN.MC", "company_name": "Banco Santander, S.A.", "country": "Spain", "exchange": "BME", "currency": "EUR", "region": "Europe"},
    {"ticker": "BBVA.MC", "yahoo_ticker": "BBVA.MC", "company_name": "Banco Bilbao Vizcaya Argentaria", "country": "Spain", "exchange": "BME", "currency": "EUR", "region": "Europe"},
    {"ticker": "ITX.MC", "yahoo_ticker": "ITX.MC", "company_name": "Industria de DiseÃ±o Textil (Inditex)", "country": "Spain", "exchange": "BME", "currency": "EUR", "region": "Europe"},
    {"ticker": "TEF.MC", "yahoo_ticker": "TEF.MC", "company_name": "TelefÃ³nica, S.A.", "country": "Spain", "exchange": "BME", "currency": "EUR", "region": "Europe"},

    # =========================================================================
    # ITALY (Borsa Italiana)
    # =========================================================================
    {"ticker": "ENI.MI", "yahoo_ticker": "ENI.MI", "company_name": "Eni S.p.A.", "country": "Italy", "exchange": "Borsa Italiana", "currency": "EUR", "region": "Europe"},
    {"ticker": "ISP.MI", "yahoo_ticker": "ISP.MI", "company_name": "Intesa Sanpaolo S.p.A.", "country": "Italy", "exchange": "Borsa Italiana", "currency": "EUR", "region": "Europe"},
    {"ticker": "ENEL.MI", "yahoo_ticker": "ENEL.MI", "company_name": "Enel S.p.A.", "country": "Italy", "exchange": "Borsa Italiana", "currency": "EUR", "region": "Europe"},
    {"ticker": "RACE.MI", "yahoo_ticker": "RACE.MI", "company_name": "Ferrari N.V.", "country": "Italy", "exchange": "Borsa Italiana", "currency": "EUR", "region": "Europe"},
    {"ticker": "STLAM.MI", "yahoo_ticker": "STLAM.MI", "company_name": "Stellantis N.V.", "country": "Italy", "exchange": "Borsa Italiana", "currency": "EUR", "region": "Europe"},

    # =========================================================================
    # SOUTH AFRICA (JSE)
    # =========================================================================
    {"ticker": "NPN.JO", "yahoo_ticker": "NPN.JO", "company_name": "Naspers Limited", "country": "South Africa", "exchange": "JSE", "currency": "ZAR", "region": "Africa"},
    {"ticker": "AGL.JO", "yahoo_ticker": "AGL.JO", "company_name": "Anglo American plc", "country": "South Africa", "exchange": "JSE", "currency": "ZAR", "region": "Africa"},
    {"ticker": "SOL.JO", "yahoo_ticker": "SOL.JO", "company_name": "Sasol Limited", "country": "South Africa", "exchange": "JSE", "currency": "ZAR", "region": "Africa"},
    {"ticker": "SBK.JO", "yahoo_ticker": "SBK.JO", "company_name": "Standard Bank Group Limited", "country": "South Africa", "exchange": "JSE", "currency": "ZAR", "region": "Africa"},

    # =========================================================================
    # SWEDEN (Nasdaq Stockholm)
    # =========================================================================
    {"ticker": "ERIC-B.ST", "yahoo_ticker": "ERIC-B.ST", "company_name": "Telefonaktiebolaget LM Ericsson", "country": "Sweden", "exchange": "Nasdaq Stockholm", "currency": "SEK", "region": "Europe"},
    {"ticker": "VOLV-B.ST", "yahoo_ticker": "VOLV-B.ST", "company_name": "Volvo AB", "country": "Sweden", "exchange": "Nasdaq Stockholm", "currency": "SEK", "region": "Europe"},
    {"ticker": "ATLAS-A.ST", "yahoo_ticker": "ATLAS-A.ST", "company_name": "Atlas Copco AB", "country": "Sweden", "exchange": "Nasdaq Stockholm", "currency": "SEK", "region": "Europe"},
    {"ticker": "INVE-B.ST", "yahoo_ticker": "INVE-B.ST", "company_name": "Investor AB", "country": "Sweden", "exchange": "Nasdaq Stockholm", "currency": "SEK", "region": "Europe"},
    {"ticker": "HM-B.ST", "yahoo_ticker": "HM-B.ST", "company_name": "H & M Hennes & Mauritz AB", "country": "Sweden", "exchange": "Nasdaq Stockholm", "currency": "SEK", "region": "Europe"},

    # =========================================================================
    # DENMARK (Nasdaq Copenhagen)
    # =========================================================================
    {"ticker": "NOVO-B.CO", "yahoo_ticker": "NOVO-B.CO", "company_name": "Novo Nordisk A/S", "country": "Denmark", "exchange": "Nasdaq Copenhagen", "currency": "DKK", "region": "Europe"},
    {"ticker": "MAERSK-B.CO", "yahoo_ticker": "MAERSK-B.CO", "company_name": "A.P. MÃ¸ller - MÃ¦rsk A/S", "country": "Denmark", "exchange": "Nasdaq Copenhagen", "currency": "DKK", "region": "Europe"},
    {"ticker": "DSV.CO", "yahoo_ticker": "DSV.CO", "company_name": "DSV A/S", "country": "Denmark", "exchange": "Nasdaq Copenhagen", "currency": "DKK", "region": "Europe"},

    # =========================================================================
    # NORWAY (Oslo BÃ¸rs)
    # =========================================================================
    {"ticker": "EQNR.OL", "yahoo_ticker": "EQNR.OL", "company_name": "Equinor ASA", "country": "Norway", "exchange": "Oslo BÃ¸rs", "currency": "NOK", "region": "Europe"},
    {"ticker": "DNB.OL", "yahoo_ticker": "DNB.OL", "company_name": "DNB Bank ASA", "country": "Norway", "exchange": "Oslo BÃ¸rs", "currency": "NOK", "region": "Europe"},

    # =========================================================================
    # SAUDI ARABIA (Tadawul)
    # =========================================================================
    {"ticker": "2222.SR", "yahoo_ticker": "2222.SR", "company_name": "Saudi Arabian Oil Group (Aramco)", "country": "Saudi Arabia", "exchange": "Tadawul", "currency": "SAR", "region": "Middle East"},
    {"ticker": "1120.SR", "yahoo_ticker": "1120.SR", "company_name": "Al Rajhi Bank", "country": "Saudi Arabia", "exchange": "Tadawul", "currency": "SAR", "region": "Middle East"},
    {"ticker": "2010.SR", "yahoo_ticker": "2010.SR", "company_name": "Saudi Basic Industries (SABIC)", "country": "Saudi Arabia", "exchange": "Tadawul", "currency": "SAR", "region": "Middle East"}
]

# Lookup Maps for fast in-memory indexing
CATALOG_BY_TICKER = {c["ticker"].upper(): c for c in GLOBAL_COMPANIES}

# Also map lowercase/normalized queries to ticker
COMPANY_ALIAS_MAP = {
    # US
    "apple": "AAPL", "aapl": "AAPL", "apple inc": "AAPL",
    "microsoft": "MSFT", "msft": "MSFT",
    "nvidia": "NVDA", "nvda": "NVDA",
    "amazon": "AMZN", "amzn": "AMZN",
    "google": "GOOGL", "googl": "GOOGL", "alphabet": "GOOGL",
    "meta": "META", "meta platforms": "META", "facebook": "META",
    "tesla": "TSLA", "tsla": "TSLA",
    "broadcom": "AVGO", "avgo": "AVGO",
    "amd": "AMD", "advanced micro devices": "AMD",
    "netflix": "NFLX", "nflx": "NFLX",
    "oracle": "ORCL", "orcl": "ORCL",
    "salesforce": "CRM", "crm": "CRM",
    "adobe": "ADBE", "adbe": "ADBE",
    "intel": "INTC", "intc": "INTC",
    "qualcomm": "QCOM", "qcom": "QCOM",
    "cisco": "CSCO", "csco": "CSCO",
    "ibm": "IBM", "uber": "UBER", "paypal": "PYPL",
    "costco": "COST", "walmart": "WMT", "coca cola": "KO", "coke": "KO", "pepsi": "PEP",
    "mcdonalds": "MCD", "nike": "NKE", "disney": "DIS",
    "jpmorgan": "JPM", "jpm": "JPM", "bank of america": "BAC", "goldman sachs": "GS",
    "visa": "V", "mastercard": "MA", "johnson & johnson": "JNJ", "pfizer": "PFE",
    "merck": "MRK", "exxon": "XOM", "chevron": "CVX",

    # India
    "tcs": "TCS.NS", "tcs.ns": "TCS.NS", "tata consultancy": "TCS.NS", "tata consultancy services": "TCS.NS",
    "infosys": "INFY.NS", "infy.ns": "INFY.NS", "infy": "INFY.NS",
    "reliance": "RELIANCE.NS", "reliance.ns": "RELIANCE.NS", "reliance industries": "RELIANCE.NS",
    "hdfc": "HDFCBANK.NS", "hdfc bank": "HDFCBANK.NS", "hdfcbank.ns": "HDFCBANK.NS",
    "icici": "ICICIBANK.NS", "icici bank": "ICICIBANK.NS",
    "sbi": "SBIN.NS", "state bank of india": "SBIN.NS",
    "airtel": "BHARTIARTL.NS", "bharti airtel": "BHARTIARTL.NS",
    "itc": "ITC.NS", "larsen": "LT.NS", "l&t": "LT.NS", "lt": "LT.NS",
    "hcl": "HCLTECH.NS", "hcl tech": "HCLTECH.NS", "wipro": "WIPRO.NS",
    "maruti": "MARUTI.NS", "maruti suzuki": "MARUTI.NS",
    "tata motors": "TATAMOTORS.NS", "sun pharma": "SUNPHARMA.NS",
    "axis bank": "AXISBANK.NS", "kotak": "KOTAKBANK.NS", "kotak mahindra": "KOTAKBANK.NS",
    "asian paints": "ASIANPAINT.NS", "bajaj finance": "BAJFINANCE.NS",
    "adani": "ADANIENT.NS", "adani enterprises": "ADANIENT.NS",
    "zomato": "ZOMATO.NS", "trent": "TRENT.NS", "titan": "TITAN.NS",

    # Japan
    "toyota": "7203.T", "7203": "7203.T", "7203.t": "7203.T", "toyota motor": "7203.T",
    "sony": "6758.T", "6758": "6758.T", "softbank": "9984.T", "keyence": "6861.T",
    "denso": "6902.T", "hitachi": "6501.T", "honda": "7267.T", "nintendo": "7974.T",
    "tokyo electron": "8035.T", "ntt": "9432.T", "fast retailing": "9983.T", "uniqlo": "9983.T",

    # Germany
    "sap": "SAP.DE", "sap.de": "SAP.DE", "siemens": "SIE.DE", "deutsche telekom": "DTE.DE",
    "allianz": "ALV.DE", "bmw": "BMW.DE", "mercedes": "MBG.DE", "mercedes-benz": "MBG.DE",
    "volkswagen": "VOW3.DE", "bayer": "BAYN.DE", "deutsche bank": "DBK.DE",
    "puma": "PUM.DE", "pum.de": "PUM.DE", "pum": "PUM.DE", "adidas": "ADS.DE",
    "basf": "BAS.DE", "infineon": "IFX.DE",

    # UK
    "astrazeneca": "AZN.L", "azn.l": "AZN.L", "shell": "SHEL.L", "hsbc": "HSBA.L",
    "unilever": "ULVR.L", "bp": "BP.L", "gsk": "GSK.L", "rio tinto": "RIO.L",
    "barclays": "BARC.L", "vodafone": "VOD.L", "lseg": "LSEG.L",

    # France
    "lvmh": "MC.PA", "mc.pa": "MC.PA", "loreal": "OR.PA", "l'oreal": "OR.PA",
    "totalenergies": "TTE.PA", "sanofi": "SAN.PA", "airbus": "AIR.PA",
    "bnp": "BNP.PA", "bnp paribas": "BNP.PA", "schneider": "SU.PA",
    "schneider electric": "SU.PA", "hermes": "RMS.PA", "kering": "KER.PA",

    # Switzerland
    "nestle": "NESN.SW", "roche": "ROG.SW", "novartis": "NOVN.SW", "ubs": "UBSG.SW",

    # South Korea
    "samsung": "005930.KS", "005930": "005930.KS", "005930.ks": "005930.KS", "samsung electronics": "005930.KS",
    "sk hynix": "000660.KS", "hyundai": "005380.KS", "hyundai motor": "005380.KS",
    "naver": "035420.KS", "kakao": "035720.KS", "lg chem": "051910.KS", "kia": "000270.KS",

    # Hong Kong & China
    "tencent": "0700.HK", "0700": "0700.HK", "0700.hk": "0700.HK",
    "alibaba": "9988.HK", "9988": "9988.HK", "baba": "BABA",
    "xiaomi": "1810.HK", "meituan": "3690.HK", "pinduoduo": "PDD", "pdd": "PDD",
    "jd": "JD", "jd.com": "9618.HK", "baidu": "BIDU", "byd": "1211.HK",
    "china mobile": "0941.HK", "nio": "NIO",

    # Canada
    "shopify": "SHOP.TO", "shop.to": "SHOP.TO", "shop": "SHOP.TO",
    "rbc": "RY.TO", "royal bank": "RY.TO", "td": "TD.TO", "td bank": "TD.TO",
    "enbridge": "ENB.TO", "canadian national": "CNR.TO",

    # Australia
    "bhp": "BHP.AX", "bhp.ax": "BHP.AX", "cba": "CBA.AX", "commonwealth bank": "CBA.AX",
    "csl": "CSL.AX", "westpac": "WBC.AX", "anz": "ANZ.AX", "nab": "NAB.AX",

    # Netherlands
    "asml": "ASML.AS", "asml.as": "ASML.AS", "adyen": "ADYEN.AS", "ing": "INGA.AS",

    # Taiwan
    "tsmc": "2330.TW", "2330": "2330.TW", "2330.tw": "2330.TW",
    "foxconn": "2317.TW", "hon hai": "2317.TW", "mediatek": "2454.TW",

    # Brazil
    "vale": "VALE3.SA", "petrobras": "PETR4.SA", "itau": "ITUB4.SA", "bradesco": "BBDC4.SA",

    # Spain, Italy, South Africa, Sweden, Denmark, Norway, Saudi Arabia
    "iberdrola": "IBE.MC", "santander": "SAN.MC", "bbva": "BBVA.MC", "inditex": "ITX.MC", "zara": "ITX.MC",
    "eni": "ENI.MI", "intesa": "ISP.MI", "enel": "ENEL.MI", "ferrari": "RACE.MI",
    "naspers": "NPN.JO", "anglo american": "AGL.JO",
    "ericsson": "ERIC-B.ST", "volvo": "VOLV-B.ST",
    "novo nordisk": "NOVO-B.CO", "maersk": "MAERSK-B.CO",
    "equinor": "EQNR.OL", "dnb": "DNB.OL",
    "aramco": "2222.SR", "saudi aramco": "2222.SR"
}

def get_all_companies():
    """Returns the full seed list of global companies."""
    return GLOBAL_COMPANIES

def get_company_by_ticker(ticker: str):
    """Finds a company in the seed catalog by ticker."""
    if not ticker:
        return None
    return CATALOG_BY_TICKER.get(ticker.strip().upper())

def get_supported_countries():
    """Returns sorted unique countries from the catalog."""
    return sorted(list(set(c["country"] for c in GLOBAL_COMPANIES)))

def get_supported_exchanges():
    """Returns sorted unique exchanges from the catalog."""
    return sorted(list(set(c["exchange"] for c in GLOBAL_COMPANIES)))
