# NoCap Stocks

Historical Stock Drop Pattern Analysis System

NoCap Stocks is a web-based historical stock analysis system that studies how stocks behaved after significant historical price drops.

Instead of speculative forecasting, the system focuses strictly on empirical historical analysis rather than future price prediction, and does **NOT** provide buy, sell, or hold recommendations.

---

## Key Features

- **Company & Ticker Resolution:** Accepts company names (e.g., Apple, Microsoft, Puma, Toyota) and stock tickers across international markets, with intelligent global search and resolution.
- **Historical Market Data Ingestion:** Fetches adjusted historical market data spanning up to 50 years via Yahoo Finance (`yfinance`).
- **Drop Event Detection:** Systematically identifies significant historical price-drop events matching configurable rolling windows and drawdown percentage thresholds.
- **Forward Horizon Returns:** Automatically tracks and calculates post-drop price trajectories across **30-day**, **90-day**, and **180-day** forward holding periods.
- **Comprehensive Statistical Synthesis:** Computes empirical metrics for each forward horizon, including:
  - Average return
  - Median return
  - Win rate (percentage of periods with positive returns)
  - Best (maximum) return
  - Worst (minimum / tail-risk) return
  - Standard deviation / return dispersion
- **Interactive Visualizations:** High-density financial charts with price history, highlighted drop event markers, trading volume bars, and forward return distributions powered by Chart.js.
- **Database & Caching Layer:** Leverages Supabase (PostgreSQL) for persistent company directory cataloging and historical pricing cache.
- **Local AI Explanations:** Employs Gemma 3 (running locally via Ollama) to synthesize and explain historical drop patterns in plain English without hallucinating unverified figures or making forward-looking investment predictions.

---

## Technology Stack

- **Backend:** Python, Flask, Flask-CORS
- **Market Data & Processing:** yfinance, pandas
- **Database & Storage:** Supabase (PostgreSQL)
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Charting & Visualization:** Chart.js, Hammer.js, chartjs-plugin-zoom
- **Local AI / LLM Layer:** Gemma 3 (`gemma3:4b`), Ollama

---

## Development Status

- Historical stock analysis: **implemented**
- Global company search: **implemented**
- Market/company resolution: **implemented**
- Supabase integration: **implemented**
- Charts and volume visualization: **implemented**
- Local Gemma/Ollama AI: **implemented/in development**
- Login/signup authentication: **NOT YET IMPLEMENTED**
- Production deployment: **NOT YET IMPLEMENTED**

---

## Project Structure

```
NoCap-Stocks/
├── backend/
│   ├── app.py                          # Flask application server, REST API endpoints & route handlers
│   ├── analysis.py                     # Historical price analysis engine, drop detection & statistics
│   ├── global_catalog.py               # International company catalog & multi-exchange ticker resolution
│   ├── global_companies_catalog.json   # Seed dataset of global companies and ticker symbols
│   ├── supabase_client.py              # Supabase client initialization and connection handling
│   ├── supabase_cache.py               # Caching layer for companies and historical price data in Supabase
│   ├── seed_companies.py               # Database seeding utility to populate Supabase from catalog
│   ├── patch_chat.py                   # Chat and explanation context helper
│   ├── requirements.txt                # Python package dependencies
│   ├── test_chat.py                    # Backend test script for chat interaction
│   ├── test_resolve.py                 # Backend test script for ticker resolution
│   └── scratch_*.py                    # Internal test and verification utility scripts
├── frontend/
│   ├── index.html                      # Terminal user interface layout and DOM structure
│   ├── style.css                       # Styling tokens, responsive layout, dark theme & chat styles
│   ├── script.js                       # Frontend client logic, Chart.js graphs, table sorting & API client
│   ├── CompanyLogo.js                  # Dynamic company logo loader and fallback icons
│   └── default_aapl.json               # Default offline fallback dataset for Apple Inc. (AAPL)
├── .env.example                        # Template environment configuration file
├── .gitignore                          # Git rules ignoring credentials, cache, and virtual environments
├── README.md                           # Project documentation and setup guide
├── supabase_setup.sql                  # Database migration schema, table definitions & RLS policies
├── scratch_test_gemma_explain.py       # Script demonstrating local Gemma 3 historical explanation via Ollama
└── scratch_test_ollama.py              # Connectivity check script for local Ollama API
```

---

## Setup & Installation

### 1. Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) (for running the local Gemma 3 AI model)
- Modern web browser (Chrome, Edge, Firefox, Safari)

---

### 2. Environment Configuration

Copy the template configuration file:

```bash
cp .env.example .env
```

Open `.env` and configure your environment variables. **Never commit actual secret values to version control.**

```env
# Flask Backend Server Configuration
HOST=127.0.0.1
PORT=5000
FLASK_ENV=development
FLASK_DEBUG=True

# Supabase Credentials (Optional for local caching)
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Local AI / Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
GEMMA_MODEL=gemma3:4b
```

---

### 3. Install Python Dependencies

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r backend/requirements.txt
```

---

### 4. Set Up Local AI (Gemma 3 via Ollama)

If using the local AI explanation features, start Ollama and pull the Gemma 3 model:

```bash
ollama serve
ollama run gemma3:4b
```

---

### 5. Database Setup (Supabase — Optional)

If using Supabase for catalog persistence and caching:
1. Create a Supabase project at [supabase.com](https://supabase.com).
2. Open the SQL Editor in your Supabase dashboard.
3. Run the SQL statements found in `supabase_setup.sql`.
4. (Optional) Populate the company directory:
   ```bash
   python backend/seed_companies.py
   ```

---

### 6. Start the Flask Backend

Run the Flask server:

```bash
python backend/app.py
```

*The API will start at `http://127.0.0.1:5000`.*

---

### 7. Start the Frontend

In a separate terminal window, serve the frontend:

```bash
cd frontend
python -m http.server 8000
```

Open your browser and navigate to:

```
http://localhost:8000
```

---

## Disclaimer

*NoCap Stocks is designed strictly for educational, research, and empirical study purposes. It does not provide financial advice, price targets, buy/sell recommendations, or future market guarantees. Past historical performance is never an indicator of future market returns.*
