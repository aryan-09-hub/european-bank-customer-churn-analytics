from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="RetainIQ | European Banking",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


DATA_FILE = Path(__file__).resolve().parent / "European_Bank.csv"
REQUIRED_COLUMNS = {
    "CustomerId",
    "Surname",
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
}
BINARY_COLUMNS = ("HasCrCard", "IsActiveMember", "Exited")


class DataValidationError(ValueError):
    """Raised when the customer file cannot safely support the overview KPIs."""


@st.cache_data(show_spinner="Loading and validating customer data…")
def load_customer_data(path: str) -> pd.DataFrame:
    customers = pd.read_csv(path)
    missing_columns = sorted(REQUIRED_COLUMNS.difference(customers.columns))
    if missing_columns:
        raise DataValidationError(
            "The customer file is missing required columns: " + ", ".join(missing_columns)
        )
    if customers.empty:
        raise DataValidationError("The customer file contains no records.")
    if customers["CustomerId"].isna().any():
        raise DataValidationError("CustomerId contains blank values.")
    duplicate_ids = int(customers["CustomerId"].duplicated().sum())
    if duplicate_ids:
        raise DataValidationError(f"CustomerId contains {duplicate_ids:,} duplicate records.")

    for column in BINARY_COLUMNS:
        values = pd.to_numeric(customers[column], errors="coerce")
        invalid = values.isna() | ~values.isin((0, 1))
        if invalid.any():
            raise DataValidationError(
                f"{column} must contain only 0 or 1; found {int(invalid.sum()):,} invalid records."
            )
        customers[column] = values.astype("int8")

    return customers


def summarize_churn(data: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Return customer counts and churn rates for one analysis dimension."""
    return (
        data.groupby(dimension, observed=False, dropna=False)["Exited"]
        .agg(Customers="size", Churned="sum", Churn_Rate="mean")
        .reset_index()
    )


def style_chart(figure, height: int = 330):
    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": TEXT},
        margin={"l": 12, "r": 12, "t": 24, "b": 12},
        height=height,
        showlegend=False,
    )
    figure.update_yaxes(tickformat=".0%", gridcolor=STROKE, zeroline=False)
    figure.update_xaxes(gridcolor=STROKE, zeroline=False)
    return figure


def build_segmented_data(data: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    """Add documented, analysis-only segment labels derived from the source data."""
    segmented = data.copy()
    segmented["Age group"] = pd.cut(
        segmented["Age"],
        bins=[-float("inf"), 29, 45, 59, float("inf")],
        labels=["Under 30", "30–45", "46–59", "60+"],
    )

    credit_low = int(data["CreditScore"].quantile(1 / 3))
    credit_high = int(data["CreditScore"].quantile(2 / 3))
    segmented["Credit score"] = pd.cut(
        segmented["CreditScore"],
        bins=[-float("inf"), credit_low, credit_high, float("inf")],
        labels=["Low", "Medium", "High"],
    )

    segmented["Tenure group"] = pd.cut(
        segmented["Tenure"],
        bins=[-float("inf"), 2, 6, float("inf")],
        labels=["New (0–2 years)", "Mid-term (3–6 years)", "Long-term (7+ years)"],
    )

    positive_balance_median = data.loc[data["Balance"].gt(0), "Balance"].median()
    segmented["Balance group"] = pd.Series("Zero balance", index=data.index, dtype="object")
    positive_balance = data["Balance"].gt(0)
    segmented.loc[positive_balance & data["Balance"].le(positive_balance_median), "Balance group"] = "Low positive balance"
    segmented.loc[positive_balance & data["Balance"].gt(positive_balance_median), "Balance group"] = "High positive balance"

    segmented["Product count"] = segmented["NumOfProducts"].map(lambda value: f"{value} product{'s' if value != 1 else ''}")
    segmented["Activity"] = segmented["IsActiveMember"].map({1: "Active", 0: "Inactive"})

    notes = {
        "Age group": "Age bands use the project cutoffs: under 30, 30–45, 46–59, and 60+.",
        "Credit score": f"Relative bands based on this dataset’s tertiles: Low ≤ {credit_low}; Medium {credit_low + 1}–{credit_high}; High > {credit_high}. These are descriptive groupings, not lending thresholds.",
        "Tenure group": "New = 0–2 years; Mid-term = 3–6 years; Long-term = 7 or more years.",
        "Balance group": f"Zero balance = 0; positive balances split at the dataset median of {positive_balance_median:,.2f} (lower band includes the median). Units are as recorded in the source.",
        "Product count": "Segments show the number of products recorded for each customer.",
        "Activity": "Active and inactive labels come from IsActiveMember (1 = active, 0 = inactive).",
    }
    return segmented, notes


def summarize_segment_churn(data: pd.DataFrame, dimension: str) -> pd.DataFrame:
    summary = summarize_churn(data, dimension).rename(
        columns={dimension: "Segment", "Churn_Rate": "Churn rate"}
    )
    total_churned = int(data["Exited"].sum())
    summary["Churn contribution"] = (
        summary["Churned"] / total_churned if total_churned else 0
    )
    return summary


try:
    customer_data = load_customer_data(str(DATA_FILE))
    data_error = None
except FileNotFoundError:
    customer_data = None
    data_error = f"Could not find {DATA_FILE.name} beside app.py."
except (
    OSError,
    UnicodeDecodeError,
    pd.errors.EmptyDataError,
    pd.errors.ParserError,
    DataValidationError,
) as error:
    customer_data = None
    data_error = f"Could not use {DATA_FILE.name}: {error}"

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
    sidebar_status = "Dataset validated" if customer_data is not None else "Dataset unavailable"
    sidebar_status_color = GREEN if customer_data is not None else "#f6b94a"
    st.markdown(
        f'<span class="status"><span class="status-dot" style="background:{sidebar_status_color}"></span>{sidebar_status}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("\n")
    st.caption("Customer Segmentation & Churn Pattern Analytics")

if section == "Geography & demographics":
    st.markdown('<div class="eyebrow">Customer analysis · geography & demographics</div>', unsafe_allow_html=True)
    st.title("Geography & demographics")
    st.markdown('<div class="subtle">Compare observed churn across countries, age groups, and gender.</div>', unsafe_allow_html=True)
    if customer_data is None:
        st.error(data_error, icon="⚠️")
        st.stop()

    analysis_data = customer_data.copy()
    analysis_data["Age group"] = pd.cut(
        analysis_data["Age"],
        bins=[-float("inf"), 29, 45, 59, float("inf")],
        labels=["Under 30", "30–45", "46–59", "60+"],
    )
    country_summary = summarize_churn(analysis_data, "Geography").sort_values("Churn_Rate", ascending=False)
    age_summary = summarize_churn(analysis_data, "Age group")
    gender_summary = summarize_churn(analysis_data, "Gender").sort_values("Churn_Rate", ascending=False)
    country_age = analysis_data.pivot_table(
        index="Age group", columns="Geography", values="Exited", aggfunc="mean", observed=False
    )

    highest_country = country_summary.iloc[0]
    highest_age = age_summary.loc[age_summary["Churn_Rate"].idxmax()]
    highest_gender = gender_summary.iloc[0]
    summary_cols = st.columns(3)
    for col, (label, value, detail, accent) in zip(
        summary_cols,
        [
            ("HIGHEST COUNTRY RATE", f"{highest_country['Churn_Rate']:.1%}", f"{highest_country['Geography']} · {int(highest_country['Customers']):,} customers", ROSE),
            ("HIGHEST AGE-GROUP RATE", f"{highest_age['Churn_Rate']:.1%}", f"{highest_age['Age group']} · {int(highest_age['Customers']):,} customers", BLUE),
            ("GENDER WITH HIGHER RATE", f"{highest_gender['Churn_Rate']:.1%}", f"{highest_gender['Gender']} · {int(highest_gender['Customers']):,} customers", GREEN),
        ],
    ):
        with col:
            st.markdown(
                f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{accent}">{value}</div><div class="kpi-note">{detail}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("\n")
    left, right = st.columns(2)
    with left:
        st.subheader("Churn by country")
        st.caption("Rate bars include customer and churned counts on hover.")
        fig = px.bar(
            country_summary.sort_values("Geography"), x="Geography", y="Churn_Rate",
            color="Churn_Rate", color_continuous_scale=["#70a5ff", "#ff7185"],
            custom_data=["Customers", "Churned"], labels={"Churn_Rate": "Churn rate", "Geography": "Country"},
        )
        fig.update_traces(hovertemplate="%{x}<br>Churn rate: %{y:.1%}<br>Customers: %{customdata[0]:,}<br>Churned: %{customdata[1]:,}<extra></extra>")
        style_chart(fig).update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.dataframe(
            country_summary.rename(columns={"Geography": "Country", "Churn_Rate": "Churn rate"})
            .assign(**{"Churn rate": lambda table: table["Churn rate"].map(lambda rate: f"{rate:.1%}")})
            [["Country", "Customers", "Churned", "Churn rate"]],
            hide_index=True, use_container_width=True,
        )
    with right:
        st.subheader("Churn by age group")
        st.caption("Age bands follow the project definitions: under 30, 30–45, 46–59, and 60+.")
        fig = px.bar(
            age_summary, x="Age group", y="Churn_Rate", color="Churn_Rate",
            color_continuous_scale=["#70a5ff", "#ff7185"], custom_data=["Customers", "Churned"],
            labels={"Churn_Rate": "Churn rate", "Age group": "Age group"},
        )
        fig.update_traces(hovertemplate="%{x}<br>Churn rate: %{y:.1%}<br>Customers: %{customdata[0]:,}<br>Churned: %{customdata[1]:,}<extra></extra>")
        style_chart(fig).update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.dataframe(
            age_summary.rename(columns={"Churn_Rate": "Churn rate"})
            .assign(**{"Churn rate": lambda table: table["Churn rate"].map(lambda rate: f"{rate:.1%}")})
            [["Age group", "Customers", "Churned", "Churn rate"]],
            hide_index=True, use_container_width=True,
        )

    st.markdown("\n")
    left, right = st.columns(2)
    with left:
        st.subheader("Churn by gender")
        fig = px.bar(
            gender_summary, x="Gender", y="Churn_Rate", color="Churn_Rate",
            color_continuous_scale=["#70a5ff", "#ff7185"], custom_data=["Customers", "Churned"],
            labels={"Churn_Rate": "Churn rate", "Gender": "Gender"},
        )
        fig.update_traces(hovertemplate="%{x}<br>Churn rate: %{y:.1%}<br>Customers: %{customdata[0]:,}<br>Churned: %{customdata[1]:,}<extra></extra>")
        style_chart(fig).update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.dataframe(
            gender_summary.rename(columns={"Churn_Rate": "Churn rate"})
            .assign(**{"Churn rate": lambda table: table["Churn rate"].map(lambda rate: f"{rate:.1%}")})
            [["Gender", "Customers", "Churned", "Churn rate"]],
            hide_index=True, use_container_width=True,
        )
    with right:
        st.subheader("Country × age-group churn")
        st.caption("Each cell shows the churn rate for customers in that country and age band.")
        fig = px.imshow(
            country_age * 100, text_auto=".1f", aspect="auto",
            color_continuous_scale=["#152749", "#70a5ff", "#ff7185"],
            labels={"x": "Country", "y": "Age group", "color": "Churn rate (%)"},
        )
        fig.update_traces(hovertemplate="Age group: %{y}<br>Country: %{x}<br>Churn rate: %{z:.1f}%<extra></extra>")
        fig.update_layout(coloraxis_colorbar={"ticksuffix": "%"})
        style_chart(fig, height=380)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.caption("Rates are churned customers divided by customers in each group. These are descriptive comparisons and do not establish causation.")
    st.stop()

if section == "Customer segments":
    st.markdown('<div class="eyebrow">Customer analysis · segmentation</div>', unsafe_allow_html=True)
    st.title("Customer segments")
    st.markdown('<div class="subtle">Compare churn rates and churn contribution across six customer-profile dimensions.</div>', unsafe_allow_html=True)
    if customer_data is None:
        st.error(data_error, icon="⚠️")
        st.stop()

    segmented_data, segment_notes = build_segmented_data(customer_data)
    st.caption("Churn contribution means a segment’s share of all churned customers. It is affected by both segment size and churn rate.")
    segment_dimensions = [
        ("Age", "Age group"),
        ("Credit score", "Credit score"),
        ("Tenure", "Tenure group"),
        ("Balance", "Balance group"),
        ("Products", "Product count"),
        ("Engagement", "Activity"),
    ]
    segment_tabs = st.tabs([label for label, _ in segment_dimensions])
    for tab, (label, dimension) in zip(segment_tabs, segment_dimensions):
        with tab:
            summary = summarize_segment_churn(segmented_data, dimension)
            st.caption(segment_notes[dimension])
            table_summary = summary.assign(
                **{
                    "Churn rate": summary["Churn rate"].map(lambda rate: f"{rate:.1%}"),
                    "Churn contribution": summary["Churn contribution"].map(lambda share: f"{share:.1%}"),
                }
            )
            st.dataframe(
                table_summary[["Segment", "Customers", "Churned", "Churn rate", "Churn contribution"]],
                hide_index=True,
                use_container_width=True,
            )
            figure = px.bar(
                summary,
                x="Segment",
                y="Churn rate",
                color="Churn rate",
                color_continuous_scale=["#70a5ff", "#ff7185"],
                custom_data=["Customers", "Churned", "Churn contribution"],
                labels={"Segment": label, "Churn rate": "Churn rate"},
            )
            figure.update_traces(
                hovertemplate=(
                    "%{x}<br>Churn rate: %{y:.1%}<br>Customers: %{customdata[0]:,}"
                    "<br>Churned: %{customdata[1]:,}<br>Share of all churn: %{customdata[2]:.1%}<extra></extra>"
                )
            )
            style_chart(figure).update_layout(coloraxis_showscale=False)
            st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})
    st.caption("Segment totals are descriptive of this dataset and do not establish that a profile causes churn.")
    st.stop()

if section != "Overview":
    upcoming = {
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
    if customer_data is not None:
        st.markdown(
            f'<div style="text-align:right"><span class="status"><span class="status-dot" style="background:{GREEN}"></span>Source validated · {len(customer_data):,} customers</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="text-align:right"><span class="status"><span class="status-dot" style="background:#f6b94a"></span>Dataset unavailable</span></div>',
            unsafe_allow_html=True,
        )

st.markdown("\n")
if customer_data is None:
    st.error(data_error, icon="⚠️")
else:
    st.caption(f"Source: {DATA_FILE.name} · one row per unique customer · filters and charts arrive in later milestones.")

st.markdown('<div class="eyebrow">Filters · later milestone</div>', unsafe_allow_html=True)
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
    ("TOTAL CUSTOMERS", "—", "Unavailable until the data validates", BLUE),
    ("OVERALL CHURN RATE", "—", "Unavailable until the data validates", ROSE),
    ("CHURNED CUSTOMERS", "—", "Unavailable until the data validates", ROSE),
    ("RETAINED CUSTOMERS", "—", "Unavailable until the data validates", GREEN),
]
if customer_data is not None:
    total_customers = len(customer_data)
    churned_customers = int(customer_data["Exited"].eq(1).sum())
    retained_customers = total_customers - churned_customers
    churn_rate = churned_customers / total_customers
    metrics = [
        ("TOTAL CUSTOMERS", f"{total_customers:,}", "Unique customer records", BLUE),
        ("OVERALL CHURN RATE", f"{churn_rate:.1%}", "Churned ÷ total customers", ROSE),
        ("CHURNED CUSTOMERS", f"{churned_customers:,}", "Exited = 1", ROSE),
        ("RETAINED CUSTOMERS", f"{retained_customers:,}", "Exited = 0", GREEN),
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
    st.markdown('<div class="panel"><div class="panel-title">Churn by geography</div><div class="panel-copy">Compare customer exit rates across France, Germany, and Spain.</div><div class="empty"><div class="empty-icon">▥</div><strong>Analysis planned for a later milestone</strong><span>The dataset is loaded; geography breakdowns are not part of this phase.</span></div></div>', unsafe_allow_html=True)
with chart_right:
    st.markdown('<div class="panel"><div class="panel-title">Customer status mix</div><div class="panel-copy">Retained and churned customers across the selected population.</div><div class="empty"><div class="empty-icon">◉</div><strong>Analysis planned for a later milestone</strong><span>The headline status counts above are live; the chart comes later.</span></div></div>', unsafe_allow_html=True)

st.markdown("\n")
st.markdown('<div class="panel"><div class="panel-title">Segment snapshot</div><div class="panel-copy">A preview of the segment comparison table.</div><div class="table-placeholder">Segment comparisons are planned for a later milestone.</div></div>', unsafe_allow_html=True)

st.markdown("\n")
st.caption("Customer counts and churn rate use the validated source labels; filters and breakdowns are not active yet.")
