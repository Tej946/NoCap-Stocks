/**
 * CompanyLogo Component / Helper for NoCap Stocks
 * Provides high-definition vector brand logos for top global companies,
 * Supabase/catalog logo_url support, automatic CDN lookup for global tickers,
 * and an institutional initials fallback [TS].
 * Guarantees zero broken images.
 */

// Inject essential logo styles automatically to prevent missing-CSS issues
(function injectLogoStyles() {
    if (document.getElementById('company-logo-styles')) return;
    const style = document.createElement('style');
    style.id = 'company-logo-styles';
    style.textContent = `
        .company-logo-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            background: #101622;
            border: 1px solid #1f2a3d;
            overflow: hidden;
            flex-shrink: 0;
            color: #ffffff;
            position: relative;
            vertical-align: middle;
        }
        .company-logo-badge.logo-sm { width: 22px; height: 22px; font-size: 8px; font-weight: 700; }
        .company-logo-badge.logo-md { width: 32px; height: 32px; font-size: 10px; font-weight: 700; }
        .company-logo-badge.logo-lg { width: 44px; height: 44px; font-size: 13px; font-weight: 700; }
        .company-logo-badge.logo-xl { width: 56px; height: 56px; font-size: 15px; font-weight: 700; }
        .company-logo-badge svg {
            width: 70%;
            height: 70%;
            display: block;
            margin: auto;
        }
        .company-logo-badge img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }
        .company-logo-initials {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            text-align: center;
            letter-spacing: -0.02em;
            text-transform: uppercase;
            font-family: 'JetBrains Mono', 'Inter', monospace;
            font-weight: 700;
        }
    `;
    document.head.appendChild(style);
})();

const BRAND_SVGS = {
    "AAPL": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#ffffff"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.63-.77 1.06-1.84.94-2.91-.91.04-2.02.61-2.67 1.37-.58.67-1.09 1.76-.95 2.81 1.02.08 2.05-.5 2.68-1.27z"/></svg>`,
    "MSFT": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect x="2" y="2" width="9.5" height="9.5" fill="#f25022"/><rect x="12.5" y="2" width="9.5" height="9.5" fill="#7fba00"/><rect x="2" y="12.5" width="9.5" height="9.5" fill="#00a4ef"/><rect x="12.5" y="12.5" width="9.5" height="9.5" fill="#ffb900"/></svg>`,
    "NVDA": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#76b900"><path d="M7.74 8.76c-.23.1-.38.31-.38.56v5.36c0 .25.15.46.38.56.23.1.5.06.69-.11l4.08-3.68c.27-.24.27-.66 0-.9l-4.08-3.68a.59.59 0 0 0-.69-.11zM1.5 12C1.5 6.2 6.2 1.5 12 1.5s10.5 4.7 10.5 10.5-4.7 10.5-10.5 10.5S1.5 17.8 1.5 12zm18.3 0c0-4.3-3.5-7.8-7.8-7.8-2.6 0-5 1.3-6.4 3.4l2.1 1.9c1-1.5 2.6-2.5 4.3-2.5 3 0 5.4 2.4 5.4 5.4 0 2.2-1.3 4.1-3.2 4.9v2.8c3.2-1.1 5.6-4.1 5.6-8.1z"/></svg>`,
    "TSLA": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#e82127"><path d="M12 4.5c2.7 0 5.6.8 7.7 2.1l1.3-2.6C18.2 2.4 15.2 1.5 12 1.5S5.8 2.4 3 4l1.3 2.6C6.4 5.3 9.3 4.5 12 4.5zm0 3.7c-2 0-3.9.4-5.5 1.1l-.8-1.5C7.4 7 9.6 6.6 12 6.6s4.6.4 6.3 1.2l-.8 1.5c-1.6-.7-3.5-1.1-5.5-1.1zm6.9 3.6l-5.6 11.2h-2.6L5.1 11.8c-.8.6-1.5 1.3-2.1 2.1l7.8 8.6h2.4l7.8-8.6c-.6-.8-1.3-1.5-2.1-2.1z"/></svg>`,
    "AMZN": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#ff9900"><path d="M13.9 14.7c-1.8 1.4-4.5 2.1-6.8 2.1-3.2 0-6.1-1.2-8.3-3.2-.2-.2-.2-.4 0-.6l1-.9c.2-.2.4-.1.6.1 1.7 1.5 4 2.4 6.5 2.4 1.9 0 4.1-.6 5.6-1.8.3-.2.6.1.4.4l-1.3 1.2c-.2.2-.2.3.1.3 2.4 0 4.8-.8 6.7-2.3.2-.2.5-.1.6.2.3.5.7 1.1 1 1.7.1.3 0 .5-.3.7-2.1 1.6-4.7 2.4-7.3 2.4-2.8 0-5.5-.9-7.7-2.5-.2-.2-.2-.4 0-.6l.9-.9c.2-.2.4-.1.6.1 1.8 1.3 4 2.1 6.3 2.1 2.2 0 4.4-.7 6.1-2.1.2-.2.5 0 .4.3l-.9 1.1c0 .1-.2.2-.3.2z"/><path d="M19.8 17.5c-.3.4-1.7 1.2-2.5 1.2-.3 0-.4-.2-.2-.5.5-.8 1.4-2 1.4-2s.2-.4.4-.3c.3.1.9 1.2.9 1.6z"/></svg>`,
    "GOOGL": `<svg viewBox="0 0 24 24" width="100%" height="100%"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>`,
    "META": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#0081fb"><path d="M16.9 3.5c-2.3 0-4.3 1.2-5.4 3-1.1-1.8-3.1-3-5.4-3-3.6 0-6.1 2.9-6.1 6.5 0 4.8 5.7 8.8 11.5 12.5 5.8-3.7 11.5-7.7 11.5-12.5 0-3.6-2.5-6.5-6.1-6.5zm-5.4 12.2c-3.1-2.4-6.3-5.3-6.3-8.7 0-2.1 1.4-3.7 3.5-3.7 1.8 0 3.4 1.3 3.9 3.1h-1.9c-.3 0-.6.3-.6.6s.3.6.6.6h2.2c.1.4.1.7.1 1.1 0 2.2-.7 4.9-1.5 7zm2.4 0c-.8-2.1-1.5-4.8-1.5-7 0-.4 0-.7.1-1.1h2.2c.3 0 .6-.3.6-.6s-.3-.6-.6-.6h-1.9c.5-1.8 2.1-3.1 3.9-3.1 2.1 0 3.5 1.6 3.5 3.7 0 3.4-3.2 6.3-6.3 8.7z"/></svg>`,
    "PUM.DE": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#00e676"><path d="M21.8 7.4c-.4-.7-1.1-1.2-1.9-1.4-1.2-.2-2.3.3-3.1 1.1-.9.9-1.5 2.1-2.3 3.1-.7.9-1.6 1.7-2.7 2.1-1 .4-2.1.3-3.1-.1l-1.3-.6c-.8-.4-1.8-.4-2.6 0L2.5 13c-.4.2-.6.7-.4 1.1.2.4.7.6 1.1.4l2.3-1.3c.5-.3 1.1-.3 1.6 0l1.3.6c1.3.6 2.8.7 4.1.2 1.4-.5 2.6-1.5 3.5-2.6.7-.9 1.3-1.9 2-2.7.5-.5 1.1-.8 1.8-.7.5.1.9.4 1.2.8.3.5.3 1.1.1 1.6-.4.9-1.1 1.6-1.8 2.2-.4.3-.4.8-.1 1.2.3.4.8.4 1.2.1 1-.8 1.9-1.8 2.3-3 .4-.9.4-2-.1-2.9z"/></svg>`,
    "PUMSY": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#00e676"><path d="M21.8 7.4c-.4-.7-1.1-1.2-1.9-1.4-1.2-.2-2.3.3-3.1 1.1-.9.9-1.5 2.1-2.3 3.1-.7.9-1.6 1.7-2.7 2.1-1 .4-2.1.3-3.1-.1l-1.3-.6c-.8-.4-1.8-.4-2.6 0L2.5 13c-.4.2-.6.7-.4 1.1.2.4.7.6 1.1.4l2.3-1.3c.5-.3 1.1-.3 1.6 0l1.3.6c1.3.6 2.8.7 4.1.2 1.4-.5 2.6-1.5 3.5-2.6.7-.9 1.3-1.9 2-2.7.5-.5 1.1-.8 1.8-.7.5.1.9.4 1.2.8.3.5.3 1.1.1 1.6-.4.9-1.1 1.6-1.8 2.2-.4.3-.4.8-.1 1.2.3.4.8.4 1.2.1 1-.8 1.9-1.8 2.3-3 .4-.9.4-2-.1-2.9z"/></svg>`,
    "TCS.NS": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#0f4c81"/><text x="12" y="16" fill="#ffffff" font-size="10" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">TCS</text></svg>`,
    "INFY.NS": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#007cc3"/><text x="12" y="16" fill="#ffffff" font-size="9" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">INFY</text></svg>`,
    "SAP.DE": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#008fd3"/><text x="12" y="16" fill="#ffffff" font-size="9" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">SAP</text></svg>`,
    "7203.T": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#eb0a1e"><ellipse cx="12" cy="12" rx="9.5" ry="6" fill="none" stroke="#eb0a1e" stroke-width="1.8"/><ellipse cx="12" cy="12" rx="3.5" ry="6" fill="none" stroke="#eb0a1e" stroke-width="1.8"/><ellipse cx="12" cy="9.5" rx="5" ry="2.5" fill="none" stroke="#eb0a1e" stroke-width="1.8"/></svg>`,
    "BHP.AX": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#ff5f00"/><text x="12" y="16" fill="#ffffff" font-size="9" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">BHP</text></svg>`,
    "SHOP.TO": `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="#95bf47"><path d="M19.4 6.8c-.1-.4-.4-.6-.8-.6h-3.1c-.2-1.7-1.4-3.1-3.1-3.2-1.9-.1-3.5 1.3-3.7 3.2H5.6c-.4 0-.7.2-.8.6l-2.6 13c-.1.5.2 1 .7 1.1.1 0 .2 0 .3 0h17.6c.5 0 .9-.4 1-.9l-2.4-13.2zM12 4.5c.9 0 1.6.7 1.7 1.6H10.3c.1-.9.8-1.6 1.7-1.6zm2.4 8.2c-.4 1.5-1.4 2.2-2.7 2.2-1.6 0-2.7-1.1-2.7-2.8 0-1.8 1.2-3 3-3 .6 0 1.1.1 1.5.4l-.6 1.2c-.3-.2-.6-.3-.9-.3-.9 0-1.5.7-1.5 1.6 0 .9.5 1.5 1.4 1.5.6 0 1.1-.3 1.3-.9l1.2.1z"/></svg>`,
    "005930.KS": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#1428a0"/><text x="12" y="16" fill="#ffffff" font-size="8" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">SMSNG</text></svg>`,
    "0700.HK": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#0052d9"/><text x="12" y="16" fill="#ffffff" font-size="8" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">TENC</text></svg>`,
    "2330.TW": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#c41230"/><text x="12" y="16" fill="#ffffff" font-size="8" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">TSMC</text></svg>`,
    "ASML.AS": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#0f2042"/><text x="12" y="16" fill="#ffffff" font-size="8" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">ASML</text></svg>`,
    "RELIANCE.NS": `<svg viewBox="0 0 24 24" width="100%" height="100%"><rect width="24" height="24" rx="4" fill="#003366"/><text x="12" y="16" fill="#ffffff" font-size="8" font-weight="bold" font-family="'Inter',sans-serif" text-anchor="middle">RIL</text></svg>`
};

const FALLBACK_HUES = [
    { bg: '#172554', text: '#60a5fa', border: '#1e3a8a' }, // Blue
    { bg: '#064e3b', text: '#34d399', border: '#065f46' }, // Emerald
    { bg: '#4c1d95', text: '#c084fc', border: '#581c87' }, // Purple
    { bg: '#701a75', text: '#f472b6', border: '#831843' }, // Pink
    { bg: '#78350f', text: '#fbbf24', border: '#92400e' }, // Amber
    { bg: '#1e293b', text: '#94a3b8', border: '#334155' }  // Slate
];

function getTickerColor(sym) {
    let hash = 0;
    for (let i = 0; i < (sym || '').length; i++) {
        hash = (hash << 5) - hash + sym.charCodeAt(i);
        hash |= 0;
    }
    const idx = Math.abs(hash) % FALLBACK_HUES.length;
    return FALLBACK_HUES[idx];
}

/**
 * Derives clean 2-letter uppercase institutional initials fallback (e.g. [TS], [TM], [SE])
 */
function getInitials(ticker, companyName = '') {
    if (companyName) {
        const clean = companyName.replace(/[^a-zA-Z0-9\s]/g, '').trim();
        const words = clean.split(/\s+/).filter(w => !['inc', 'ltd', 'corp', 'corporation', 'plc', 'se', 'sa', 'ag', 'co'].includes(w.toLowerCase()));
        if (words.length >= 2) {
            return (words[0][0] + words[1][0]).toUpperCase();
        } else if (words.length === 1 && words[0].length >= 2) {
            return words[0].slice(0, 2).toUpperCase();
        }
    }
    const base = (ticker || 'TS').split('.')[0].replace(/[^a-zA-Z0-9]/g, '');
    if (base.length >= 2 && !/^\d+$/.test(base)) {
        return base.slice(0, 2).toUpperCase();
    }
    return base.slice(0, 2).toUpperCase() || 'TS';
}

/**
 * Creates or renders a CompanyLogo DOM node
 * Priority:
 * 1. logo_url if provided (from Supabase or catalog)
 * 2. High-definition local SVG brand logo
 * 3. Dynamic trusted CDN lookup with onerror fallback
 * 4. Initials fallback badge (e.g. [TS])
 * Guarantees zero broken images.
 * @param {string} ticker Ticker symbol (e.g. 'AAPL', 'MSFT', 'TCS.NS', '7203.T')
 * @param {string} companyName Optional company full name
 * @param {string} size 'sm' (22px), 'md' (32px), 'lg' (44px), 'xl' (56px)
 * @param {string|null} logoUrl Optional image URL from Supabase
 * @returns {HTMLElement} A safe, guaranteed non-broken logo container element
 */
function createCompanyLogo(ticker, companyName = '', size = 'md', logoUrl = null) {
    const sym = (ticker || 'AAPL').toUpperCase().trim();
    const baseTicker = sym.split('.')[0];
    const container = document.createElement('div');
    container.className = `company-logo-badge logo-${size}`;
    container.setAttribute('data-ticker', sym);

    // 1. High-definition local SVG brand logo
    if (BRAND_SVGS[sym] || BRAND_SVGS[baseTicker]) {
        container.innerHTML = BRAND_SVGS[sym] || BRAND_SVGS[baseTicker];
        return container;
    }

    const palette = getTickerColor(sym);
    const initials = getInitials(sym, companyName);

    container.style.backgroundColor = palette.bg;
    container.style.borderColor = palette.border;

    const fallbackSpan = document.createElement('span');
    fallbackSpan.className = 'company-logo-initials';
    fallbackSpan.style.color = palette.text;
    fallbackSpan.textContent = initials;
    fallbackSpan.style.display = 'none';

    // 2. Image resolution: logoUrl or Parqet CDN
    const img = document.createElement('img');
    const srcUrl = logoUrl || `https://assets.parqet.com/logos/symbol/${baseTicker}?format=png`;
    img.src = srcUrl;
    img.alt = companyName || sym;
    img.className = 'company-logo-img';
    img.loading = 'lazy';

    img.onload = () => {
        img.style.display = 'block';
    };

    img.onerror = () => {
        img.remove();
        fallbackSpan.style.display = 'flex';
    };

    container.appendChild(img);
    container.appendChild(fallbackSpan);
    return container;
}

// Export for vanilla JS window scope
window.createCompanyLogo = createCompanyLogo;
