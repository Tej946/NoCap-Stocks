/**
 * NoCap Stocks — Client Authentication & Session Management Module
 * Connects frontend UI to Supabase Auth backend APIs.
 * Enforces session persistence, JWT token validation, real-time input checks, and credit syncing.
 */

// Centralized Environment & API Base URL Resolution
const AUTH_ENV_CONFIG = {
    production: 'https://nocap-stocks-tq26.onrender.com',
    local: 'http://127.0.0.1:5000'
};

function getAuthApiBaseUrl() {
    if (typeof window === 'undefined' || !window.location) {
        return AUTH_ENV_CONFIG.production;
    }
    const params = new URLSearchParams(window.location.search);
    const apiParam = params.get('api') || params.get('apiUrl') || params.get('backend');
    if (apiParam === 'prod' || apiParam === 'production') return AUTH_ENV_CONFIG.production;
    if (apiParam === 'local' || apiParam === 'dev') return AUTH_ENV_CONFIG.local;
    if (apiParam && apiParam.startsWith('http')) return apiParam.replace(/\/$/, '');

    try {
        const storedUrl = localStorage.getItem('nocap_api_url');
        if (storedUrl && storedUrl.startsWith('http') && !storedUrl.includes('nocap-stocks-api.onrender.com')) {
            return storedUrl.replace(/\/$/, '');
        }
        const storedEnv = localStorage.getItem('nocap_api_env');
        if (storedEnv && AUTH_ENV_CONFIG[storedEnv]) return AUTH_ENV_CONFIG[storedEnv];
    } catch (_) {}

    const hostname = window.location.hostname;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '0.0.0.0';
    if (!isLocalhost && window.location.protocol !== 'file:') {
        return AUTH_ENV_CONFIG.production;
    }
    return AUTH_ENV_CONFIG.local;
}

const AUTH_STORAGE_KEYS = {
    TOKEN: 'nocap_access_token',
    REFRESH_TOKEN: 'nocap_refresh_token',
    USER: 'nocap_user',
    PROFILE: 'nocap_profile',
    CREDITS: 'nocap_ai_credits'
};

// --------------------------------------------------------------------------
// Session Storage Helpers
// --------------------------------------------------------------------------
function getAuthToken() {
    return localStorage.getItem(AUTH_STORAGE_KEYS.TOKEN) || null;
}

function getCurrentUser() {
    try {
        const raw = localStorage.getItem(AUTH_STORAGE_KEYS.USER);
        return raw ? JSON.parse(raw) : null;
    } catch (_) {
        return null;
    }
}

function getUserProfile() {
    try {
        const raw = localStorage.getItem(AUTH_STORAGE_KEYS.PROFILE);
        return raw ? JSON.parse(raw) : null;
    } catch (_) {
        return null;
    }
}

function setAuthSession(accessToken, refreshToken, user, profile) {
    if (accessToken) localStorage.setItem(AUTH_STORAGE_KEYS.TOKEN, accessToken);
    if (refreshToken) localStorage.setItem(AUTH_STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
    if (user) localStorage.setItem(AUTH_STORAGE_KEYS.USER, JSON.stringify(user));
    if (profile) {
        localStorage.setItem(AUTH_STORAGE_KEYS.PROFILE, JSON.stringify(profile));
        if (profile.credits !== undefined) {
            localStorage.setItem(AUTH_STORAGE_KEYS.CREDITS, String(profile.credits));
        }
    }
}

function clearAuthSession() {
    localStorage.removeItem(AUTH_STORAGE_KEYS.TOKEN);
    localStorage.removeItem(AUTH_STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(AUTH_STORAGE_KEYS.USER);
    localStorage.removeItem(AUTH_STORAGE_KEYS.PROFILE);
    // Reset client credits to default starting amount
    localStorage.setItem(AUTH_STORAGE_KEYS.CREDITS, '500');
}

// --------------------------------------------------------------------------
// API Calls
// --------------------------------------------------------------------------
async function authFetch(endpoint, options = {}) {
    const baseUrl = getAuthApiBaseUrl();
    const url = `${baseUrl}${endpoint}`;
    const token = getAuthToken();

    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(options.headers || {})
    };

    if (token && !headers['Authorization']) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 20000); // 20s timeout

    try {
        const res = await fetch(url, {
            ...options,
            headers,
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        let data;
        const text = await res.text();
        try {
            data = JSON.parse(text);
        } catch (_) {
            data = { success: false, message: `Server error (${res.status} ${res.statusText})` };
        }

        return { ok: res.ok, status: res.status, data };
    } catch (err) {
        clearTimeout(timeoutId);
        let msg = err.name === 'AbortError' ? 'Request timed out after 20 seconds.' : (err.message || 'Network connection failed.');
        return { ok: false, status: 0, data: { success: false, message: msg } };
    }
}

async function apiSignUp(email, password, fullName) {
    return authFetch('/api/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ email, password, full_name: fullName })
    });
}

async function apiLogIn(email, password) {
    return authFetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
    });
}

async function apiLogOut() {
    const token = getAuthToken();
    try {
        if (token) {
            await authFetch('/api/auth/logout', { method: 'POST' });
        }
    } catch (_) {}
    clearAuthSession();
}

async function apiResetPassword(email) {
    return authFetch('/api/auth/reset-password', {
        method: 'POST',
        body: JSON.stringify({ email })
    });
}

async function apiGetMe() {
    return authFetch('/api/auth/me', { method: 'GET' });
}

// --------------------------------------------------------------------------
// UI Helpers: Password Strength & Form Feedback
// --------------------------------------------------------------------------
function calculatePasswordStrength(password) {
    if (!password) return { score: 0, text: 'Empty', color: '#64748b', pct: 0 };
    let score = 0;
    if (password.length >= 6) score += 1;
    if (password.length >= 10) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score += 1;

    if (password.length < 6) {
        return { score: 1, text: 'Too short (min 6 characters)', color: '#ef4444', pct: 20 };
    }
    if (score <= 2) {
        return { score: 2, text: 'Weak', color: '#f87171', pct: 40 };
    }
    if (score === 3) {
        return { score: 3, text: 'Moderate', color: '#f59e0b', pct: 65 };
    }
    if (score === 4) {
        return { score: 4, text: 'Strong', color: '#10b981', pct: 85 };
    }
    return { score: 5, text: 'Very Strong', color: '#06b6d4', pct: 100 };
}

function showAlert(alertEl, message, type = 'error') {
    if (!alertEl) return;
    alertEl.className = `auth-alert ${type}`;
    alertEl.innerHTML = `<span>${type === 'error' ? '⚠️' : (type === 'success' ? '✓' : 'ℹ️')}</span> <div>${message}</div>`;
    alertEl.classList.remove('hidden');
}

function hideAlert(alertEl) {
    if (!alertEl) return;
    alertEl.classList.add('hidden');
    alertEl.innerHTML = '';
}

function setButtonLoading(btn, isLoading, loadingText = 'Processing...') {
    if (!btn) return;
    if (isLoading) {
        btn.disabled = true;
        btn.dataset.origText = btn.innerHTML;
        btn.innerHTML = `<span class="auth-spinner"></span> <span>${loadingText}</span>`;
    } else {
        btn.disabled = false;
        if (btn.dataset.origText) btn.innerHTML = btn.dataset.origText;
    }
}

// --------------------------------------------------------------------------
// Topbar User Profile Rendering (For Terminal Dashboard)
// --------------------------------------------------------------------------
async function syncTopbarUser() {
    const slot = document.getElementById('topbar-user-slot');
    if (!slot) return;

    const token = getAuthToken();
    if (!token) {
        slot.innerHTML = `
            <a href="login.html" class="topbar-auth-btn" id="topbar-login-btn">Log In</a>
            <a href="signup.html" class="topbar-auth-btn signup" id="topbar-signup-btn">Sign Up</a>
        `;
        return;
    }

    const cachedUser = getCurrentUser();
    const cachedProfile = getUserProfile();
    const displayName = (cachedProfile && cachedProfile.full_name) || (cachedUser && cachedUser.email) || 'User';
    const initial = (displayName[0] || 'U').toUpperCase();

    slot.innerHTML = `
        <div class="user-profile-badge" id="user-profile-badge" title="${cachedUser?.email || ''}">
            <div class="user-avatar-initial">${initial}</div>
            <span class="user-display-name">${displayName}</span>
            <button type="button" class="user-logout-btn" id="user-topbar-logout" title="Sign out of NoCap Stocks">Sign Out</button>
        </div>
    `;

    document.getElementById('user-topbar-logout')?.addEventListener('click', async () => {
        await apiLogOut();
        window.location.reload();
    });

    // Verify token & sync credits with server in background
    try {
        const { ok, data } = await apiGetMe();
        if (ok && data.success) {
            setAuthSession(token, null, data.user, data.profile);
            const remaining = data.profile?.credits ?? 500;
            const topCreds = document.getElementById('top-credits-count');
            const panelCreds = document.getElementById('panel-credits-count');
            if (topCreds) topCreds.textContent = remaining;
            if (panelCreds) panelCreds.textContent = remaining;
        } else {
            // Token expired or invalid -> clear session
            clearAuthSession();
            syncTopbarUser();
        }
    } catch (_) {}
}

// --------------------------------------------------------------------------
// Initialization on Page Load
// --------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    // 1. Password toggle buttons (Eye icons)
    document.querySelectorAll('.auth-toggle-pwd-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const input = document.getElementById(targetId);
            if (!input) return;
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            btn.innerHTML = isPassword ? '👁️' : '👁️‍🗨️';
            btn.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
        });
    });

    // 2. Forgot Password Modal handling
    const forgotLink = document.getElementById('forgot-password-link');
    const forgotModal = document.getElementById('forgot-password-modal');
    const closeForgotBtn = document.getElementById('close-forgot-modal');
    const forgotForm = document.getElementById('forgot-password-form');
    const forgotAlert = document.getElementById('forgot-alert');
    const forgotSubmitBtn = document.getElementById('forgot-submit-btn');

    if (forgotLink && forgotModal) {
        forgotLink.addEventListener('click', (e) => {
            e.preventDefault();
            hideAlert(forgotAlert);
            forgotModal.classList.remove('hidden');
            document.getElementById('forgot-email')?.focus();
        });
    }

    if (closeForgotBtn && forgotModal) {
        closeForgotBtn.addEventListener('click', () => forgotModal.classList.add('hidden'));
        forgotModal.addEventListener('click', (e) => {
            if (e.target === forgotModal) forgotModal.classList.add('hidden');
        });
    }

    if (forgotForm) {
        forgotForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('forgot-email');
            const email = (emailInput?.value || '').trim();
            if (!email) {
                showAlert(forgotAlert, 'Please enter your account email address.');
                return;
            }

            setButtonLoading(forgotSubmitBtn, true, 'Sending...');
            hideAlert(forgotAlert);

            const { ok, data } = await apiResetPassword(email);
            setButtonLoading(forgotSubmitBtn, false);

            if (ok && data.success) {
                showAlert(forgotAlert, data.message || 'Password reset instructions have been dispatched to your email.', 'success');
                if (emailInput) emailInput.value = '';
            } else {
                showAlert(forgotAlert, data.message || 'Failed to dispatch reset email. Please try again.', 'error');
            }
        });
    }

    // 3. Sync topbar on main terminal pages
    syncTopbarUser();
});
