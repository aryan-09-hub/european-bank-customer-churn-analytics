import streamlit as st


st.set_page_config(
    page_title="RetainIQ | European Banking",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#0b1326"
PANEL = "#171f33"
PANEL_RAISED = "#222a3d"
STROKE = "#313b51"
TEXT = "#e8edfb"
MUTED = "#a3adc4"
BLUE = "#70a5ff"
GREEN = "#4edea3"
ROSE = "#ff7185"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700&display=swap');
    :root {{ color-scheme: dark; }}
    html, body, [data-testid="stAppViewContainer"] {{ background: {NAVY}; color: {TEXT}; }}
    [data-testid="stHeader"] {{ background: rgba(11,19,38,.88); }}
    [data-testid="stSidebar"] {{ background: #080f20; border-right: 1px solid {STROKE}; }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color: {MUTED}; }}
    .block-container {{ max-width: 1440px; padding: 2rem 2.4rem 3rem; }}
    h1, h2, h3 {{ font-family: 'Plus Jakarta Sans', Inter, sans-serif; letter-spacing: -.025em; color: {TEXT}; }}
    h1 {{ font-size: 2rem; margin-bottom: .3rem; }}
    h2 {{ font-size: 1.2rem; }}
    p, label, div {{ font-family: Inter, sans-serif; }}
    .eyebrow {{ color: {BLUE}; text-transform: uppercase; letter-spacing: .14em; font-size: .69rem; font-weight: 700; }}
    .subtle {{ color: {MUTED}; font-size: .91rem; }}
    .brand {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.2rem; font-weight: 700; color: {TEXT}; }}
    .brand-mark {{ display:inline-grid; place-items:center; width:2rem; height:2rem; margin-right:.55rem; border-radius:.6rem; color:{BLUE}; background:#152749; border:1px solid #2d4774; }}
    .status {{ display:inline-flex; align-items:center; gap:.45rem; padding:.4rem .7rem; border:1px solid {STROKE}; border-radius:999px; background:{PANEL}; color:{MUTED}; font-size:.78rem; }}
    .status-dot {{ width:.48rem; height:.48rem; border-radius:50%; background:#f6b94a; }}
    .kpi {{ background:linear-gradient(150deg, {PANEL_RAISED}, {PANEL} 70%); border:1px solid {STROKE}; border-radius:14px; padding:18px 20px; min-height:132px; }}
    .kpi-label {{ color:{MUTED}; font-size:.79rem; font-weight:600; }}
    .kpi-value {{ font-family:'Plus Jakarta Sans',sans-serif; color:{TEXT}; font-size:1.9rem; font-weight:700; line-height:1.25; margin:.45rem 0 .15rem; }}
    .kpi-note {{ color:#7f8aa5; font-size:.75rem; }}
    .panel {{ background:{PANEL}; border:1px solid {STROKE}; border-radius:14px; padding:18px 20px; min-height:230px; }}
    .panel-title {{ font-family:'Plus Jakarta Sans',sans-serif; font-size:1rem; font-weight:600; margin:0 0 .25rem; }}
    .panel-copy {{ color:{MUTED}; font-size:.82rem; }}
    .empty {{ display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; min-height:145px; color:#7f8aa5; border:1px dashed #3a465f; border-radius:10px; margin-top:1rem; padding:1rem; }}
    .empty-icon {{ font-size:1.5rem; color:{BLUE}; margin-bottom:.4rem; }}
    .table-placeholder {{ margin-top:1rem; padding:1.1rem; border-radius:10px; color:#7f8aa5; background:#111a2d; border:1px dashed #3a465f; font-size:.85rem; }}
    [data-testid="stSelectbox"] > div > div, [data-testid="stMultiSelect"] > div > div {{ background:{PANEL}; border-color:{STROKE}; }}
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {{ gap:1rem; }}
    @media (max-width: 760px) {{ .block-container {{ padding:1.2rem 1rem 2rem; }} h1 {{ font-size:1.6rem; }} .kpi {{ padding:15px; min-height:120px; }} .kpi-value {{ font-size:1.55rem; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">◈</span>RetainIQ</div>', unsafe_allow_html=True)
    st.caption("EUROPEAN BANKING ANALYTICS")
    st.divider()
    st.markdown("**WORKSPACE**")
    section = st.radio(
        "Dashboard sections",
        ["Overview", "Geography & demographics", "Customer segments", "High-value explorer"],
        index=0,
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown('<span class="status"><span class="status-dot"></span> Data not connected</span>', unsafe_allow_html=True)
    st.markdown("\n")
    st.caption("Customer Segmentation & Churn Pattern Analytics")

if section != "Overview":
    upcoming = {
        "Geography & demographics": "Country, age, and gender comparisons will be added in a later project milestone.",
        "Customer segments": "Segment definitions and comparisons will be added in a later project milestone.",
        "High-value explorer": "High-value customer criteria and analysis will be added in a later project milestone.",
    }
    st.markdown('<div class="eyebrow">Workspace · in progress</div>', unsafe_allow_html=True)
    st.title(section)
    st.markdown(
        f'<div class="panel"><div class="panel-title">This section is coming soon</div><div class="panel-copy">{upcoming[section]}</div><div class="table-placeholder">The Overview is the active page for the current UI milestone. No figures are displayed on this placeholder page.</div></div>',
        unsafe_allow_html=True,
    )
    st.stop()

head_left, head_right = st.columns([5, 2])
with head_left:
    st.markdown('<div class="eyebrow">Executive workspace</div>', unsafe_allow_html=True)
    st.title("Customer churn overview")
    st.markdown('<div class="subtle">A clear view of customer retention across European markets.</div>', unsafe_allow_html=True)
with head_right:
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:right"><span class="status"><span class="status-dot"></span> Awaiting data connection</span></div>', unsafe_allow_html=True)

st.markdown("\n")
st.markdown('<div class="eyebrow">Filters · preview</div>', unsafe_allow_html=True)
filter_cols = st.columns([1.25, 1.25, 1.25, 1.1, 1.1])
with filter_cols[0]:
    st.selectbox("Geography", ["All countries", "France", "Germany", "Spain"], disabled=True)
with filter_cols[1]:
    st.selectbox("Age group", ["All age groups", "Under 30", "30–45", "46–59", "60+"], disabled=True)
with filter_cols[2]:
    st.selectbox("Customer status", ["All customers", "Retained", "Churned"], disabled=True)
with filter_cols[3]:
    st.selectbox("Tenure", ["All tenure", "New", "Mid-term", "Long-term"], disabled=True)
with filter_cols[4]:
    st.markdown("<div style='height:1.85rem'></div>", unsafe_allow_html=True)
    st.button("Reset filters", disabled=True, use_container_width=True)

st.markdown("\n")
metric_cols = st.columns(4)
metrics = [
    ("TOTAL CUSTOMERS", "—", "Connect the dataset to view customer count", BLUE),
    ("OVERALL CHURN RATE", "—", "Calculated from the Exited field", ROSE),
    ("CHURNED CUSTOMERS", "—", "Customer records where Exited = 1", ROSE),
    ("RETAINED CUSTOMERS", "—", "Customer records where Exited = 0", GREEN),
]
for col, (label, value, note, accent) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{accent}">{value}</div><div class="kpi-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("\n")
chart_left, chart_right = st.columns([1.15, 1])
with chart_left:
    st.markdown('<div class="panel"><div class="panel-title">Churn by geography</div><div class="panel-copy">Compare customer exit rates across France, Germany, and Spain.</div><div class="empty"><div class="empty-icon">▥</div><strong>Chart placeholder</strong><span>Geography analysis will appear when the dataset is connected.</span></div></div>', unsafe_allow_html=True)
with chart_right:
    st.markdown('<div class="panel"><div class="panel-title">Customer status mix</div><div class="panel-copy">Retained and churned customers across the selected population.</div><div class="empty"><div class="empty-icon">◉</div><strong>Chart placeholder</strong><span>Customer counts and proportions are not loaded yet.</span></div></div>', unsafe_allow_html=True)

st.markdown("\n")
st.markdown('<div class="panel"><div class="panel-title">Segment snapshot</div><div class="panel-copy">A preview of the segment comparison table.</div><div class="table-placeholder">Segment data will be shown here after connecting and validating the customer dataset.</div></div>', unsafe_allow_html=True)

st.markdown("\n")
st.caption("Overview layout preview · No analytics or sample figures are shown in this milestone.")
