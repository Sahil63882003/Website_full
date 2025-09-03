import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import uuid

# Plain text credentials
CREDENTIALS = {
    'admin': {
        'password': 'admin123',
        'role': 'Admin'
    },
    'user1': {
        'password': 'user123',
        'role': 'User'
    }
}

# Initialize session state variables
def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = None
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = []
    if 'remember_me' not in st.session_state:
        st.session_state.remember_me = False

# Card definitions
CARDS = {
    'JAINAM': {
        'description': 'Access Jainam administration tools.',
        'url': 'https://jainam1sahil.streamlit.app/',
        'roles': ['Admin']
    },
    'REALIZED PNL FOR 19': {
        'description': 'View realized profit and loss for 19.',
        'url': 'https://algo19realizedandunrealized.streamlit.app/',
        'roles': ['Admin']
    },
    'STRATEGY AUTOMATION': {
        'description': 'Manage and automate trading strategies.',
        'url': 'https://strategiesautomationbysahil.streamlit.app/',
        'roles': ['Admin', 'User']
    },
    'SUMMARY AUTOMATION': {
        'description': 'Generate automated summaries.',
        'url': 'https://summaryautomationgaurav.streamlit.app/',
        'roles': ['Admin', 'User']
    },
    'HEDGE AUTOMATION': {
        'description': 'Automate orderbook hedge operations.',
        'url': 'https://gauravobhedge.streamlit.app/',
        'roles': ['Admin', 'User']
    },
    'VAR CALCULATION': {
        'description': 'Calculate Value at Risk.',
        'url': 'https://varprosahil.streamlit.app/',
        'roles': ['Admin', 'User']
    },
    'USERSETTING CHECK': {
        'description': 'Manage user settings and configurations.',
        'url': 'https://usersetting.streamlit.app/',
        'roles': ['Admin']
    }
}

def authenticate(username, password):
    if username in CREDENTIALS and password == CREDENTIALS[username]['password']:
        return CREDENTIALS[username]['role']
    return None

def inject_enhanced_css():
    theme_class = 'dark-mode' if st.session_state.theme == 'dark' else 'light-mode'
    st.markdown(f"""
    <style>
    :root {{
        --primary-bg: linear-gradient(135deg, #f0f4ff, #e3e7f1);
        --card-bg: #ffffff;
        --text-color: #1a1a2e;
        --accent-color: #3b82f6;
        --button-bg: #3b82f6;
        --button-hover: #2563eb;
        --border-color: #e2e8f0;
        --shadow: 0 8px 24px rgba(0,0,0,0.12);
        --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --transition: all 0.3s ease-in-out;
    }}
    .dark-mode {{
        --primary-bg: linear-gradient(135deg, #1f2937, #374151);
        --card-bg: #2d3748;
        --text-color: #e5e7eb;
        --accent-color: #60a5fa;
        --button-bg: #60a5fa;
        --button-hover: #3b82f6;
        --border-color: #4b5563;
        --shadow: 0 8px 24px rgba(0,0,0,0.4);
    }}
    body {{
        margin: 0;
        font-family: var(--font-family);
        background: var(--primary-bg);
        color: var(--text-color);
        transition: var(--transition);
    }}
    .{theme_class} body, .{theme_class} .card, .{theme_class} .login-container, 
    .{theme_class} .activity-log-container, .{theme_class} .sidebar .sidebar-content {{
        background: var(--primary-bg);
        color: var(--text-color);
    }}
    .card {{
        border: 1px solid var(--border-color);
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        margin: 12px;
        background-color: var(--card-bg);
        color: var(--text-color);
        transition: transform 0.4s ease, box-shadow 0.4s ease, background-color 0.4s ease;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        animation: fadeIn 0.5s ease-in-out;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 12px 32px rgba(0,0,0,0.2);
    }}
    .card h3 {{
        margin: 0 0 12px;
        font-size: 1.4em;
        font-weight: 700;
        color: var(--accent-color);
        min-height: 48px;
        transition: var(--transition);
    }}
    .card p {{
        margin: 0 0 20px;
        font-size: 0.95em;
        color: var(--text-color);
        opacity: 0.9;
        line-height: 1.6;
        flex-grow: 1;
    }}
    .card button {{
        align-self: center;
        background: var(--button-bg);
        color: white;
        padding: 12px 32px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-size: 1em;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        width: 80%;
        max-width: 220px;
    }}
    .card button:hover {{
        background: var(--button-hover);
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    }}
    .search-bar {{
        width: 100%;
        max-width: 500px;
        margin: 32px auto 24px;
        position: relative;
    }}
    .search-bar input {{
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 2px solid var(--accent-color);
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 1.1em;
        width: 100%;
        transition: var(--transition);
        box-shadow: var(--shadow);
    }}
    .search-bar input::placeholder {{
        color: var(--accent-color);
        opacity: 0.6;
    }}
    .search-bar input:focus {{
        border-color: var(--button-hover);
        outline: none;
        box-shadow: 0 0 12px var(--button-hover);
    }}
    .activity-log-container {{
        max-height: 350px;
        overflow-y: auto;
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        background: var(--card-bg);
        box-shadow: var(--shadow);
        color: var(--text-color);
        font-size: 0.95em;
        line-height: 1.6;
        margin-top: 24px;
        animation: slideIn 0.5s ease-in-out;
    }}
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    .activity-log-container p {{
        margin: 6px 0;
        transition: var(--transition);
    }}
    .login-container {{
        max-width: 450px;
        margin: 40px auto;
        padding: 32px;
        background-color: var(--card-bg);
        border-radius: 20px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        animation: fadeIn 0.6s ease-in-out;
    }}
    .stForm {{
        background: transparent !important;
        border: none !important;
    }}
    .sidebar .sidebar-content {{
        background: var(--card-bg);
        border-right: 1px solid var(--border-color);
        color: var(--text-color);
        padding: 24px;
        border-radius: 12px 0 0 12px;
        box-shadow: var(--shadow);
        font-weight: 600;
        font-size: 0.95em;
    }}
    .sidebar .sidebar-content p {{
        margin: 4px 0 12px;
        font-weight: 600;
    }}
    .stButton>button {{
        background: var(--button-bg);
        color: white;
        border-radius: 10px;
        padding: 12px 28px;
        font-size: 1em;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        width: 100%;
        margin-top: 20px;
    }}
    .stButton>button:hover {{
        background: var(--button-hover);
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: var(--accent-color);
        font-family: var(--font-family);
        font-weight: 700;
        margin-bottom: 0.6em;
    }}
    .dark-mode h1, .dark-mode h2, .dark-mode h3, .dark-mode h4, .dark-mode h5, .dark-mode h6 {{
        color: var(--accent-color);
    }}
    .dark-mode p, .dark-mode .card p, .dark-mode .activity-log-container p {{
        color: var(--text-color);
        opacity: 0.9;
    }}
    .dark-mode .search-bar input::placeholder {{
        color: var(--accent-color);
        opacity: 0.6;
    }}
    .dark-mode .stTextInput > div > input,
    .dark-mode .stSelectbox > div > select {{
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 2px solid var(--accent-color);
        border-radius: 10px;
        transition: var(--transition);
    }}
    .dark-mode .stTextInput > div > input:focus,
    .dark-mode .stSelectbox > div > select:focus {{
        border-color: var(--button-hover);
        box-shadow: 0 0 12px var(--button-hover);
    }}
    .theme-toggle {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 16px 0;
    }}
    .theme-toggle label {{
        color: var(--text-color);
        font-weight: 600;
    }}
    .cards-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 20px;
        max-width: 1280px;
        margin: 0 auto 48px;
        padding: 0 12px;
    }}
    @media (max-width: 768px) {{
        .card {{
            min-height: 200px;
            padding: 20px;
        }}
        .card h3 {{
            font-size: 1.3em;
        }}
        .card p {{
            font-size: 0.9em;
        }}
        .search-bar {{
            max-width: 90%;
            margin: 24px 16px;
        }}
        .login-container {{
            padding: 24px;
            margin: 24px 12px;
        }}
    }}
    @media (max-width: 480px) {{
        .card {{
            min-height: 180px;
            padding: 16px;
        }}
        .card h3 {{
            font-size: 1.2em;
        }}
        .card p {{
            font-size: 0.85em;
        }}
        .search-bar input {{
            font-size: 1em;
            padding: 10px 16px;
        }}
        .login-container {{
            padding: 20px;
            margin: 20px 8px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def login_page():
    st.title("🔐 Secure Dashboard")
    st.markdown("<h3 style='text-align: center; color: var(--accent-color); font-weight: 700;'>Your Gateway to Control</h3>", unsafe_allow_html=True)

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    with st.form(key='login_form'):
        username = st.text_input("User ID", placeholder="Enter your username", key="username_input")
        password = st.text_input("Password", placeholder="Enter your password", type="password", key="password_input")
        role = st.selectbox("Role", ["Admin", "User"], key="role_select")
        remember_me = st.checkbox("Remember Me", key="remember_me_check")
        submit = st.form_submit_button("Login", type="primary")

        if submit:
            with st.spinner("Authenticating..."):
                auth_role = authenticate(username, password)
                if auth_role and auth_role == role:
                    st.session_state.authenticated = True
                    st.session_state.role = auth_role
                    st.session_state.username = username
                    st.session_state.last_activity = datetime.now()
                    st.session_state.remember_me = remember_me
                    st.session_state.activity_log.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {username} logged in as {auth_role}")
                    st.balloons()
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials or role selection.")
    st.markdown("</div>", unsafe_allow_html=True)

def render_cards(role, search_query=""):
    inject_enhanced_css()
    filtered_cards = [
        card for card, details in CARDS.items()
        if role in details['roles'] and search_query.lower() in card.lower()
    ]

    st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
    for card_name in filtered_cards:
        card = CARDS[card_name]
        st.markdown(
            f"""
            <div class="card">
                <h3>{card_name}</h3>
                <p>{card['description']}</p>
                <a href="{card['url']}" target="_blank"><button>Open</button></a>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def export_activity_log():
    if st.session_state.activity_log:
        df = pd.DataFrame(st.session_state.activity_log, columns=["Activity Log"])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Activity Log as CSV",
            data=csv,
            file_name='activity_log.csv',
            mime='text/csv',
            key='export_log'
        )

def admin_page():
    st.title("🛠️ Admin Control Center")
    st.markdown(
        f"""
        <div style='background: var(--card-bg); padding: 24px; border-radius: 16px; margin-bottom: 32px; box-shadow: var(--shadow); animation: fadeIn 0.5s ease-in-out;'>
            <h2 style='color: var(--accent-color); margin: 0;'>Welcome, {st.session_state.username}!</h2>
            <p style='color: var(--text-color); opacity: 0.9; font-size: 1.05em; margin-top: 8px;'>Manage tools and monitor activities.</p>
            <p style="color: var(--text-color); opacity:0.7; font-size:0.9em; margin-top: 12px;">
            Current server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True
    )

    search_query = st.text_input(
        "Search Tools",
        placeholder="Search tools by name...",
        key="admin_search",
        help="Find a specific tool quickly",
        label_visibility="visible"
    )

    st.subheader("Available Tools")
    render_cards('Admin', search_query)

    st.subheader("User Activity Log")
    filter_log = st.text_input("Filter Activities", placeholder="Filter by keyword or date...", key="admin_log_filter", label_visibility="visible")
    filtered_log = [log for log in st.session_state.activity_log if filter_log.lower() in log.lower()] if filter_log else st.session_state.activity_log

    st.markdown("<div class='activity-log-container'>", unsafe_allow_html=True)
    if filtered_log:
        for log in filtered_log[-50:][::-1]:
            st.markdown(f"<p>- {log}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: var(--text-color);'>No matching activities found.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    export_activity_log()

def user_page():
    st.title("👤 User Dashboard")
    st.markdown(
        f"""
        <div style='background: var(--card-bg); padding: 24px; border-radius: 16px; margin-bottom: 32px; box-shadow: var(--shadow); animation: fadeIn 0.5s ease-in-out;'>
            <h2 style='color: var(--accent-color); margin: 0;'>Hello, {st.session_state.username}!</h2>
            <p style='color: var(--text-color); opacity: 0.9; font-size: 1.05em; margin-top: 8px;'>Access your tools below.</p>
            <p style="color: var(--text-color); opacity:0.7; font-size:0.9em; margin-top: 12px;">
            Current server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True
    )

    search_query = st.text_input(
        "Search Tools",
        placeholder="Search tools by name...",
        key="user_search",
        help="Find a specific tool quickly",
        label_visibility="visible"
    )

    st.subheader("Available Tools")
    render_cards('User', search_query)

def logout():
    st.session_state.activity_log.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {st.session_state.username} logged out")
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.last_activity = None
    st.session_state.remember_me = False
    st.success("You have been logged out.")
    st.rerun()

def check_session_timeout():
    if st.session_state.last_activity and not st.session_state.remember_me:
        if datetime.now() - st.session_state.last_activity > timedelta(minutes=15):
            logout()
            st.error("Session timed out due to inactivity. Please log in again.")
            return False
    return True

def main():
    initialize_session_state()

    st.set_page_config(
        page_title="Secure Dashboard",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.markdown("<h2 style='color: var(--accent-color); font-weight: 700; margin-bottom: 16px;'>Control Dashboard</h2>", unsafe_allow_html=True)
        if st.session_state.authenticated:
            st.markdown(
                f"""
                <div style='background: var(--card-bg); padding: 16px; border-radius: 12px; box-shadow: var(--shadow); margin-bottom: 20px;'>
                    <p style='color: var(--text-color); margin: 0 0 8px; font-weight: 600; font-size: 0.95em;'><strong>Username:</strong> {st.session_state.username}</p>
                    <p style='color: var(--text-color); margin: 0 0 8px; font-weight: 600; font-size: 0.95em;'><strong>Role:</strong> {st.session_state.role}</p>
                    <p style='color: var(--text-color); font-weight: 600; font-size: 0.9em; margin: 0;'><strong>Last Login:</strong> {st.session_state.last_activity.strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                """, unsafe_allow_html=True
            )
            theme = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == 'light' else 1, key="theme_select")
            if theme.lower() != st.session_state.theme:
                st.session_state.theme = theme.lower()
                st.rerun()
            if st.button("Logout", key="sidebar_logout", type="primary"):
                logout()

    if st.session_state.authenticated and not check_session_timeout():
        return

    if not st.session_state.authenticated:
        login_page()
    else:
        st.session_state.last_activity = datetime.now()
        if st.session_state.role == "Admin":
            admin_page()
        elif st.session_state.role == "User":
            user_page()
        else:
            st.error("Unauthorized role. Please logout and login again.")
            if st.button("Logout", key="unauthorized_logout", type="primary"):
                logout()

if __name__ == "__main__":
    main()