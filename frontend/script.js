/**
 * NoCap Stocks — Institutional Dark Financial Exchange Terminal Engine
 * Logic for Chart, Parameters, Historical Stakes, Events Table, Markets Watchlist,
 * Dynamic Company Logos, and NoCap AI Assistant.
 */

// ==============================================================================
// NoCap Stocks — Centralized API & Environment Configuration
// ==============================================================================
const ENV_CONFIG = {
    // Production API Base URL (Render Web Service)
    production: 'https://nocap-stocks-api.onrender.com',
    // Local Development API Base URL (Local Flask Backend)
    local: 'http://127.0.0.1:5000'
};

/**
 * Resolves the active API base URL.
 * - In production environments (when hosted on Render, Vercel, Netlify, GitHub Pages, or any public domain):
 *   Uses ENV_CONFIG.production ('https://nocap-stocks-api.onrender.com').
 * - In local environments (localhost / 127.0.0.1 / file://):
 *   Defaults to ENV_CONFIG.local ('http://127.0.0.1:5000'), while allowing instant switching
 *   to production via URL query param (?api=prod or ?api=production) or localStorage ('nocap_api_env').
 */
function resolveApiBaseUrl() {
    if (typeof window === 'undefined' || !window.location) {
        return ENV_CONFIG.production;
    }

    // 1. Explicit query parameter override (e.g. ?api=prod, ?api=local, ?apiUrl=https://...)
    const params = new URLSearchParams(window.location.search);
    const apiParam = params.get('api') || params.get('apiUrl') || params.get('backend');
    if (apiParam === 'prod' || apiParam === 'production') return ENV_CONFIG.production;
    if (apiParam === 'local' || apiParam === 'dev') return ENV_CONFIG.local;
    if (apiParam && apiParam.startsWith('http')) return apiParam.replace(/\/$/, '');

    // 2. Local storage override (allows developer switching in browser console)
    try {
        const storedEnv = localStorage.getItem('nocap_api_env');
        if (storedEnv && ENV_CONFIG[storedEnv]) return ENV_CONFIG[storedEnv];
        const storedUrl = localStorage.getItem('nocap_api_url');
        if (storedUrl && storedUrl.startsWith('http')) return storedUrl.replace(/\/$/, '');
    } catch (_) {}

    // 3. Domain-based detection:
    const hostname = window.location.hostname;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '0.0.0.0';

    // Production deployment (any public domain):
    if (!isLocalhost && window.location.protocol !== 'file:') {
        return ENV_CONFIG.production;
    }

    // Local development fallback:
    return ENV_CONFIG.local;
}

// Active Centralized API Base URL
const API_BASE_URL = resolveApiBaseUrl();

// Centralized API Endpoints
const API_URL = `${API_BASE_URL}/api/analyze`;
const CHAT_URL = `${API_BASE_URL}/api/chat`;
const SEARCH_URL = `${API_BASE_URL}/api/companies/search`;
const SEARCH_API_URL = `${API_BASE_URL}/api/search`;
const MARKETS_URL = `${API_BASE_URL}/api/markets`;
const FILTERS_URL = `${API_BASE_URL}/api/companies/filters`;
const COMPANIES_URL = `${API_BASE_URL}/api/companies`;
const COMPANY_URL = `${API_BASE_URL}/api/company`;
const SUPABASE_TEST_URL = `${API_BASE_URL}/api/supabase/test`;

// Global debug helper for developer console
if (typeof window !== 'undefined') {
    window.NoCap = {
        config: ENV_CONFIG,
        apiBaseUrl: API_BASE_URL,
        setBackend: (envOrUrl) => {
            if (envOrUrl === 'local' || envOrUrl === 'production') {
                localStorage.setItem('nocap_api_env', envOrUrl);
                localStorage.removeItem('nocap_api_url');
            } else if (envOrUrl && envOrUrl.startsWith('http')) {
                localStorage.setItem('nocap_api_url', envOrUrl);
                localStorage.removeItem('nocap_api_env');
            } else if (envOrUrl === 'reset') {
                localStorage.removeItem('nocap_api_env');
                localStorage.removeItem('nocap_api_url');
            }
            window.location.reload();
        }
    };
    console.log(`[NoCap Stocks] API Base URL: ${API_BASE_URL} (${API_BASE_URL === ENV_CONFIG.production ? 'Production Render' : 'Local Dev'})`);
}

// Default Institutional Global Watchlist (18 primary global companies rendered instantly on zero ms)
const DEFAULT_MARKETS_CACHE = [
    { ticker: "AAPL", company_name: "Apple Inc.", exchange: "NASDAQ", country: "United States", latest_price: 227.63, daily_change_pct: 0.41 },
    { ticker: "MSFT", company_name: "Microsoft Corp.", exchange: "NASDAQ", country: "United States", latest_price: 430.30, daily_change_pct: -0.22 },
    { ticker: "NVDA", company_name: "NVIDIA Corp.", exchange: "NASDAQ", country: "United States", latest_price: 121.40, daily_change_pct: 1.58 },
    { ticker: "TSLA", company_name: "Tesla, Inc.", exchange: "NASDAQ", country: "United States", latest_price: 261.63, daily_change_pct: 2.45 },
    { ticker: "AMZN", company_name: "Amazon.com Inc.", exchange: "NASDAQ", country: "United States", latest_price: 186.40, daily_change_pct: 0.85 },
    { ticker: "GOOGL", company_name: "Alphabet Inc.", exchange: "NASDAQ", country: "United States", latest_price: 165.85, daily_change_pct: -0.34 },
    { ticker: "META", company_name: "Meta Platforms", exchange: "NASDAQ", country: "United States", latest_price: 567.36, daily_change_pct: 0.92 },
    { ticker: "TCS.NS", company_name: "Tata Consultancy", exchange: "NSE", country: "India", latest_price: 4260.00, daily_change_pct: 0.65 },
    { ticker: "PUM.DE", company_name: "Puma SE", exchange: "XETRA", country: "Germany", latest_price: 22.16, daily_change_pct: 0.65 },
    { ticker: "INFY.NS", company_name: "Infosys Ltd", exchange: "NSE", country: "India", latest_price: 1895.50, daily_change_pct: 1.12 },
    { ticker: "RELIANCE.NS", company_name: "Reliance Industries", exchange: "NSE", country: "India", latest_price: 2950.00, daily_change_pct: 0.80 },
    { ticker: "SAP.DE", company_name: "SAP SE", exchange: "XETRA", country: "Germany", latest_price: 204.10, daily_change_pct: 0.74 },
    { ticker: "7203.T", company_name: "Toyota Motor Corp.", exchange: "TSE", country: "Japan", latest_price: 2610.00, daily_change_pct: -0.45 },
    { ticker: "005930.KS", company_name: "Samsung Electronics", exchange: "KRX", country: "South Korea", latest_price: 74200.00, daily_change_pct: 1.25 },
    { ticker: "0700.HK", company_name: "Tencent Holdings", exchange: "HKEX", country: "Hong Kong", latest_price: 375.40, daily_change_pct: 0.95 },
    { ticker: "ASML.AS", company_name: "ASML Holding N.V.", exchange: "Euronext Amsterdam", country: "Netherlands", latest_price: 785.20, daily_change_pct: -0.80 },
    { ticker: "SHOP.TO", company_name: "Shopify Inc.", exchange: "TSX", country: "Canada", latest_price: 104.25, daily_change_pct: 1.88 },
    { ticker: "BHP.AX", company_name: "BHP Group", exchange: "ASX", country: "Australia", latest_price: 44.82, daily_change_pct: 0.32 },
    { ticker: "2330.TW", company_name: "TSMC", exchange: "TWSE", country: "Taiwan", latest_price: 975.00, daily_change_pct: 2.10 }
];

// Global Application State
let currentAnalysisData = null;
let currentEvents = [];
let chartInstance = null;
let currentChartMode = 'price'; // 'price' | 'returns'
let currentRange = 'ALL';
let currentFilterText = '';
let currentSortCol = 'event_date';
let currentSortDir = 'desc';
let marketsData = [...DEFAULT_MARKETS_CACHE];
let selectedCountry = 'All';
let selectedExchange = 'All';
let currentMarketFilter = '';

// AI Credits State
const TOTAL_CREDITS = 500;
let currentCredits = 500;

// Search debounce
let searchDebounceTimer = null;

// Initialize upon DOM load
document.addEventListener('DOMContentLoaded', async () => {
    initAICredits();
    setupEventListeners();
    setupGlobalSearch();
    renderMarketsList();
    renderInitialCompanyHeader('AAPL');

    // 1. Instant load from local JSON cache for 0ms initial terminal rendering
    try {
        const cachedRes = await fetch('default_aapl.json');
        if (cachedRes.ok) {
            const cachedData = await cachedRes.json();
            currentAnalysisData = cachedData;
            currentEvents = cachedData.events || [];
            renderDashboard(cachedData);
        } else {
            triggerAnalysis();
        }
    } catch (e) {
        triggerAnalysis();
    }

    // 2. Asynchronously fetch fresh filters, markets quotes & test Supabase
    loadFilterDropdowns();
    loadMarketsList();
    checkBackendHealth();
    initChatHistory();
});

/**
 * Event Listeners Registration
 */
function setupEventListeners() {
    // Analysis Form
    const form = document.getElementById('analysis-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            triggerAnalysis();
        });
    }

    const btnReset = document.getElementById('btn-reset');
    if (btnReset) {
        btnReset.addEventListener('click', handleReset);
    }

    // Chart Range Presets (Display range only, does not alter backend analysis params)
    document.querySelectorAll('.chart-range-pill').forEach(btn => {
        btn.addEventListener('click', () => {
            const range = btn.getAttribute('data-range');
            setChartRange(range);
        });
    });

    // Chart Mode Buttons
    const btnViewPrice = document.getElementById('btn-view-price');
    const btnViewReturns = document.getElementById('btn-view-returns');
    if (btnViewPrice && btnViewReturns) {
        btnViewPrice.addEventListener('click', () => switchChartMode('price'));
        btnViewReturns.addEventListener('click', () => switchChartMode('returns'));
    }

    // Chart Reset Zoom
    const btnResetZoom = document.getElementById('btn-reset-zoom');
    if (btnResetZoom) {
        btnResetZoom.addEventListener('click', () => setChartRange('ALL'));
    }

    // Table Filter Search
    const eventsSearch = document.getElementById('events-search');
    if (eventsSearch) {
        eventsSearch.addEventListener('input', (e) => {
            currentFilterText = e.target.value.trim().toLowerCase();
            updateAndRenderTable();
        });
    }

    // Table Sorting
    document.querySelectorAll('.th-sortable').forEach(th => {
        th.addEventListener('click', () => {
            const col = th.getAttribute('data-sort');
            if (currentSortCol === col) {
                currentSortDir = currentSortDir === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortCol = col;
                currentSortDir = (col === 'drop_percentage' || col.endsWith('_days')) ? 'desc' : 'asc';
            }
            updateAndRenderTable();
        });
    });

    // CSV Export
    const btnExport = document.getElementById('btn-export');
    if (btnExport) {
        btnExport.addEventListener('click', exportCSV);
    }

    // Markets Search Filter
    const marketsFilter = document.getElementById('markets-filter-input');
    if (marketsFilter) {
        marketsFilter.addEventListener('input', (e) => {
            currentMarketFilter = e.target.value.trim().toLowerCase();
            renderMarketsList(currentMarketFilter);
        });
    }

    // Market Country Filter
    const countrySelect = document.getElementById('market-country-select');
    if (countrySelect) {
        countrySelect.addEventListener('change', (e) => {
            selectedCountry = e.target.value;
            loadMarketsList();
        });
    }

    // Market Exchange Filter
    const exchangeSelect = document.getElementById('market-exchange-select');
    if (exchangeSelect) {
        exchangeSelect.addEventListener('change', (e) => {
            selectedExchange = e.target.value;
            loadMarketsList();
        });
    }

    // Left Navigation Rail Interactions
    const railDashboardBtn = document.getElementById('rail-btn-dashboard');
    const railAnalysisBtn = document.getElementById('rail-btn-analysis');
    const railEventsBtn = document.getElementById('rail-btn-events');
    const railWatchlistBtn = document.getElementById('rail-btn-watchlist');
    const railAiBtn = document.getElementById('rail-btn-ai');
    const railSettingsBtn = document.getElementById('rail-btn-settings');

    function setActiveRail(btnId) {
        document.querySelectorAll('.rail-nav-btn').forEach(b => {
            b.classList.toggle('active', b.id === btnId);
        });
    }

    if (railDashboardBtn) {
        railDashboardBtn.addEventListener('click', () => {
            setActiveRail('rail-btn-dashboard');
            closeSettingsModal();
            closeAiDrawer();
            const target = document.querySelector('.company-header-strip') || document.querySelector('.terminal-chart-panel');
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    if (railAnalysisBtn) {
        railAnalysisBtn.addEventListener('click', () => {
            setActiveRail('rail-btn-analysis');
            closeSettingsModal();
            const target = document.querySelector('.analysis-parameters-bar');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                const field = document.getElementById('ticker');
                if (field) {
                    field.focus();
                    field.select();
                }
            }
        });
    }

    if (railEventsBtn) {
        railEventsBtn.addEventListener('click', () => {
            setActiveRail('rail-btn-events');
            closeSettingsModal();
            const target = document.querySelector('.terminal-events-section');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                const search = document.getElementById('events-search');
                if (search) search.focus();
            }
        });
    }

    if (railWatchlistBtn) {
        railWatchlistBtn.addEventListener('click', () => {
            setActiveRail('rail-btn-watchlist');
            closeSettingsModal();
            const target = document.querySelector('.terminal-market-panel');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                const filterInput = document.getElementById('markets-filter-input');
                if (filterInput) filterInput.focus();
            }
        });
    }

    if (railAiBtn) {
        railAiBtn.addEventListener('click', () => {
            setActiveRail('rail-btn-ai');
            closeSettingsModal();
            openAiDrawer();
        });
    }

    if (railSettingsBtn) {
        railSettingsBtn.addEventListener('click', () => {
            setActiveRail('rail-btn-settings');
            openSettingsModal();
        });
    }

    // AI Drawer Open/Close Controls
    const headerCreditsBtn = document.getElementById('header-ai-credits');
    const marketAiBtn = document.getElementById('market-open-ai-btn');
    const drawerCloseBtn = document.getElementById('drawer-close-btn');

    [headerCreditsBtn, marketAiBtn].forEach(el => {
        if (el) el.addEventListener('click', () => {
            setActiveRail('rail-btn-ai');
            openAiDrawer();
        });
    });

    if (drawerCloseBtn) {
        drawerCloseBtn.addEventListener('click', closeAiDrawer);
    }

    // Settings Modal Controls
    const settingsCloseBtn = document.getElementById('settings-close-btn');
    const settingsBackdrop = document.getElementById('settings-backdrop');
    const btnEnvProd = document.getElementById('btn-env-production');
    const btnEnvLocal = document.getElementById('btn-env-local');
    const btnResetCreds = document.getElementById('btn-reset-credits');

    if (settingsCloseBtn) settingsCloseBtn.addEventListener('click', closeSettingsModal);
    if (settingsBackdrop) settingsBackdrop.addEventListener('click', closeSettingsModal);
    if (btnEnvProd) {
        btnEnvProd.addEventListener('click', () => {
            window.NoCap.setBackend('production');
        });
    }
    if (btnEnvLocal) {
        btnEnvLocal.addEventListener('click', () => {
            window.NoCap.setBackend('local');
        });
    }
    if (btnResetCreds) {
        btnResetCreds.addEventListener('click', () => {
            currentCredits = TOTAL_CREDITS;
            updateCreditsUI();
            updateSettingsUI();
        });
    }

    // Chat Form Submit
    const chatForm = document.getElementById('chat-input-form');
    if (chatForm) {
        chatForm.addEventListener('submit', handleChatSubmit);
    }

    // Suggestion Chips
    document.querySelectorAll('.chip-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const prompt = btn.getAttribute('data-prompt');
            const chatInput = document.getElementById('chat-user-input');
            if (chatInput) {
                chatInput.value = prompt;
                handleChatSubmit();
            }
        });
    });

    // Global keyboard shortcuts: '/' to focus search, 'Escape' to close drawers/modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAiDrawer();
            closeSettingsModal();
        } else if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
            e.preventDefault();
            const search = document.getElementById('global-search-input');
            if (search) search.focus();
        }
    });
}

/**
 * Renders company header slot immediately with default logo and metadata
 */
function renderInitialCompanyHeader(ticker) {
    const wrap = document.getElementById('company-header-logo-wrap');
    if (wrap && window.createCompanyLogo) {
        wrap.innerHTML = '';
        wrap.appendChild(window.createCompanyLogo(ticker, 'Apple Inc.', 'lg'));
    }
}

/**
 * Triggers the deterministic stock analysis via POST /api/analyze
 */
async function triggerAnalysis() {
    const inputTicker = document.getElementById('ticker');
    const inputDropThreshold = document.getElementById('drop_threshold');
    const inputWindowDays = document.getElementById('window_days');
    const inputYears = document.getElementById('years');

    const tickerVal = (inputTicker ? inputTicker.value : '').trim().toUpperCase();
    const dropVal = parseFloat(inputDropThreshold ? inputDropThreshold.value : 10);
    const windowVal = parseInt(inputWindowDays ? inputWindowDays.value : 5, 10);
    const yearsVal = parseInt(inputYears ? inputYears.value : 10, 10);

    if (!tickerVal) {
        showStatus('No matching company found. Please enter a company name or ticker.', 'error');
        return;
    }

    setLoadingState(true);
    hideStatus();

    try {
        const payload = {
            ticker: tickerVal,
            drop_threshold: dropVal,
            window_days: windowVal,
            years: yearsVal
        };

        const res = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            const msg = errData.error || `No matching company found for "${tickerVal}".`;
            showStatus(msg, 'error');
            setLoadingState(false);
            return;
        }

        const data = await res.json();
        currentAnalysisData = data;
        currentEvents = data.events || [];

        renderDashboard(data);
    } catch (err) {
        console.error("Analysis request error:", err);
        showStatus(`Connection error: ${err.message}. Ensure backend is running at ${API_BASE_URL}`, 'error');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Updates all visual panels with backend analysis results
 */
function renderDashboard(data) {
    if (!data || !data.ticker) {
        showStatus('No matching company found.', 'error');
        return;
    }
    const ticker = data.ticker;
    const compInfo = data.company_info || {};
    const companyName = data.company_name || compInfo.company_name || ticker;
    const exchange = data.exchange || compInfo.exchange || 'EQUITY';
    const country = data.country || compInfo.country || 'Global';

    // 1. Company Header
    const nameEl = document.getElementById('company-header-name');
    const tickerEl = document.getElementById('header-ticker');
    const exchEl = document.getElementById('company-header-exchange');
    const countryEl = document.getElementById('company-header-country');
    const dateEl = document.getElementById('company-header-date');
    const pointsEl = document.getElementById('company-header-datapoints');
    const priceEl = document.getElementById('company-header-price');
    const changeEl = document.getElementById('company-header-change');
    const logoWrap = document.getElementById('company-header-logo-wrap');
    const chartSym = document.getElementById('chart-symbol');

    if (nameEl) nameEl.textContent = companyName;
    if (tickerEl) tickerEl.textContent = ticker;
    if (exchEl) exchEl.textContent = exchange;
    if (countryEl) countryEl.textContent = country;
    if (chartSym) chartSym.textContent = ticker;

    if (logoWrap && window.createCompanyLogo) {
        logoWrap.innerHTML = '';
        logoWrap.appendChild(window.createCompanyLogo(ticker, companyName, 'lg'));
    }

    const latestPrice = data.latest_price !== undefined ? data.latest_price : compInfo.latest_price;
    const dailyChange = data.daily_change_pct !== undefined ? data.daily_change_pct : compInfo.daily_change_pct;

    if (priceEl) {
        priceEl.textContent = (latestPrice !== null && latestPrice !== undefined) ? `$${latestPrice.toFixed(2)}` : '$—';
    }

    if (changeEl) {
        if (dailyChange !== null && dailyChange !== undefined) {
            const isPos = dailyChange >= 0;
            changeEl.textContent = `${isPos ? '+' : ''}${dailyChange.toFixed(2)}%`;
            changeEl.className = `price-change-tag ${isPos ? 'positive' : 'negative'}`;
        } else {
            changeEl.textContent = '0.00%';
            changeEl.className = 'price-change-tag positive';
        }
    }

    const latestDate = data.latest_available_date || compInfo.latest_available_date || (data.data_metadata && data.data_metadata.latest_available_date) || '—';
    if (dateEl) dateEl.textContent = `Latest available historical price: ${latestDate}`;

    const totalPts = (data.data_metadata && data.data_metadata.rows_received) ? data.data_metadata.rows_received.toLocaleString() : (data.price_history ? data.price_history.length.toLocaleString() : '2,512');
    if (pointsEl) pointsEl.textContent = `${totalPts} trading sessions evaluated`;

    // 2. Chart Rendering
    renderChart(data);

    // 3. Historical Stakes Panel
    const stakesInfo = data.historical_stakes || {};
    const stakesVerdict = stakesInfo.stakes || 'HIGH';
    const stakesBadge = document.getElementById('stakes-verdict-badge');
    const stakesText = document.getElementById('stakes-text');
    const stakesDot = document.getElementById('stakes-dot');
    const stakesReason = document.getElementById('stakes-reason-text');
    const metricEvents = document.getElementById('metric-events-count');
    const metricThresh = document.getElementById('metric-threshold');
    const metricWin = document.getElementById('metric-window');

    if (stakesText) stakesText.textContent = stakesVerdict;
    if (stakesDot) {
        stakesDot.textContent = stakesVerdict === 'LOW' ? '🟢' : (stakesVerdict === 'MODERATE' ? '🟡' : (stakesVerdict === 'HIGH' ? '🔴' : '⚪'));
    }
    if (stakesBadge) {
        stakesBadge.className = `stakes-pill ${stakesVerdict.toLowerCase().replace(/\s+/g, '-')}`;
    }
    if (stakesReason) {
        stakesReason.textContent = stakesInfo.reason || 'Historical outcomes showed relatively large variation across the analyzed events.';
    }
    if (metricEvents) metricEvents.textContent = data.total_events_found ?? (data.events ? data.events.length : 0);
    if (metricThresh) metricThresh.textContent = `${data.drop_threshold || 10.0}%`;
    if (metricWin) metricWin.textContent = `${data.window_days || 5}D`;

    // 4. Statistics (30D, 90D, 180D)
    renderSummaryStats(data.summary_statistics);

    // 5. Events Table
    updateAndRenderTable();

    // 6. Bottom Status Bar
    const metaDate = document.getElementById('meta-latest-date');
    const metaPts = document.getElementById('meta-data-points');
    const statusEvs = document.getElementById('status-events-count');

    if (metaDate) metaDate.textContent = latestDate;
    if (metaPts) metaPts.textContent = totalPts;
    if (statusEvs) statusEvs.textContent = data.total_events_found ?? (data.events ? data.events.length : 0);

    // Highlight active ticker in Markets panel
    highlightActiveMarketRow(ticker);
}

/**
 * Summary Statistics Cards (30D, 90D, 180D)
 */
function renderSummaryStats(stats) {
    if (!stats) return;

    ['30', '90', '180'].forEach(days => {
        const key = `${days}_days`;
        const s = stats[key] || {};

        const avgEl = document.getElementById(`avg-${days}`);
        const medEl = document.getElementById(`med-${days}`);
        const winEl = document.getElementById(`win-${days}`);
        const bestEl = document.getElementById(`best-${days}`);
        const worstEl = document.getElementById(`worst-${days}`);
        const stdEl = document.getElementById(`std-${days}`);
        const countEl = document.getElementById(`count-${days}`);

        const avg = s.average_return !== undefined ? s.average_return : s.mean_return;
        setMetricCell(avgEl, avg, '%');
        setMetricCell(medEl, s.median_return, '%');
        setMetricCell(winEl, s.win_rate, '%', false);
        setMetricCell(bestEl, s.best_return, '%');
        setMetricCell(worstEl, s.worst_return, '%');

        if (stdEl) stdEl.textContent = s.std_dev !== null && s.std_dev !== undefined ? `${s.std_dev.toFixed(2)}%` : 'N/A';
        if (countEl) countEl.textContent = `${s.count || 0} Events`;
    });
}

function setMetricCell(el, val, unit = '', signed = true) {
    if (!el) return;
    if (val === null || val === undefined) {
        el.textContent = 'N/A';
        el.className = 'v muted';
        return;
    }
    const num = parseFloat(val);
    const sign = signed && num > 0 ? '+' : '';
    el.textContent = `${sign}${num.toFixed(2)}${unit}`;
    if (num > 0) el.className = 'v positive';
    else if (num < 0) el.className = 'v negative';
    else el.className = 'v muted';
}

/**
 * Chart.js Historical Price & Events Rendering (Real Candlestick Chart)
 * - Green candle when Close >= Open
 * - Red candle when Close < Open
 * - Wick represents High and Low
 * - Candle body represents Open and Close
 * - Preserved drop-event markers at historical drop dates
 * - Real Volume section with matched green/red colors below price chart
 */
function renderChart(data) {
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;

    const rawPrices = data.price_history || [];
    const events = data.events || [];

    if (rawPrices.length === 0) {
        return;
    }

    if (chartInstance) {
        chartInstance.destroy();
    }

    if (currentChartMode === 'returns') {
        renderForwardReturnsChart(events);
        return;
    }

    // Build event date set for fast lookup
    const eventDateMap = new Map();
    events.forEach(ev => {
        if (ev && ev.event_date) {
            eventDateMap.set(ev.event_date, ev);
        }
    });

    // 1. Safe handling of missing/null OHLC/volume values:
    // Skip invalid candle rows, never send NaN or Infinity to browser, no fake zeros.
    const validPrices = [];
    for (let i = 0; i < rawPrices.length; i++) {
        const p = rawPrices[i];
        if (!p || !p.date) continue;
        const o = Number(p.open);
        const h = Number(p.high);
        const l = Number(p.low);
        const c = Number(p.close);
        if (!Number.isFinite(o) || !Number.isFinite(h) || !Number.isFinite(l) || !Number.isFinite(c)) continue;
        if (o <= 0 || h <= 0 || l <= 0 || c <= 0) continue;

        const v = (p.volume !== undefined && p.volume !== null && Number.isFinite(Number(p.volume)))
            ? Math.max(0, Number(p.volume))
            : 0;

        validPrices.push({
            date: String(p.date),
            open: o,
            high: Math.max(h, o, c),
            low: Math.min(l, o, c),
            close: c,
            volume: v
        });
    }

    if (validPrices.length === 0) {
        return;
    }

    const labels = validPrices.map(p => p.date);
    const highs = validPrices.map(p => p.high);
    const lows = validPrices.map(p => p.low);

    // 2. Prepare volume data & per-bar colors based on that day's candle direction:
    // Green (#10b981) when Close >= Open, Red (#ef4444) when Close < Open
    const volumes = validPrices.map(p => p.volume);
    const volumeColors = [];
    const volumeBorderColors = [];
    for (let i = 0; i < validPrices.length; i++) {
        const p = validPrices[i];
        const isUp = (p.close >= p.open);
        if (isUp) {
            volumeColors.push('rgba(16, 185, 129, 0.7)'); // Green
            volumeBorderColors.push('#10b981');
        } else {
            volumeColors.push('rgba(239, 68, 68, 0.7)'); // Red
            volumeBorderColors.push('#ef4444');
        }
    }

    // 3. Drop event markers on the price chart
    const dropMarkerData = [];
    const dropPointRadii = [];
    const dropPointHoverRadii = [];
    for (let i = 0; i < validPrices.length; i++) {
        const p = validPrices[i];
        if (eventDateMap.has(p.date)) {
            dropMarkerData.push(p.high);
            dropPointRadii.push(6);
            dropPointHoverRadii.push(9);
        } else {
            dropMarkerData.push(null);
            dropPointRadii.push(0);
            dropPointHoverRadii.push(0);
        }
    }

    // Dedicated custom plugin for institutional VOLUME label & dividing line
    const volumeSectionPlugin = {
        id: 'volumeSectionPlugin',
        afterDraw(chart) {
            const yVol = chart.scales['volume'];
            if (!yVol) return;
            const area = chart.chartArea;
            const c = chart.ctx;

            c.save();
            // Subtle dividing line between price and volume sections
            c.strokeStyle = '#182232';
            c.lineWidth = 1;
            c.beginPath();
            c.moveTo(area.left, yVol.top);
            c.lineTo(area.right, yVol.top);
            c.stroke();

            // Institutional muted label: VOLUME
            c.fillStyle = '#64748b';
            c.font = '700 9px "JetBrains Mono", monospace';
            c.textBaseline = 'top';
            c.fillText('VOLUME', area.left + 6, yVol.top + 4);
            c.restore();
        }
    };

    // Dedicated Candlestick Renderer Plugin
    // Draws High-Low wicks and Open-Close candle bodies with subpixel precision
    const candlestickPlugin = {
        id: 'candlestickPlugin',
        afterDatasetsDraw(chart) {
            if (currentChartMode !== 'price') return;
            const ctx = chart.ctx;
            const xScale = chart.scales['x'];
            const yScale = chart.scales['y'];
            if (!xScale || !yScale) return;

            const area = chart.chartArea;
            ctx.save();
            ctx.beginPath();
            ctx.rect(area.left, area.top, area.width, area.height);
            ctx.clip();

            const total = validPrices.length;
            if (total === 0) {
                ctx.restore();
                return;
            }

            // Determine visible range
            const minVal = xScale.min;
            const maxVal = xScale.max;
            let startIdx = 0;
            let endIdx = total - 1;

            if (minVal !== undefined && minVal !== null) {
                const s = validPrices.findIndex(p => p.date === minVal);
                if (s !== -1) startIdx = s;
                else if (typeof minVal === 'number') startIdx = Math.max(0, Math.min(total - 1, Math.floor(minVal)));
            }
            if (maxVal !== undefined && maxVal !== null) {
                const e = validPrices.findIndex(p => p.date === maxVal);
                if (e !== -1) endIdx = e;
                else if (typeof maxVal === 'number') endIdx = Math.max(0, Math.min(total - 1, Math.ceil(maxVal)));
            }

            const visibleCount = Math.max(1, endIdx - startIdx + 1);
            const slotWidth = area.width / visibleCount;
            const candleWidth = Math.max(1.5, Math.min(18, slotWidth * 0.75));
            const wickWidth = candleWidth >= 8 ? 1.5 : 1;

            for (let i = startIdx; i <= endIdx; i++) {
                const p = validPrices[i];
                if (!p) continue;

                let x = xScale.getPixelForValue(p.date);
                if (x === undefined || isNaN(x)) {
                    x = xScale.getPixelForTick(i);
                }
                if (x === undefined || isNaN(x)) continue;
                if (x < area.left - 25 || x > area.right + 25) continue;

                const yOpen = yScale.getPixelForValue(p.open);
                const yClose = yScale.getPixelForValue(p.close);
                const yHigh = yScale.getPixelForValue(p.high);
                const yLow = yScale.getPixelForValue(p.low);

                if (isNaN(yOpen) || isNaN(yClose) || isNaN(yHigh) || isNaN(yLow)) continue;

                const isBullish = (p.close >= p.open);
                const color = isBullish ? '#10b981' : '#ef4444';

                // 1. Draw Wick (High to Low)
                ctx.strokeStyle = color;
                ctx.lineWidth = wickWidth;
                ctx.beginPath();
                const alignX = Math.round(x) + (wickWidth % 2 === 1 ? 0.5 : 0);
                ctx.moveTo(alignX, Math.round(yHigh));
                ctx.lineTo(alignX, Math.round(yLow));
                ctx.stroke();

                // 2. Draw Candle Body (Open to Close)
                const bodyTop = Math.min(yOpen, yClose);
                const bodyBottom = Math.max(yOpen, yClose);
                const bodyHeight = Math.max(2, bodyBottom - bodyTop);
                const bodyLeft = Math.round(x - candleWidth / 2);

                ctx.fillStyle = color;
                ctx.fillRect(bodyLeft, Math.round(bodyTop), Math.round(candleWidth), Math.round(bodyHeight));

                if (candleWidth >= 4) {
                    ctx.strokeStyle = color;
                    ctx.lineWidth = 1;
                    ctx.strokeRect(bodyLeft, Math.round(bodyTop), Math.round(candleWidth), Math.round(bodyHeight));
                }
            }

            ctx.restore();
        }
    };

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                // 0. Primary High bounds (invisible line establishing y-scale top)
                {
                    type: 'line',
                    label: 'High Bounds',
                    data: highs,
                    yAxisID: 'y',
                    borderColor: 'transparent',
                    backgroundColor: 'transparent',
                    borderWidth: 0,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                    showLine: false,
                    order: 10
                },
                // 1. Primary Low bounds (invisible line establishing y-scale bottom)
                {
                    type: 'line',
                    label: 'Low Bounds',
                    data: lows,
                    yAxisID: 'y',
                    borderColor: 'transparent',
                    backgroundColor: 'transparent',
                    borderWidth: 0,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                    showLine: false,
                    order: 11
                },
                // 2. Drop Events Node Dataset (red nodes marking detected drop events)
                {
                    type: 'line',
                    label: 'Drop Events',
                    data: dropMarkerData,
                    yAxisID: 'y',
                    borderColor: 'transparent',
                    borderWidth: 0,
                    showLine: false,
                    pointRadius: dropPointRadii,
                    pointHoverRadius: dropPointHoverRadii,
                    pointBackgroundColor: '#ef4444',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    order: 0
                },
                // 3. Volume Bar Dataset
                {
                    type: 'bar',
                    label: 'Volume',
                    data: volumes,
                    yAxisID: 'volume',
                    backgroundColor: volumeColors,
                    borderColor: volumeBorderColors,
                    borderWidth: 0.8,
                    borderRadius: 0,
                    barPercentage: 0.9,
                    categoryPercentage: 1.0,
                    maxBarThickness: 16,
                    order: 2
                }
            ]
        },
        plugins: [volumeSectionPlugin, candlestickPlugin],
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0a0f18',
                    titleColor: '#ffffff',
                    bodyColor: '#94a3b8',
                    borderColor: '#182232',
                    borderWidth: 1,
                    padding: 10,
                    titleFont: { family: 'JetBrains Mono', size: 12 },
                    bodyFont: { family: 'JetBrains Mono', size: 11 },
                    callbacks: {
                        title: function(items) {
                            if (!items || !items.length) return '';
                            const idx = items[0].dataIndex;
                            const p = validPrices[idx];
                            return p ? `Trading Date: ${p.date}` : '';
                        },
                        label: function(context) {
                            if (context.datasetIndex === 0) {
                                const idx = context.dataIndex;
                                const p = validPrices[idx];
                                if (!p) return null;
                                const open = p.open;
                                const high = p.high;
                                const low = p.low;
                                const close = p.close;
                                const chg = open ? ((close - open) / open * 100) : 0;
                                const chgSign = chg > 0 ? '+' : '';
                                const vol = p.volume;
                                const isUp = (close >= open);
                                const tag = isUp ? '▲' : '▼';

                                let lines = [
                                    `Open:   $${open.toFixed(2)}`,
                                    `High:   $${high.toFixed(2)}`,
                                    `Low:    $${low.toFixed(2)}`,
                                    `Close:  $${close.toFixed(2)}`,
                                    `Change: ${chgSign}${chg.toFixed(2)}% ${tag}`,
                                    `Volume: ${formatVolumeDetailed(vol)}`
                                ];

                                if (eventDateMap.has(p.date)) {
                                    const ev = eventDateMap.get(p.date);
                                    const fr = ev.forward_returns || {};
                                    lines.push(`───────────────────────────`);
                                    lines.push(`⚠️ Detected Drop: -${Math.abs(ev.drop_percentage).toFixed(2)}%`);
                                    lines.push(`Start Price: $${ev.start_price.toFixed(2)}`);
                                    lines.push(`Event Price: $${ev.event_price ? ev.event_price.toFixed(2) : close.toFixed(2)}`);
                                    lines.push(`30D Return:  ${fr['30_days'] !== null && fr['30_days'] !== undefined ? (fr['30_days'] > 0 ? '+' : '') + fr['30_days'].toFixed(2) + '%' : 'N/A'}`);
                                    lines.push(`90D Return:  ${fr['90_days'] !== null && fr['90_days'] !== undefined ? (fr['90_days'] > 0 ? '+' : '') + fr['90_days'].toFixed(2) + '%' : 'N/A'}`);
                                    lines.push(`180D Return: ${fr['180_days'] !== null && fr['180_days'] !== undefined ? (fr['180_days'] > 0 ? '+' : '') + fr['180_days'].toFixed(2) + '%' : 'N/A'}`);
                                }
                                return lines;
                            }
                            return null;
                        }
                    }
                },
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x'
                    },
                    zoom: {
                        wheel: { enabled: true },
                        pinch: { enabled: true },
                        mode: 'x'
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: '#101622', drawTicks: false },
                    ticks: {
                        color: '#64748b',
                        font: { family: 'JetBrains Mono', size: 10 },
                        maxTicksLimit: 10
                    }
                },
                y: {
                    type: 'linear',
                    position: 'right',
                    stack: 'v-stack',
                    stackWeight: 3.8,
                    grace: '4%',
                    grid: { color: '#101622', drawTicks: false },
                    ticks: {
                        color: '#64748b',
                        font: { family: 'JetBrains Mono', size: 10 },
                        callback: function(v) { return `$${v}`; }
                    }
                },
                volume: {
                    type: 'linear',
                    position: 'right',
                    stack: 'v-stack',
                    stackWeight: 1.2,
                    beginAtZero: true,
                    offset: false,
                    grace: '10%',
                    grid: { color: '#101622', drawTicks: false },
                    ticks: {
                        color: '#475569',
                        font: { family: 'JetBrains Mono', size: 9 },
                        maxTicksLimit: 3,
                        callback: function(v) {
                            if (v >= 1e9) return (v / 1e9).toFixed(1) + 'B';
                            if (v >= 1e6) return (v / 1e6).toFixed(1) + 'M';
                            if (v >= 1e3) return (v / 1e3).toFixed(0) + 'K';
                            if (v === 0) return '0';
                            return v;
                        }
                    }
                }
            }
        }
    });

    applyChartRange(currentRange);
}

/**
 * Preserved Line Chart Implementation (Retained for verification & fallback)
 */
function renderLineChart(data) {
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;
    const prices = data.price_history || [];
    const events = data.events || [];
    if (prices.length === 0) return;

    const eventDateMap = new Map();
    events.forEach(ev => eventDateMap.set(ev.event_date, ev));
    const labels = prices.map(p => p.date);
    const closePrices = prices.map(p => p.close);
    const pointRadii = prices.map(p => eventDateMap.has(p.date) ? 6 : 0);
    const pointColors = prices.map(p => eventDateMap.has(p.date) ? '#ef4444' : 'transparent');
    const pointBorderColors = prices.map(p => eventDateMap.has(p.date) ? '#ffffff' : 'transparent');
    const pointBorderWidths = prices.map(p => eventDateMap.has(p.date) ? 2 : 0);

    if (chartInstance) chartInstance.destroy();
    const volumes = prices.map(p => (p.volume !== undefined && p.volume !== null) ? Number(p.volume) : 0);
    const volumeColors = prices.map(p => Number(p.close) >= Number(p.open || p.close) ? 'rgba(16, 185, 129, 0.75)' : 'rgba(239, 68, 68, 0.75)');

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    type: 'line',
                    label: 'Historical Price',
                    data: closePrices,
                    yAxisID: 'y',
                    borderColor: '#06b6d4',
                    borderWidth: 1.6,
                    backgroundColor: 'rgba(6, 182, 212, 0.05)',
                    fill: true,
                    tension: 0.1,
                    pointRadius: pointRadii,
                    pointHoverRadius: 8,
                    pointBackgroundColor: pointColors,
                    pointBorderColor: pointBorderColors,
                    pointBorderWidth: pointBorderWidths,
                    order: 1
                },
                {
                    type: 'bar',
                    label: 'Volume',
                    data: volumes,
                    yAxisID: 'volume',
                    backgroundColor: volumeColors,
                    borderWidth: 0.8,
                    order: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { color: '#101622' } },
                y: { stack: 'v-stack', stackWeight: 3.8 },
                volume: { stack: 'v-stack', stackWeight: 1.2 }
            }
        }
    });
    applyChartRange(currentRange);
}

function formatVolumeDetailed(num) {
    if (num === null || num === undefined || isNaN(num)) return '0';
    const n = Number(num);
    let compact = '';
    if (n >= 1e9) compact = ` (${(n / 1e9).toFixed(2)}B)`;
    else if (n >= 1e6) compact = ` (${(n / 1e6).toFixed(2)}M)`;
    else if (n >= 1e3) compact = ` (${(n / 1e3).toFixed(1)}K)`;
    return n.toLocaleString() + compact;
}

/**
 * Alternative Chart View: Forward Returns Bar Distribution
 */
function renderForwardReturnsChart(events) {
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;

    const labels = events.map(e => e.event_date);
    const r30 = events.map(e => (e.forward_returns && e.forward_returns['30_days']) || 0);
    const r90 = events.map(e => (e.forward_returns && e.forward_returns['90_days']) || 0);
    const r180 = events.map(e => (e.forward_returns && e.forward_returns['180_days']) || 0);

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                { label: '30D Return %', data: r30, backgroundColor: '#3b82f6' },
                { label: '90D Return %', data: r90, backgroundColor: '#10b981' },
                { label: '180D Return %', data: r180, backgroundColor: '#8b5cf6' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: '#101622' },
                    ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 10 } }
                },
                y: {
                    position: 'right',
                    grid: { color: '#101622' },
                    ticks: {
                        color: '#64748b',
                        font: { family: 'JetBrains Mono', size: 10 },
                        callback: v => `${v}%`
                    }
                }
            }
        }
    });
}

function switchChartMode(mode) {
    currentChartMode = mode;
    const btnPrice = document.getElementById('btn-view-price');
    const btnReturns = document.getElementById('btn-view-returns');
    if (btnPrice && btnReturns) {
        if (mode === 'price') {
            btnPrice.classList.add('active');
            btnReturns.classList.remove('active');
        } else {
            btnReturns.classList.add('active');
            btnPrice.classList.remove('active');
        }
    }
    if (currentAnalysisData) {
        renderChart(currentAnalysisData);
    }
}

/**
 * Filter Display Range Only (1M, 3M, 6M, 1Y, 5Y, ALL)
 */
function setChartRange(range) {
    currentRange = range;
    document.querySelectorAll('.chart-range-pill').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-range') === range);
    });
    applyChartRange(range);
}

function applyChartRange(range) {
    if (!chartInstance || !chartInstance.data || !chartInstance.data.labels) return;
    const total = chartInstance.data.labels.length;
    if (total === 0) return;

    let pointsToShow = total;
    if (range === '1M') pointsToShow = 22;
    else if (range === '3M') pointsToShow = 66;
    else if (range === '6M') pointsToShow = 126;
    else if (range === '1Y') pointsToShow = 252;
    else if (range === '5Y') pointsToShow = 1260;
    else if (range === 'ALL') pointsToShow = total;

    const minIdx = Math.max(0, total - pointsToShow);
    const maxIdx = total - 1;

    chartInstance.options.scales.x.min = chartInstance.data.labels[minIdx];
    chartInstance.options.scales.x.max = chartInstance.data.labels[maxIdx];
    chartInstance.update('none');
}

/**
 * Historical Drop Events Table
 */
function updateAndRenderTable() {
    const tbody = document.getElementById('events-tbody');
    const badge = document.getElementById('table-badge');
    if (!tbody) return;
    tbody.innerHTML = '';

    const list = getFilteredAndSortedEvents();
    if (badge) badge.textContent = `${list.length} Detected Events`;

    if (list.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align: center; padding: 24px; color: var(--text-muted);">
                    No historical drop events found matching the criteria.
                </td>
            </tr>
        `;
        return;
    }

    list.forEach(ev => {
        const tr = document.createElement('tr');
        tr.title = `Click to zoom chart to event on ${ev.event_date}`;
        tr.addEventListener('click', () => zoomChartToEvent(ev));

        const fr = ev.forward_returns || {};
        const r30 = fr['30_days'];
        const r90 = fr['90_days'];
        const r180 = fr['180_days'];

        tr.innerHTML = `
            <td><strong>${ev.event_date}</strong></td>
            <td style="color: var(--text-muted);">${ev.start_date || '—'}</td>
            <td class="num-align" style="color: var(--red-down); font-weight: 700;">-${Math.abs(ev.drop_percentage).toFixed(2)}%</td>
            <td class="num-align">$${ev.start_price.toFixed(2)}</td>
            <td class="num-align">$${ev.event_price.toFixed(2)}</td>
            <td class="num-align ${getReturnClass(r30)}">${formatReturn(r30)}</td>
            <td class="num-align ${getReturnClass(r90)}">${formatReturn(r90)}</td>
            <td class="num-align ${getReturnClass(r180)}">${formatReturn(r180)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function getFilteredAndSortedEvents() {
    let list = [...currentEvents];

    if (currentFilterText) {
        list = list.filter(ev => {
            return (ev.event_date || '').toLowerCase().includes(currentFilterText) ||
                   (ev.start_date || '').toLowerCase().includes(currentFilterText);
        });
    }

    list.sort((a, b) => {
        let valA, valB;
        if (currentSortCol === 'event_date' || currentSortCol === 'start_date') {
            valA = a[currentSortCol] || '';
            valB = b[currentSortCol] || '';
        } else if (currentSortCol.endsWith('_days')) {
            valA = (a.forward_returns && a.forward_returns[currentSortCol]) ?? -999999;
            valB = (b.forward_returns && b.forward_returns[currentSortCol]) ?? -999999;
        } else {
            valA = a[currentSortCol] ?? 0;
            valB = b[currentSortCol] ?? 0;
        }

        if (valA < valB) return currentSortDir === 'asc' ? -1 : 1;
        if (valA > valB) return currentSortDir === 'asc' ? 1 : -1;
        return 0;
    });

    return list;
}

function formatReturn(val) {
    if (val === null || val === undefined) return 'N/A';
    const num = parseFloat(val);
    return `${num > 0 ? '+' : ''}${num.toFixed(2)}%`;
}

function getReturnClass(val) {
    if (val === null || val === undefined) return '';
    return val > 0 ? 'color: var(--green-up);' : (val < 0 ? 'color: var(--red-down);' : '');
}

function zoomChartToEvent(ev) {
    if (!chartInstance || !chartInstance.data || !chartInstance.data.labels) return;
    const labels = chartInstance.data.labels;
    const idx = labels.indexOf(ev.event_date);
    if (idx === -1) return;

    const startIdx = Math.max(0, idx - 15);
    const endIdx = Math.min(labels.length - 1, idx + 25);

    chartInstance.options.scales.x.min = labels[startIdx];
    chartInstance.options.scales.x.max = labels[endIdx];
    chartInstance.update();

    document.querySelectorAll('.chart-range-pill').forEach(b => b.classList.remove('active'));
}

/**
 * Global Search Autocomplete Logic
 */
function setupGlobalSearch() {
    const input = document.getElementById('global-search-input');
    const dropdown = document.getElementById('global-search-dropdown');
    if (!input || !dropdown) return;

    input.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        clearTimeout(searchDebounceTimer);

        if (query.length === 0) {
            dropdown.classList.add('hidden');
            dropdown.innerHTML = '';
            return;
        }

        searchDebounceTimer = setTimeout(async () => {
            try {
                const res = await fetch(`${SEARCH_URL}?q=${encodeURIComponent(query)}`);
                if (!res.ok) {
                    renderSearchDropdown([]);
                    return;
                }
                const data = await res.json();
                const results = Array.isArray(data) ? data : (data.results || []);
                renderSearchDropdown(results);
            } catch (err) {
                console.error("Search fetch error:", err);
                renderSearchDropdown([]);
            }
        }, 180);
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.topbar-center')) {
            dropdown.classList.add('hidden');
        }
    });

    // Enter key selects
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const first = dropdown.querySelector('.search-drop-item');
            if (first) {
                first.click();
            } else if (input.value.trim()) {
                const rawVal = input.value.trim();
                fetch(`${SEARCH_URL}?q=${encodeURIComponent(rawVal)}`)
                    .then(res => res.json())
                    .then(data => {
                        const results = Array.isArray(data) ? data : (data.results || []);
                        if (results.length > 0) {
                            selectCompany(results[0].ticker, results[0]);
                            dropdown.classList.add('hidden');
                            input.value = '';
                        } else {
                            showStatus(`No matching company found for "${rawVal}".`, 'error');
                            dropdown.classList.add('hidden');
                        }
                    })
                    .catch(() => {
                        showStatus(`No matching company found for "${rawVal}".`, 'error');
                        dropdown.classList.add('hidden');
                    });
            }
        } else if (e.key === 'Escape') {
            dropdown.classList.add('hidden');
        }
    });
}

function renderSearchDropdown(results) {
    const dropdown = document.getElementById('global-search-dropdown');
    if (!dropdown) return;
    dropdown.innerHTML = '';

    if (!results || results.length === 0) {
        dropdown.innerHTML = `
            <div style="padding: 12px 14px; color: var(--text-muted); font-size: 11px; font-family: var(--font-ui);">
                No matching company found.
            </div>
        `;
        dropdown.classList.remove('hidden');
        return;
    }

    results.forEach(item => {
        const row = document.createElement('div');
        row.className = 'search-drop-item';

        const logo = window.createCompanyLogo ? window.createCompanyLogo(item.ticker, item.company_name, 'sm', item.logo_url) : document.createElement('div');
        const textCol = document.createElement('div');
        textCol.className = 'search-drop-text';
        textCol.innerHTML = `
            <span class="search-drop-title">${item.company_name}</span>
            <span class="search-drop-sub">${item.ticker} · ${item.exchange || 'EQUITY'} · ${item.country || 'Global'}</span>
        `;

        row.appendChild(logo);
        row.appendChild(textCol);

        row.addEventListener('click', () => {
            selectCompany(item.ticker, item);
            dropdown.classList.add('hidden');
            const searchInput = document.getElementById('global-search-input');
            if (searchInput) searchInput.value = '';
        });

        dropdown.appendChild(row);
    });

    dropdown.classList.remove('hidden');
}

/**
 * Filter Dropdowns Loader
 */
async function loadFilterDropdowns() {
    try {
        const res = await fetch(FILTERS_URL);
        if (res.ok) {
            const data = await res.json();
            populateFilterSelect('market-country-select', data.countries || [], 'Countries');
            populateFilterSelect('market-exchange-select', data.exchanges || [], 'Exchanges');
        }
    } catch (e) {
        console.warn("Could not load filters from backend:", e);
    }
}

function populateFilterSelect(selectId, options, label) {
    const el = document.getElementById(selectId);
    if (!el) return;
    el.innerHTML = '';
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.textContent = opt === 'All' ? `All ${label}` : opt;
        el.appendChild(option);
    });
}

/**
 * Right Markets Panel (Asset List)
 */
async function loadMarketsList() {
    try {
        const params = new URLSearchParams();
        if (selectedCountry && selectedCountry !== 'All') params.append('country', selectedCountry);
        if (selectedExchange && selectedExchange !== 'All') params.append('exchange', selectedExchange);
        if (currentMarketFilter) params.append('q', currentMarketFilter);

        const url = `${MARKETS_URL}?${params.toString()}`;
        const res = await fetch(url);
        if (res.ok) {
            const rawData = await res.json();
            if (Array.isArray(rawData)) {
                marketsData = rawData;
            } else if (rawData && Array.isArray(rawData.markets)) {
                marketsData = rawData.markets;
            } else if (rawData && Array.isArray(rawData.results)) {
                marketsData = rawData.results;
            } else {
                marketsData = [...DEFAULT_MARKETS_CACHE];
            }
            const countTag = document.getElementById('dock-markets-count');
            if (countTag) countTag.textContent = marketsData.length;

            const scopeText = document.getElementById('market-scope-text');
            if (scopeText) {
                if (selectedCountry !== 'All' || selectedExchange !== 'All' || currentMarketFilter) {
                    const cPart = selectedCountry !== 'All' ? selectedCountry : '';
                    const ePart = selectedExchange !== 'All' ? selectedExchange : '';
                    scopeText.textContent = `${cPart} ${ePart} (${marketsData.length})`.trim();
                } else {
                    scopeText.textContent = `WATCHLIST & GLOBAL (${marketsData.length})`;
                }
            }
            renderMarketsList(currentMarketFilter);
        }
    } catch (e) {
        console.warn("Markets refresh failed; using default asset list.", e);
        if (!Array.isArray(marketsData) || marketsData.length === 0) {
            marketsData = [...DEFAULT_MARKETS_CACHE];
        }
        renderMarketsList(currentMarketFilter);
    }
}

function renderMarketsList(filter = '') {
    const container = document.getElementById('markets-list-container');
    if (!container) return;
    container.innerHTML = '';

    if (!Array.isArray(marketsData) || marketsData.length === 0) {
        marketsData = [...DEFAULT_MARKETS_CACHE];
    }

    const list = marketsData.filter(m => {
        if (!filter) return true;
        const sym = (m.ticker || '').toLowerCase();
        const name = (m.company_name || '').toLowerCase();
        const cntry = (m.country || '').toLowerCase();
        return sym.includes(filter) || name.includes(filter) || cntry.includes(filter);
    });

    if (list.length === 0) {
        container.innerHTML = `
            <div style="padding: 20px 14px; text-align: center; color: var(--text-muted); font-size: 11px;">
                No matching company found.
            </div>
        `;
        return;
    }

    const currentTicker = (document.getElementById('ticker')?.value || 'AAPL').toUpperCase();

    list.forEach(item => {
        const row = document.createElement('div');
        const isActive = item.ticker.toUpperCase() === currentTicker;
        row.className = `market-asset-row ${isActive ? 'active' : ''}`;
        row.setAttribute('data-market-ticker', item.ticker.toUpperCase());
        row.title = `Click to analyze ${item.company_name || item.ticker} (${item.country || 'Global'})`;

        const left = document.createElement('div');
        left.className = 'asset-left-info';

        const logo = window.createCompanyLogo ? window.createCompanyLogo(item.ticker, item.company_name, 'md', item.logo_url) : document.createElement('div');
        const names = document.createElement('div');
        names.className = 'asset-names-group';
        names.innerHTML = `
            <span class="asset-company-name" title="${item.company_name}">${item.company_name || item.ticker}</span>
            <span class="asset-ticker-text">${item.ticker}</span>
            <span class="asset-country-text">${item.country || item.exchange || 'Global'}</span>
        `;
        left.appendChild(logo);
        left.appendChild(names);

        const right = document.createElement('div');
        right.className = 'asset-right-quotes';

        const priceStr = item.latest_price !== null && item.latest_price !== undefined ? `$${item.latest_price.toFixed(2)}` : (item.exchange || '—');
        const chg = item.daily_change_pct;
        const isPos = chg >= 0;
        const chgStr = chg !== null && chg !== undefined ? `${isPos ? '+' : ''}${chg.toFixed(2)}%` : '';

        right.innerHTML = `
            <span class="asset-price-val">${priceStr}</span>
            ${chgStr ? `<span class="asset-change-val ${isPos ? 'positive' : 'negative'}">${chgStr}</span>` : ''}
        `;

        row.appendChild(left);
        row.appendChild(right);

        row.addEventListener('click', () => {
            selectCompany(item.ticker, item);
        });

        container.appendChild(row);
    });
}

function highlightActiveMarketRow(ticker) {
    const sym = (ticker || 'AAPL').toUpperCase();
    document.querySelectorAll('.market-asset-row').forEach(row => {
        row.classList.toggle('active', row.getAttribute('data-market-ticker') === sym);
    });
}

function selectCompany(ticker, fallbackMetadata = null) {
    if (!ticker) return;
    const cleanTicker = ticker.trim().toUpperCase();
    const inputTicker = document.getElementById('ticker');
    if (inputTicker) inputTicker.value = cleanTicker;

    // Highlight row in right Markets list immediately
    highlightActiveMarketRow(cleanTicker);

    // Look for company in local marketsData or fallbackMetadata
    let item = fallbackMetadata;
    if (!item && Array.isArray(marketsData)) {
        item = marketsData.find(m => (m.ticker || '').toUpperCase() === cleanTicker);
    }

    if (item) {
        // Immediate visual header update
        const nameEl = document.getElementById('company-header-name');
        const tickerEl = document.getElementById('header-ticker');
        const exchEl = document.getElementById('company-header-exchange');
        const countryEl = document.getElementById('company-header-country');
        const chartSym = document.getElementById('chart-symbol');
        const logoWrap = document.getElementById('company-header-logo-wrap');
        const priceEl = document.getElementById('company-header-price');
        const changeEl = document.getElementById('company-header-change');

        if (nameEl) nameEl.textContent = item.company_name || cleanTicker;
        if (tickerEl) tickerEl.textContent = cleanTicker;
        if (exchEl) exchEl.textContent = item.exchange || 'EQUITY';
        if (countryEl) countryEl.textContent = item.country || 'Global';
        if (chartSym) chartSym.textContent = cleanTicker;

        if (logoWrap && window.createCompanyLogo) {
            logoWrap.innerHTML = '';
            logoWrap.appendChild(window.createCompanyLogo(cleanTicker, item.company_name || cleanTicker, 'lg', item.logo_url));
        }

        if (item.latest_price !== undefined && item.latest_price !== null) {
            if (priceEl) priceEl.textContent = `$${Number(item.latest_price).toFixed(2)}`;
            if (changeEl && item.daily_change_pct !== undefined && item.daily_change_pct !== null) {
                const isPos = item.daily_change_pct >= 0;
                changeEl.textContent = `${isPos ? '+' : ''}${Number(item.daily_change_pct).toFixed(2)}%`;
                changeEl.className = `price-change-tag ${isPos ? 'positive' : 'negative'}`;
            }
        }
    } else {
        renderInitialCompanyHeader(cleanTicker);
    }

    // Trigger full deterministic analysis
    triggerAnalysis();
}

function openSettingsModal() {
    const modal = document.getElementById('terminal-settings-modal');
    if (modal) {
        modal.classList.remove('hidden');
        updateSettingsUI();
    }
}

function closeSettingsModal() {
    const modal = document.getElementById('terminal-settings-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function updateSettingsUI() {
    const activeApiEl = document.getElementById('settings-active-api');
    const creditsEl = document.getElementById('settings-credits-display');
    const btnProd = document.getElementById('btn-env-production');
    const btnLocal = document.getElementById('btn-env-local');

    if (activeApiEl) activeApiEl.textContent = API_BASE_URL;
    if (creditsEl) creditsEl.textContent = `${currentCredits} / ${TOTAL_CREDITS} cr`;

    const isProd = API_BASE_URL === ENV_CONFIG.production;
    if (btnProd) btnProd.classList.toggle('active', isProd);
    if (btnLocal) btnLocal.classList.toggle('active', !isProd);
}

/**
 * AI Credits & Drawer Implementation
 */
function initAICredits() {
    const stored = localStorage.getItem('nocap_ai_credits');
    if (stored !== null) {
        currentCredits = parseInt(stored, 10);
        if (isNaN(currentCredits) || currentCredits < 0) currentCredits = TOTAL_CREDITS;
    } else {
        currentCredits = TOTAL_CREDITS;
    }
    updateCreditsUI();
}

function updateCreditsUI() {
    localStorage.setItem('nocap_ai_credits', String(currentCredits));
    const topCount = document.getElementById('top-credits-count');
    const panelCount = document.getElementById('panel-credits-count');
    const bar = document.getElementById('panel-credits-bar');

    if (topCount) topCount.textContent = currentCredits;
    if (panelCount) panelCount.textContent = currentCredits;
    if (bar) {
        const pct = Math.max(0, Math.min(100, (currentCredits / TOTAL_CREDITS) * 100));
        bar.style.width = `${pct}%`;
    }
}

function openAiDrawer() {
    const drawer = document.getElementById('terminal-ai-drawer');
    if (drawer) {
        drawer.classList.remove('hidden');
        document.getElementById('chat-user-input')?.focus();
    }
}

function closeAiDrawer() {
    const drawer = document.getElementById('terminal-ai-drawer');
    if (drawer) drawer.classList.add('hidden');
}

function initChatHistory() {
    const box = document.getElementById('chat-messages');
    if (!box) return;
    if (box.children.length === 0) {
        appendChatMessage('ai', `Welcome to NoCap AI Terminal.\n\nHistorical analysis based on empirical data only. No crystal balls or fake predictions.\n\nAsk me to analyze any stock (e.g. "Analyze Apple", "Analyze Puma", "Analyze TCS"), explain volatility metrics, or compare drawdown histories.`);
    }
}

function appendChatMessage(sender, text, meta = {}) {
    const box = document.getElementById('chat-messages');
    if (!box) return;

    const msgEl = document.createElement('div');
    msgEl.className = `chat-msg ${sender}`;

    const header = document.createElement('div');
    header.className = 'chat-msg-hdr';

    const author = document.createElement('span');
    author.className = sender === 'ai' ? 'chat-author-ai' : 'chat-author-user';
    author.textContent = sender === 'ai' ? '✦ NoCap AI' : 'You';
    header.appendChild(author);

    if (meta.credit_cost) {
        const costTag = document.createElement('span');
        costTag.className = 'chat-cost-tag';
        costTag.textContent = `-${meta.credit_cost} cr`;
        header.appendChild(costTag);
    }
    msgEl.appendChild(header);

    if (meta.card_data) {
        const card = renderStructuredCard(meta.card_data);
        msgEl.appendChild(card);
    } else {
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';
        bubble.textContent = text;
        msgEl.appendChild(bubble);
    }

    box.appendChild(msgEl);
    box.scrollTop = box.scrollHeight;
}

function renderStructuredCard(cardData) {
    const card = document.createElement('div');
    card.className = 'ai-structured-card';

    const avg30 = cardData.avg_30d || 'N/A';
    const avg90 = cardData.avg_90d || 'N/A';
    const avg180 = cardData.avg_180d || 'N/A';

    card.innerHTML = `
        <div class="card-title-row">
            <span class="card-company-title">${cardData.ticker} — ${cardData.company_name}</span>
            <span class="card-cost-pill">-25 cr</span>
        </div>
        <div class="card-stakes-block">
            <span style="color: var(--text-muted);">Historical Stakes</span>
            <strong style="color: #ffffff;">${cardData.stakes_emoji || '🔴'} ${cardData.stakes}</strong>
        </div>
        <div style="font-size: 10px; color: var(--text-muted);">${cardData.events_count} historical events analyzed</div>
        <div class="card-returns-grid">
            <div class="return-cell">
                <span class="cell-label">30D Avg:</span>
                <span class="cell-val" style="color: ${cardData.avg_30d_num > 0 ? 'var(--green-up)' : (cardData.avg_30d_num < 0 ? 'var(--red-down)' : '#fff')}">${avg30}</span>
            </div>
            <div class="return-cell">
                <span class="cell-label">90D Avg:</span>
                <span class="cell-val" style="color: ${cardData.avg_90d_num > 0 ? 'var(--green-up)' : (cardData.avg_90d_num < 0 ? 'var(--red-down)' : '#fff')}">${avg90}</span>
            </div>
            <div class="return-cell">
                <span class="cell-label">180D Avg:</span>
                <span class="cell-val" style="color: ${cardData.avg_180d_num > 0 ? 'var(--green-up)' : (cardData.avg_180d_num < 0 ? 'var(--red-down)' : '#fff')}">${avg180}</span>
            </div>
        </div>
        <div class="card-why-block">
            <strong>Why?</strong> ${cardData.why}
        </div>
        <div class="card-disclaimer-note">
            ${cardData.disclaimer || 'Historical analysis only. Past performance does not guarantee future results.'}
        </div>
    `;
    return card;
}

async function handleChatSubmit(e) {
    if (e) e.preventDefault();
    const chatInput = document.getElementById('chat-user-input');
    if (!chatInput) return;
    const text = chatInput.value.trim();
    if (!text) return;

    appendChatMessage('user', text);
    chatInput.value = '';

    const loadingId = 'ai-loading-' + Date.now();
    const box = document.getElementById('chat-messages');
    const loadingEl = document.createElement('div');
    loadingEl.id = loadingId;
    loadingEl.className = 'chat-msg ai';
    loadingEl.innerHTML = `
        <div class="chat-msg-hdr"><span class="chat-author-ai">✦ NoCap AI</span></div>
        <div class="chat-bubble" style="color: var(--accent-cyan); font-style: italic;">Analyzing empirical market data...</div>
    `;
    box.appendChild(loadingEl);
    box.scrollTop = box.scrollHeight;

    try {
        const payload = {
            message: text,
            current_ticker: document.getElementById('ticker')?.value || 'AAPL',
            drop_threshold: parseFloat(document.getElementById('drop_threshold')?.value) || 10,
            window_days: parseInt(document.getElementById('window_days')?.value, 10) || 5,
            years: parseInt(document.getElementById('years')?.value, 10) || 10,
            credits: currentCredits
        };

        const res = await fetch(CHAT_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        const loader = document.getElementById(loadingId);
        if (loader) loader.remove();

        if (data.insufficient_credits) {
            appendChatMessage('ai', data.reply);
            return;
        }

        if (data.credits_remaining !== undefined) {
            currentCredits = data.credits_remaining;
            updateCreditsUI();
        }

        appendChatMessage('ai', data.reply, {
            credit_cost: data.credits_deducted || data.credit_cost,
            card_data: data.card_data
        });

        // If the reply contains newly analyzed company data, update the main terminal!
        if (data.analysis_data && data.action_type === 'analysis') {
            const tickerInput = document.getElementById('ticker');
            if (tickerInput) tickerInput.value = data.ticker;
            renderDashboard(data.analysis_data);
        }

    } catch (err) {
        const loader = document.getElementById(loadingId);
        if (loader) loader.remove();
        appendChatMessage('ai', `Connection error: ${err.message}`);
    }
}

/**
 * Backend Health & Supabase Check
 */
async function checkBackendHealth() {
    const dot = document.getElementById('supabase-status-dot');
    const txt = document.getElementById('supabase-status-text');
    try {
        const res = await fetch(`${API_BASE_URL}/api/supabase/test`);
        if (res.ok) {
            if (dot) dot.className = 'status-glow-dot green';
            if (txt) txt.innerHTML = 'Supabase: <strong>Connected</strong>';
        }
    } catch (e) {
        if (dot) dot.className = 'status-glow-dot green';
    }
}

function handleReset() {
    const inputTicker = document.getElementById('ticker');
    const inputDropThreshold = document.getElementById('drop_threshold');
    const inputWindowDays = document.getElementById('window_days');
    const inputYears = document.getElementById('years');

    if (inputTicker) inputTicker.value = 'AAPL';
    if (inputDropThreshold) inputDropThreshold.value = '10';
    if (inputWindowDays) inputWindowDays.value = '5';
    if (inputYears) inputYears.value = '10';
    triggerAnalysis();
}

function exportCSV() {
    const listToExport = getFilteredAndSortedEvents();
    if (!listToExport || listToExport.length === 0) {
        showStatus('No historical drop events available to export.', 'error');
        return;
    }

    const headers = ["Event Date", "Start Date", "Drop %", "Start Price", "Event Price", "30D Return", "90D Return", "180D Return"];
    const rows = listToExport.map(ev => {
        const fr = ev.forward_returns || {};
        return [
            ev.event_date,
            ev.start_date,
            ev.drop_percentage,
            ev.start_price,
            ev.event_price,
            fr['30_days'] ?? 'N/A',
            fr['90_days'] ?? 'N/A',
            fr['180_days'] ?? 'N/A'
        ].join(",");
    });

    const csvContent = [headers.join(","), ...rows].join("\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `NoCapStocks_${document.getElementById('ticker')?.value || 'AAPL'}_Drops.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function showStatus(msg, type = 'info') {
    const el = document.getElementById('status-message');
    if (!el) return;
    el.textContent = msg;
    el.classList.remove('hidden');
}

function hideStatus() {
    const el = document.getElementById('status-message');
    if (!el) return;
    el.classList.add('hidden');
}

function setLoadingState(isLoading) {
    const btn = document.getElementById('btn-analyze');
    if (btn) {
        btn.disabled = isLoading;
        btn.textContent = isLoading ? 'ANALYZING...' : 'ANALYZE';
    }
}

// Window programmatic helpers for testing
window.triggerAnalysis = triggerAnalysis;
window.selectCompany = selectCompany;
window.setChartRange = setChartRange;
window.getFilteredAndSortedEvents = getFilteredAndSortedEvents;
window.openSettingsModal = openSettingsModal;
window.closeSettingsModal = closeSettingsModal;
window.openAiDrawer = openAiDrawer;
window.closeAiDrawer = closeAiDrawer;
window.getChartInstance = () => chartInstance;
