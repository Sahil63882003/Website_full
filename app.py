import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Plain text credentials
CREDENTIALS = {
    'admin': {'password': 'admin123', 'role': 'Admin'},
    'user1': {'password': 'user123', 'role': 'User'}
}

# Card definitions for dynamic rendering
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

# Initialize session state
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
        st.session_state.theme = 'light'  # default theme is light
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = []
    if 'remember_me' not in st.session_state:
        st.session_state.remember_me = False

def authenticate(username, password):
    if username in CREDENTIALS and password == CREDENTIALS[username]['password']:
        return CREDENTIALS[username]['role']
    return None

def inject_enhanced_css():
    theme_class = 'dark-mode' if st.session_state.theme == 'dark' else 'light-mode'
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    :root {{
        --primary-bg: linear-gradient(135deg, #e3e7f1, #f5f7fa);
        --card-bg: #ffffff;
        --text-color: #2d3436;
        --accent-color: #0984e3;
        --button-bg: #0984e3;
        --button-hover: #0652dd;
        --border-color: #dfe6e9;
        --shadow: 0 6px 16px rgba(0,0,0,0.1);
        --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .dark-mode {{
        --primary-bg: linear-gradient(135deg, #2d3436, #3b3f47);
        --card-bg: #4b5157;
        --text-color: #dfe6e9;
        --accent-color: #74b9ff;
        --button-bg: #74b9ff;
        --button-hover: #4b8bff;
        --border-color: #636e72;
        --shadow: 0 6px 16px rgba(0,0,0,0.3);
    }}
    .light-mode {{
        --primary-bg: linear-gradient(135deg, #e3e7f1, #f5f7fa);
        --card-bg: #ffffff;
        --text-color: #2d3436;
        --accent-color: #0984e3;
        --button-bg: #0984e3;
        --button-hover: #0652dd;
        --border-color: #dfe6e9;
        --shadow: 0 6px 16px rgba(0,0,0,0.1);
    }}
    html, body, [class*="css"] {{
        margin: 0;
        font-family: var(--font-family);
        background: var(--primary-bg);
        color: var(--text-color);
        transition: all 0.3s ease;
    }}
    .{theme_class}, .{theme_class} [class*="css"], .{theme_class} .stApp {{
        background: var(--primary-bg) !important;
        color: var(--text-color) !important;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .card {{
        border: 1px solid var(--border-color);
        padding: 24px;
        border-radius: 20px;
        text-align: center;
        margin: 12px;
        background-color: var(--card-bg);
        color: var(--text-color);
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        opacity: 0;
        transform: translateY(20px);
        animation: fadeIn 0.6s ease forwards;
        transition: transform 0.3s ease, box-shadow 0.3s ease, opacity 0.5s ease;
    }}
    .card:hover {{
        transform: translateY(-12px) scale(1.05);
        box-shadow: 0 22px 40px rgba(0,0,0,0.2);
    }}
    .card h3 {{
        margin: 0 0 16px;
        font-size: 1.5em;
        font-weight: 700;
        color: var(--accent-color);
        min-height: 48px;
    }}
    .card p {{
        margin: 0 0 24px;
        font-size: 1em;
        color: var(--text-color);
        opacity: 0.85;
        line-height: 1.6;
        flex-grow: 1;
    }}
    .card button {{
        align-self: center;
        background-color: var(--button-bg);
        color: white;
        padding: 14px 36px;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        font-size: 1.1em;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.25s ease;
        box-shadow: 0 6px 12px rgba(9, 132, 227, 0.6);
        user-select: none;
        margin-top: 12px;
        width: 80%;
        max-width: 240px;
    }}
    .card button:hover {{
        background-color: var(--button-hover);
        transform: scale(1.1);
        box-shadow: 0 10px 20px rgba(6, 82, 221, 0.8);
    }}
    .search-bar {{
        width: 100%;
        max-width: 480px;
        margin: 30px auto 20px;
    }}
    .search-bar input {{
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 2px solid var(--accent-color);
        border-radius: 14px;
        padding: 14px 20px;
        font-size: 1.15em;
        width: 100%;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 10px rgba(9, 132, 227, 0.25);
    }}
    .search-bar input::placeholder {{
        color: var(--accent-color);
        opacity: 0.7;
    }}
    .search-bar input:focus {{
        border-color: var(--button-hover);
        outline: none;
        box-shadow: 0 0 10px var(--button-hover);
    }}
    .activity-log-container {{
        max-height: 320px;
        overflow-y: auto;
        border: 1px solid var(--border-color);
        border-radius: 18px;
        padding: 16px 28px;
        background: var(--card-bg);
        box-shadow: var(--shadow);
        color: var(--text-color);
        font-size: 1em;
        line-height: 1.5;
        margin-top: 24px;
        font-family: 'Inter', sans-serif;
        word-break: break-word;
    }}
    .activity-log-container p {{
        margin: 8px 0;
    }}
    .login-container {{
        max-width: 420px;
        margin: 0 auto 60px;
        padding: 40px 40px 36px;
        background-color: var(--card-bg);
        border-radius: 28px;
        box-shadow: var(--shadow);
        border: 1.5px solid var(--accent-color);
    }}
    .stForm {{
        background: transparent !important;
        border: none !important;
    }}
    .sidebar .sidebar-content {{
        background: var(--card-bg);
        border-right: 1px solid var(--border-color);
        color: var(--text-color);
        padding: 28px 24px;
        border-radius: 12px 0 0 12px;
        box-shadow: var(--shadow);
        font-weight: 600;
        font-size: 1em;
    }}
    .sidebar .sidebar-content:hover {{
        background-color: var(--accent-color);
        color: white;
        cursor: pointer;
    }}
    .stButton>button {{
        background-color: var(--button-bg);
        color: white;
        border-radius: 12px;
        padding: 14px 30px;
        font-size: 1.05em;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.25s ease;
        box-shadow: 0 6px 14px rgba(9, 132, 227, 0.7);
        user-select: none;
        width: 100%;
        margin-top: 24px;
    }}
    .stButton>button:hover {{
        background-color: var(--button-hover);
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(6, 82, 221, 0.8);
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: var(--accent-color);
        font-family: var(--font-family);
        font-weight: 700;
        margin-bottom: 0.5em;
    }}
    .dark-mode h1, .dark-mode h2, .dark-mode h3, .dark-mode h4, .dark-mode h5, .dark-mode h6 {{
        color: var(--accent-color);
    }}
    .dark-mode p, .dark-mode .card p, .dark-mode .activity-log-container p {{
        color: var(--text-color);
        opacity: 0.85;
    }}
    .dark-mode .search-bar input::placeholder {{
        color: var(--accent-color);
        opacity: 0.7;
    }}
    .dark-mode .stTextInput > div > div > input,
    .dark-mode .stSelectbox > div > div > select {{
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 2px solid var(--accent-color);
        border-radius: 8px;
    }}
    .dark-mode .stTextInput > div > div > input:focus,
    .dark-mode .stSelectbox > div > div > select:focus {{
        border-color: var(--button-hover);
        box-shadow: 0 0 10px var(--button-hover);
    }}
    .dark-mode .stButton > button {{
        background-color: var(--button-bg);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 30px;
        font-size: 1.05em;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.25s ease;
        box-shadow: 0 6px 14px rgba(9, 132, 227, 0.7);
    }}
    .dark-mode .stButton > button:hover {{
        background-color: var(--button-hover);
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(6, 82, 221, 0.8);
    }}
    .dark-mode .stForm {{
        background: transparent !important;
    }}
    .dark-mode .stCheckbox > label > div {{
        background-color: var(--card-bg);
        border: 2px solid var(--accent-color);
    }}
    .dark-mode .stCheckbox > label > div > div {{
        background-color: var(--accent-color);
    }}
    .cards-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 18px 18px;
        max-width: 1200px;
        margin: 0 auto 48px;
        padding: 0 8px;
    }}
    @media (max-width: 600px) {{
        .card {{
            min-height: 250px;
            padding: 20px;
        }}
        .card h3 {{
            font-size: 1.3em;
        }}
        .card p {{
            font-size: 0.95em;
        }}
        .search-bar {{
            max-width: 100%;
            margin: 24px 12px 20px;
        }}
        .dark-mode .card {{
            min-height: 220px;
            padding: 16px;
        }}
        .dark-mode .card h3 {{
            font-size: 1.2em;
        }}
        .dark-mode .card p {{
            font-size: 0.9em;
        }}
        .dark-mode .search-bar input {{
            font-size: 1em;
            padding: 12px 16px;
        }}
        .dark-mode .login-container {{
            padding: 20px;
            margin: 20px 10px;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def login_page():
    inject_enhanced_css()
    st.title("🔐 Secure Dashboard")
    st.markdown("<h3 style='text-align: center; color: var(--accent-color); font-weight: 700;'>Welcome to Your Control Hub</h3>", unsafe_allow_html=True)

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
                    st.success(f"Welcome back, {username}!")
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
            <div class="card fade-in">
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
    inject_enhanced_css()
    st.title("🛠️ Admin Control Center")
    st.markdown(
        f"""
        <div style='background: var(--card-bg); padding: 28px; border-radius: 20px; margin-bottom: 32px; box-shadow: var(--shadow);'>
            <h2 style='color: var(--accent-color); margin: 0;'>Welcome, {st.session_state.username}!</h2>
            <p style='color: var(--text-color); opacity: 0.85; font-size: 1.1em; margin-top: 8px;'>Manage tools, monitor activities, and configure settings.</p>
            <p style="color: var(--text-color); opacity:0.6; font-size:0.9em; margin-top: 12px;">
            Current server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True
    )

    search_query = st.text_input(
        "Search Tools",
        placeholder="Type to search tools...",
        key="admin_search",
        help="Search for a specific tool by name",
        label_visibility="visible"
    )

    st.subheader("Admin Tools")
    render_cards('Admin', search_query)

    st.subheader("User Activity Log")

    filter_log = st.text_input("Filter activities (keyword/date)", placeholder="Filter activity log...", key="admin_log_filter", label_visibility="visible")
    filtered_log = [log for log in st.session_state.activity_log if filter_log.lower() in log.lower()] if filter_log else st.session_state.activity_log

    st.markdown("<div class='activity-log-container'>", unsafe_allow_html=True)
    if filtered_log:
        for log in filtered_log[-50:][::-1]:
            st.markdown(f"<p>- {log}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: var(--text-color);'>No matching activity recorded.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    export_activity_log()

def user_page():
    inject_enhanced_css()
    st.title("👤 User Dashboard")
    st.markdown(
        f"""
        <div style='background: var(--card-bg); padding: 28px; border-radius: 20px; margin-bottom: 32px; box-shadow: var(--shadow);'>
            <h2 style='color: var(--accent-color); margin: 0;'>Hello, {st.session_state.username}!</h2>
            <p style='color: var(--text-color); opacity: 0.85; font-size: 1.1em; margin-top: 8px;'>Access your tools and manage your tasks below.</p>
            <p style="color: var(--text-color); opacity:0.6; font-size:0.9em; margin-top: 12px;">Current server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True
    )

    search_query = st.text_input(
        "Search Tools",
        placeholder="Search for a tool...",
        key="user_search",
        help="Search for a specific tool by name",
        label_visibility="visible"
    )

    st.subheader("User Tools")
    render_cards('User', search_query)

def logout():
    st.session_state.activity_log.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {st.session_state.username} logged out")
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.last_activity = None
    st.session_state.remember_me = False
    st.session_state.theme = 'light'  # Reset to light theme on logout
    st.success("You have been logged out.")

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
                <div style='background: var(--card-bg); padding: 18px; border-radius: 14px; box-shadow: var(--shadow); margin-bottom: 24px;'>
                    <p style='color: var(--text-color); margin: 0 0 10px; font-weight: 600; font-size: 1em;'><strong>Username:</strong> {st.session_state.username}</p>
                    <p style='color: var(--text-color); margin: 0 0 10px; font-weight: 600; font-size: 1em;'><strong>Role:</strong> {st.session_state.role}</p>
                    <p style='color: var(--text-color); font-weight: 600; font-size: 0.95em; margin: 0;'><strong>Last Login:</strong> {st.session_state.last_activity.strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                """, unsafe_allow_html=True
            )
            # Theme toggle button
            if st.button("Toggle Dark Mode", key="theme_toggle_button"):
                st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
                st.rerun()

            if st.button("Logout", key="sidebar_logout", type="primary"):
                logout()
                st.rerun()

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
                st.rerun()

if __name__ == "__main__":
    main()
