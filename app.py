import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import shap
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SHIELD_PRO_OS", layout="wide", page_icon="⚡")

# ---------------- SHARED UI SHADER (Login & Main) ----------------
def apply_unified_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=JetBrains+Mono:wght@300;500&display=swap');

    /* BASE BACKGROUND - Matching Login */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #0a1128 0%, #000814 100%) !important;
    }

    /* CRT SCANLINE EFFECT */
    [data-testid="stAppViewContainer"]::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.04), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.04));
        z-index: 2;
        background-size: 100% 3px, 3px 100%;
        pointer-events: none;
    }

    /* NEON TITLES */
    .shield-logo {
        font-family: 'Orbitron', sans-serif;
        color: #00f2fe;
        text-align: center;
        font-size: 60px;
        font-weight: 900;
        letter-spacing: 10px;
        text-shadow: 0 0 20px #00f2fe;
    }

    /* GLASS CARDS */
    .terminal-card {
        background: rgba(0, 10, 20, 0.85);
        border: 1px solid #00f2fe;
        padding: 25px;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 5px;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    
    .terminal-card:hover {
        border: 1px solid #4facfe;
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.3);
    }

    /* NEON BUTTONS */
    .stButton>button {
        background: transparent !important;
        color: #00f2fe !important;
        border: 1px solid #00f2fe !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        width: 100%;
        transition: 0.4s;
    }

    .stButton>button:hover {
        background: #00f2fe !important;
        color: #000 !important;
        box-shadow: 0 0 30px #00f2fe;
    }

    /* TABS STYLING */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        color: #4facfe;
        font-family: 'Orbitron';
        background-color: rgba(0,0,0,0.5);
        border: 1px solid #00f2fe;
        margin-right: 10px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: white !important;
        background: #00f2fe !important;
    }

    /* METRICS */
    div[data-testid="stMetric"] {
        background: rgba(0, 242, 254, 0.05);
        border-left: 3px solid #00f2fe;
        padding: 15px;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00f2fe !important;
        font-family: 'Orbitron';
    }

    /* DATAFRAME */
    .stDataFrame { border: 1px solid #00f2fe; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 8, 20, 0.95) !important;
        border-right: 1px solid #00f2fe;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "auth" not in st.session_state: st.session_state.auth = False
if "logs" not in st.session_state: st.session_state.logs = []
if "current" not in st.session_state: st.session_state.current = None

# ---------------- LOGIN PAGE ----------------
def login_page():
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.markdown('<div class="shield-logo">SHIELD</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#4facfe; font-family:\'JetBrains Mono\'">>_ UPI_PROTECTOR_CORE_v3.0.1</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(0,0,0,0.9); padding:10px; border:1px solid #00f2fe; font-family:'JetBrains Mono'; font-size:11px; color:#00f2fe; margin-bottom:20px;">
            [SYSTEM] ENCRYPTION ACTIVE<br>
            [UPLINK] GATEWAY: 192.168.1.104<br>
            [STATUS] WAITING FOR ADMIN AUTH...
        </div>
        """, unsafe_allow_html=True)
        
        u = st.text_input("ADMIN_USER", placeholder="ROOT")
        p = st.text_input("PASS_KEY", type="password", placeholder="••••")
        
        if st.button("INITIALIZE_SYSTEM"):
            if u == "admin" and p == "1234":
                with st.spinner("AUTHENTICATING..."):
                    time.sleep(1)
                    st.session_state.auth = True
                    st.rerun()
            else: st.error("ERR: ACCESS_DENIED")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
def main_app():
    # Asset Loading
    @st.cache_resource
    def load_model():
        try: return joblib.load("models/fraud_model.pkl")
        except: return None

    @st.cache_data
    def load_data():
        try: return pd.read_csv("Data/creditcard.csv")
        except: return pd.DataFrame(np.random.randn(10, 31), columns=[f'V{i}' for i in range(1, 29)] + ['Time', 'Amount', 'Class'])

    model = load_model()
    data = load_data()

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='font-family:Orbitron; color:#00f2fe;'>OS_MENU</h2>", unsafe_allow_html=True)
        mode = st.radio("STRATEGY", ["Monitor", "Auto Block", "Manual Review"])
        st.divider()
        if st.button("TERMINATE SESSION"):
            st.session_state.auth = False
            st.rerun()

    # Dashboard Header
    st.markdown('<div class="shield-logo" style="font-size:40px; text-align:left;">COMMAND_CENTER</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4facfe; font-family:\'JetBrains Mono\'">>_ STATUS: CONNECTED | MODE: '+mode+'</p>', unsafe_allow_html=True)

    # holographic Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("TOTAL_STREAM", f"{len(data):,}")
    with m2:
        st.metric("THREAT_LOG", len(data[data["Class"]==1]), delta="LIVE", delta_color="inverse")
    with m3:
        st.metric("LATENCY", "4ms")

    st.write("")

    tab1, tab2 = st.tabs([">_ PACKET_INSPECTOR", ">_ BULK_BUFFER"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("INTERCEPT RANDOM"):
                st.session_state.current = data.sample(1)
        with c2:
            if st.button("INTERCEPT FRAUD"):
                st.session_state.current = data[data["Class"]==1].sample(1)

        if st.session_state.current is not None:
            st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
            st.dataframe(st.session_state.current, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if model:
                features = st.session_state.current.drop("Class", axis=1).values
                prob = model.predict_proba(features)[0][1]

                st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
                st.markdown(f"### AI RISK ASSESSMENT: <span style='color:#00f2fe;'>{prob:.2%}</span>", unsafe_allow_html=True)
                
                if prob > 0.7:
                    st.error("🚨 CRITICAL THREAT DETECTED")
                    status = "Blocked" if mode == "Auto Block" else "Flagged"
                elif prob > 0.3:
                    st.warning("⚠️ ANOMALY DETECTED")
                    status = "Review"
                else:
                    st.success("✅ PACKET SECURE")
                    status = "Approved"
                
                st.markdown(f"**PROTOCOL DECISION:** `{status}`")
                st.markdown('</div>', unsafe_allow_html=True)

                # Log
                st.session_state.logs.append({
                    "Time": time.strftime("%H:%M:%S"),
                    "Amt": float(st.session_state.current["Amount"].values[0]),
                    "Risk": f"{prob:.2%}",
                    "Status": status
                })

                with st.expander("VIEW NEURAL BREAKDOWN"):
                    explainer = shap.Explainer(model)
                    shap_values = explainer(features)
                    fig, ax = plt.subplots(facecolor='none')
                    shap.plots.waterfall(shap_values[0], show=False)
                    st.pyplot(fig)
            else:
                st.info("System Notification: AI Model Offline. UI Preview Mode Active.")

    with tab2:
        st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
        file = st.file_uploader("LOAD_DATA_STREAM", type=["csv"])
        if file:
            st.success("Data loaded. Buffer ready for analysis.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Activity Log
    st.markdown("### RECENT_ACTIVITY_LOG")
    if st.session_state.logs:
        st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
        st.table(pd.DataFrame(st.session_state.logs).tail(5))
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- EXECUTION ----------------
apply_unified_ui()
if st.session_state.auth:
    main_app()
else:
    login_page()