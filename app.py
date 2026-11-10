import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Malaysia Data Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 2. THEME / CUSTOM CSS
# =========================================================
BLUE = "#245A9A"
DARK_BLUE = "#173B70"
TEAL = "#18A999"
LIGHT_BLUE = "#A8D5F5"
ORANGE = "#F2A65A"

st.markdown(
    """
    <style>
    .stApp { background: #F4F7FC; }
    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }
    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* Refined sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F7FAFF 100%);
        border-right: 1px solid #DCE6F2;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1.6rem;
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }
    .sidebar-heading {
        color: #173B70;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.3px;
        margin: 0 0 4px 0;
    }
    .sidebar-intro {
        color: #718096;
        font-size: 13px;
        line-height: 1.55;
        margin: 0 0 8px 0;
    }
    .sidebar-label {
        color: #294B75;
        font-size: 13px;
        font-weight: 700;
        margin: 8px 0 2px 0;
    }
    .sidebar-guide {
        background: #FFFFFF;
        border: 1px solid #E3EAF4;
        border-radius: 12px;
        padding: 12px 13px;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(23, 59, 112, 0.035);
    }
    .sidebar-guide-item {
        color: #52657D;
        font-size: 12px;
        line-height: 1.45;
        padding: 7px 0;
        border-bottom: 1px solid #EEF2F7;
    }
    .sidebar-guide-item:last-child {
        border-bottom: none;
        padding-bottom: 1px;
    }
    .sidebar-guide-number {
        display: inline-block;
        color: #245A9A;
        background: #EAF2FF;
        font-size: 10px;
        font-weight: 800;
        border-radius: 6px;
        padding: 3px 6px;
        margin-right: 7px;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        border: 1px solid #D5E0EE;
        border-radius: 11px;
        background: #FFFFFF;
        min-height: 44px;
        box-shadow: 0 2px 6px rgba(23, 59, 112, 0.035);
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
        border-color: #4C83C3;
        box-shadow: 0 0 0 3px rgba(76, 131, 195, 0.13);
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #E8F1FF !important;
        border: 1px solid #C9DCF7 !important;
        border-radius: 7px !important;
        color: #214F86 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #214F86 !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"] {
        border: 1px solid #D6E2F0;
        border-radius: 9px;
        color: #245A9A;
        background: #FFFFFF;
        font-size: 12px;
        font-weight: 650;
        min-height: 34px;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        border-color: #8FB3DF;
        background: #F0F6FF;
        color: #173B70;
    }
    .sidebar-footer {
        color: #8A98AA;
        font-size: 11px;
        line-height: 1.5;
        padding-top: 5px;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #173B70;
    }
    /* Premium sidebar polish */
    .sidebar-count {
        background: linear-gradient(110deg, #EAF2FF 0%, #E8F8F6 100%);
        border: 1px solid #D5E5F2;
        border-radius: 10px;
        padding: 10px 12px;
        color: #245A9A;
        font-size: 12px;
        font-weight: 750;
        text-align: center;
        margin-top: 7px;
        margin-bottom: 8px;
    }
    .sidebar-section-label {
        color: #294B75;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 9px 0 5px 0;
    }
    .sidebar-guide {
        background: #FFFFFF;
        border: 1px solid #DCE6F2;
        border-radius: 14px;
        padding: 12px 13px;
        margin: 5px 0;
        box-shadow: 0 4px 12px rgba(23, 59, 112, 0.055);
    }
    .sidebar-guide-item {
        color: #52657D;
        font-size: 12px;
        line-height: 1.5;
        padding: 9px 0;
        border-bottom: 1px solid #EEF2F7;
    }
    .sidebar-guide-item:last-child {
        border-bottom: none;
        padding-bottom: 2px;
    }
    .sidebar-guide-number {
        display: inline-block;
        min-width: 25px;
        text-align: center;
        color: #245A9A;
        background: #EAF2FF;
        font-size: 10px;
        font-weight: 800;
        border-radius: 7px;
        padding: 4px 6px;
        margin-right: 7px;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #EAF2FF !important;
        border: 1px solid #C9DCF7 !important;
        border-radius: 8px !important;
        color: #214F86 !important;
        font-weight: 650 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #214F86 !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"] {
        min-height: 38px;
        border: 1px solid #D6E2F0;
        border-radius: 10px;
        color: #245A9A;
        background: #FFFFFF;
        font-size: 12px;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        border-color: #8FB3DF;
        background: #F0F6FF;
        color: #173B70;
        transform: translateY(-1px);
    }
    .sidebar-footer {
        color: #8A98AA;
        font-size: 10px;
        line-height: 1.6;
        letter-spacing: 0.35px;
        padding-top: 4px;
    }

    .dashboard-hero {
        background: linear-gradient(120deg, #173B70 0%, #245A9A 65%, #18A999 100%);
        padding: 28px 32px;
        border-radius: 18px;
        margin-bottom: 22px;
        box-shadow: 0 8px 22px rgba(23, 59, 112, 0.12);
    }
    .hero-eyebrow {
        color: #DCEAFE;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .hero-title {
        color: #FFFFFF;
        font-size: 34px;
        line-height: 1.2;
        font-weight: 800;
        margin: 0;
    }
    .hero-subtitle {
        color: #E6F0FF;
        font-size: 15px;
        margin-top: 10px;
        margin-bottom: 0;
    }
    .section-title {
        color: #173B70;
        font-size: 24px;
        font-weight: 800;
        margin: 4px 0 4px 0;
    }
    .section-description {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 14px;
    }
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(23, 59, 112, 0.045);
    }
    div[data-testid="stMetricLabel"] {
        color: #64748B;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: #173B70;
        font-weight: 800;
    }
    div[data-testid="stAlert"] { border-radius: 12px; }
    div[data-baseweb="select"] { border-radius: 10px; }
    hr { border-color: #DCE4F0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 3. DATA LOADING
# Keep these three CSV files in the same folder as app.py:
# birth_income_merged.csv
# school_income_merged.csv
# birth_school_merged.csv
# =========================================================
BASE_DIR = Path(__file__).parent

@st.cache_data

def load_data(filename):
    file_path = BASE_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    return pd.read_csv(file_path)

try:
    df_birth_income = load_data("birth_income_merged.csv")
    df_school_income = load_data("school_income_merged.csv")
    df_birth_school = load_data("birth_school_merged.csv")
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.info("Make sure all three CSV files are uploaded to the same GitHub repository folder as app.py.")
    st.stop()

# =========================================================
# 4. DATA CLEANING
# =========================================================
required_columns = {
    "birth_income": {"state", "year", "abs", "rate", "income_mean"},
    "school_income": {"state", "year", "completion", "income_mean"},
    "birth_school": {"state", "year", "abs", "completion"},
}

for dataset_name, dataframe in [
    ("birth_income", df_birth_income),
    ("school_income", df_school_income),
    ("birth_school", df_birth_school),
]:
    missing = required_columns[dataset_name] - set(dataframe.columns)
    if missing:
        st.error(
            f"The {dataset_name} dataset is missing these columns: "
            f"{', '.join(sorted(missing))}. Please check the CSV column names."
        )
        st.stop()


def clean_dataset(dataframe):
    data = dataframe.copy()
    data["state"] = data["state"].astype(str).str.strip()
    data["year"] = pd.to_numeric(data["year"], errors="coerce")

    numeric_columns = [
        "abs", "rate", "completion", "income_mean", "income_median"
    ]
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(subset=["state"])
    data = data[~data["state"].str.lower().isin(["nan", "malaysia", ""])]
    return data


df_birth_income = clean_dataset(df_birth_income)
df_school_income = clean_dataset(df_school_income)
df_birth_school = clean_dataset(df_birth_school)

# =========================================================
# 5. SHARED HELPER FUNCTIONS
# =========================================================
def year_filter(dataframe, label, key):
    available_years = sorted(
        dataframe["year"].dropna().astype(int).unique().tolist()
    )
    options = ["All Years"] + available_years
    selected_year = st.selectbox(label, options, key=key)

    if selected_year == "All Years":
        return dataframe.copy()
    return dataframe[dataframe["year"] == selected_year].copy()


def correlation_strength(value):
    if pd.isna(value):
        return "Not available"
    absolute_value = abs(value)
    if absolute_value < 0.30:
        return "Weak"
    if absolute_value < 0.70:
        return "Moderate"
    return "Strong"


def style_figure(fig, height=520):
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(family="Arial", size=12, color="#334155"),
        title=dict(font=dict(size=19, color=DARK_BLUE)),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=35, r=30, t=75, b=45),
        legend_title_font=dict(color=DARK_BLUE),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E8EEF6", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E8EEF6", zeroline=False)
    return fig


def show_map(dataframe, value_column, title, color_label):
    state_coordinates = {
        "Johor": (1.85, 103.20),
        "Kedah": (6.12, 100.37),
        "Kelantan": (5.33, 102.00),
        "Melaka": (2.19, 102.25),
        "Negeri Sembilan": (2.72, 101.94),
        "Pahang": (3.75, 102.40),
        "Perak": (4.75, 100.90),
        "Perlis": (6.45, 100.20),
        "Pulau Pinang": (5.41, 100.33),
        "Penang": (5.41, 100.33),
        "Sabah": (5.98, 116.07),
        "Sarawak": (1.55, 110.35),
        "Selangor": (3.20, 101.50),
        "Terengganu": (5.31, 103.13),
        "W.P. Kuala Lumpur": (3.14, 101.69),
        "Kuala Lumpur": (3.14, 101.69),
        "W.P. Labuan": (5.28, 115.24),
        "Labuan": (5.28, 115.24),
        "W.P. Putrajaya": (2.93, 101.69),
        "Putrajaya": (2.93, 101.69),
    }

    map_data = dataframe.copy()
    map_data["latitude"] = map_data["state"].map(
        lambda state: state_coordinates.get(state, (np.nan, np.nan))[0]
    )
    map_data["longitude"] = map_data["state"].map(
        lambda state: state_coordinates.get(state, (np.nan, np.nan))[1]
    )
    map_data = map_data.dropna(
        subset=["latitude", "longitude", value_column]
    )

    if map_data.empty:
        st.warning("No recognised Malaysian state data is available for this map.")
        return

    fig = px.scatter_geo(
        map_data,
        lat="latitude",
        lon="longitude",
        size=value_column,
        color=value_column,
        hover_name="state",
        hover_data={
            value_column: ":,.2f",
            "latitude": False,
            "longitude": False,
        },
        scope="asia",
        title=title,
        color_continuous_scale="Tealgrn",
        size_max=34,
        labels={value_column: color_label},
        projection="mercator",
    )
    fig.update_traces(
        marker=dict(
            opacity=0.88,
            line=dict(width=1.5, color="white"),
        )
    )
    fig.update_geos(
        center=dict(lat=4.5, lon=109),
        projection_scale=1.35,
        lataxis_range=[0, 8],
        lonaxis_range=[99, 120],
        showland=True,
        landcolor="#F0F3F7",
        showocean=True,
        oceancolor="#E8F3FA",
        showcountries=True,
        countrycolor="#B8C5D1",
        showcoastlines=True,
        coastlinecolor="#B8C5D1",
        resolution=50,
    )
    fig.update_layout(
        template="plotly_white",
        height=650,
        paper_bgcolor="#FFFFFF",
        margin=dict(l=10, r=25, t=70, b=15),
        font=dict(family="Arial", size=12, color="#334155"),
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 6. SIDEBAR FILTERS
# =========================================================
all_states = sorted(
    set(df_birth_income["state"].dropna())
    | set(df_school_income["state"].dropna())
    | set(df_birth_school["state"].dropna())
)

# Keep the state filter selection when the user clicks the quick-action buttons.
if "state_filter" not in st.session_state:
    st.session_state["state_filter"] = all_states.copy()

with st.sidebar:
    # Sidebar heading and short description
    st.markdown(
        """
        <div class="sidebar-heading">📊 Dashboard Filters</div>
        <p class="sidebar-intro">
            Personalise your dashboard by selecting Malaysian states
            to include in your analysis.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section-label">STATE SELECTION</div>',
        unsafe_allow_html=True,
    )

    # Quick actions: select all states or clear the selection
    select_col, clear_col = st.columns(2)
    with select_col:
        if st.button(
            "✓ Select All",
            use_container_width=True,
            key="select_all_states",
        ):
            st.session_state["state_filter"] = all_states.copy()

    with clear_col:
        if st.button(
            "✕ Clear",
            use_container_width=True,
            key="clear_states",
        ):
            st.session_state["state_filter"] = []

    # Multi-state selector
    selected_states = st.multiselect(
        "Choose Malaysian states",
        options=all_states,
        key="state_filter",
        placeholder="Search or select states...",
        help=(
            "Select one or multiple Malaysian states. "
            "Use Select All or Clear for quick selection."
        ),
    )

    # Selected-state counter
    st.markdown(
        f"""
        <div class="sidebar-count">
            ✓ {len(selected_states)} / {len(all_states)} States Selected
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Guide to the three visualisation objectives
    st.markdown(
        '<div class="sidebar-section-label">VISUALISATION GUIDE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="sidebar-guide">
            <div class="sidebar-guide-item">
                <span class="sidebar-guide-number">01</span>
                Births vs Household Income
            </div>
            <div class="sidebar-guide-item">
                <span class="sidebar-guide-number">02</span>
                School Completion vs Household Income
            </div>
            <div class="sidebar-guide-item">
                <span class="sidebar-guide-number">03</span>
                Births vs School Completion
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        """
        <div class="sidebar-footer">
            SCIENTIFIC VISUALISATION ASSIGNMENT<br>
            JIE42403 · MALAYSIA
        </div>
        """,
        unsafe_allow_html=True,
    )

if not selected_states:
    st.warning("Please select at least one state from the sidebar to display the dashboard.")
    st.stop()

birth_income = df_birth_income[
    df_birth_income["state"].isin(selected_states)
].copy()
school_income = df_school_income[
    df_school_income["state"].isin(selected_states)
].copy()
birth_school = df_birth_school[
    df_birth_school["state"].isin(selected_states)
].copy()

# =========================================================
# 7. DASHBOARD HEADER
# =========================================================
st.markdown(
    """
    <div class="dashboard-hero">
        <div class="hero-eyebrow">Scientific Visualisation · Malaysia</div>
        <div class="hero-title">Malaysia Data Visualization Dashboard</div>
        <p class="hero-subtitle">
            An analysis of annual live births, household income and
            primary school completion rates across Malaysian states.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 8. DASHBOARD OVERVIEW / KPI CARDS
# =========================================================
st.markdown('<div class="section-title">Dashboard Overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">A quick summary of the selected state-level datasets.</div>',
    unsafe_allow_html=True,
)

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Number of States", f"{birth_income['state'].nunique():,}")
with kpi2:
    st.metric("Total Annual Live Births", f"{birth_income['abs'].sum():,.0f}")
with kpi3:
    st.metric("Average Household Income", f"RM {birth_income['income_mean'].mean():,.0f}")

st.caption(
    "The dashboard explores patterns and relationships between birth statistics, "
    "household income and primary school completion across Malaysian states."
)
st.divider()

# =========================================================
# 9. OBJECTIVE 1: BIRTHS VS HOUSEHOLD INCOME
# Bubble Chart: x = mean income, y = annual births, size = birth rate
# =========================================================
st.markdown(
    '<div class="section-title">Objective 1: Births vs Household Income</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">To identify the relationship between annual live births and household income across Malaysian states.</div>',
    unsafe_allow_html=True,
)

birth_plot = year_filter(
    birth_income,
    "Select Year - Objective 1",
    "year_obj1",
)
birth_plot = birth_plot.dropna(subset=["income_mean", "abs", "rate"]).copy()

if not birth_plot.empty:
    fig1 = px.scatter(
        birth_plot,
        x="income_mean",
        y="abs",
        size="rate",
        color="state",
        hover_name="state",
        hover_data={
            "year": True,
            "income_mean": ":,.0f",
            "abs": ":,.0f",
            "rate": ":.2f",
        },
        size_max=38,
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="Relationship Between Household Income and Annual Live Births",
        labels={
            "income_mean": "Mean Household Income (MYR)",
            "abs": "Annual Live Births",
            "rate": "Birth Rate",
            "state": "State",
            "year": "Year",
        },
    )
    fig1.update_traces(
        marker=dict(opacity=0.78, line=dict(width=1, color="white"))
    )
    style_figure(fig1, 560)
    st.plotly_chart(fig1, use_container_width=True)
    st.info(
        "Bubble size represents the birth rate. Each colour represents a Malaysian state. "
        "Hover over a bubble to view the state, year, household income and birth information."
    )

    with st.expander("View Objective 1 statistical summary"):
        summary1 = birth_plot[["income_mean", "abs", "rate"]].describe().round(2)
        st.dataframe(summary1, use_container_width=True)
else:
    st.warning("No data available for Objective 1 under the selected filters.")

st.divider()

# =========================================================
# 10. OBJECTIVE 2: SCHOOL COMPLETION VS HOUSEHOLD INCOME
# Scatter Plot + Overall Regression Line
# =========================================================
st.markdown(
    '<div class="section-title">Objective 2: School Completion vs Household Income</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">To examine the relationship between primary school completion rates and household income across Malaysian states.</div>',
    unsafe_allow_html=True,
)

school_plot = year_filter(
    school_income,
    "Select Year - Objective 2",
    "year_obj2",
)
school_plot = school_plot.dropna(subset=["income_mean", "completion"]).copy()

if not school_plot.empty:
    fig2 = px.scatter(
        school_plot,
        x="income_mean",
        y="completion",
        color="state",
        hover_name="state",
        hover_data={
            "year": True,
            "income_mean": ":,.0f",
            "completion": ":.2f",
        },
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="Relationship Between Household Income and Primary School Completion Rate",
        labels={
            "income_mean": "Mean Household Income (MYR)",
            "completion": "Primary School Completion Rate (%)",
            "state": "State",
            "year": "Year",
        },
    )
    fig2.update_traces(
        marker=dict(size=10, opacity=0.82, line=dict(width=1, color="white"))
    )

    # Add one overall linear regression line when there are enough valid points.
    if len(school_plot) >= 2 and school_plot["income_mean"].nunique() >= 2:
        x_values = school_plot["income_mean"].to_numpy(dtype=float)
        y_values = school_plot["completion"].to_numpy(dtype=float)
        slope, intercept = np.polyfit(x_values, y_values, 1)
        x_line = np.linspace(x_values.min(), x_values.max(), 100)
        y_line = slope * x_line + intercept
        fig2.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="Overall Regression Line",
                line=dict(color="#E4572E", width=3),
                hoverinfo="skip",
            )
        )

    style_figure(fig2, 560)
    st.plotly_chart(fig2, use_container_width=True)

    if len(school_plot) >= 2:
        correlation = school_plot["income_mean"].corr(school_plot["completion"])
        metric1, metric2 = st.columns(2)
        with metric1:
            st.metric(
                "Pearson Correlation (r)",
                f"{correlation:.3f}" if pd.notna(correlation) else "Not available",
            )
        with metric2:
            st.metric("Correlation Strength", correlation_strength(correlation))

        if pd.notna(correlation):
            direction = "positive" if correlation > 0 else "negative" if correlation < 0 else "no linear"
            st.info(
                f"The Pearson correlation is {correlation:.3f}, indicating a "
                f"{correlation_strength(correlation).lower()} {direction} association "
                "between mean household income and school completion rate in the selected data. "
                "Correlation does not prove causation."
            )
    else:
        st.info("At least two valid observations are required to calculate correlation and regression.")

    with st.expander("View Objective 2 statistical summary"):
        st.dataframe(
            school_plot[["income_mean", "completion"]].describe().round(2),
            use_container_width=True,
        )
else:
    st.warning("No data available for Objective 2 under the selected filters.")

st.divider()

# =========================================================
# 11. OBJECTIVE 3: BIRTHS VS SCHOOL COMPLETION
# Two-panel horizontal bar chart by Malaysian state
# =========================================================
st.markdown(
    '<div class="section-title">Objective 3: Births vs School Completion</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'To compare annual live births and primary school completion rates '
    'across Malaysian states.'
    '</div>',
    unsafe_allow_html=True,
)

bar_plot = year_filter(
    birth_school,
    "Select Year - Objective 3",
    "year_obj3",
)

bar_plot = bar_plot.dropna(subset=["abs", "completion"]).copy()

if not bar_plot.empty:
    # Summarise the selected year (or all years) into one record per state.
    # Mean is used so that states with more recorded years are not over-counted.
    bar_plot = (
        bar_plot.groupby("state", as_index=False)
        .agg(
            abs=("abs", "mean"),
            completion=("completion", "mean"),
        )
        .sort_values("abs", ascending=True)
    )

    if not bar_plot.empty:
        fig3 = make_subplots(
            rows=1,
            cols=2,
            shared_yaxes=True,
            horizontal_spacing=0.16,
            subplot_titles=(
                "Annual Live Births",
                "Primary School Completion Rate",
            ),
        )

        # Left panel: annual live births
        fig3.add_trace(
            go.Bar(
                x=bar_plot["abs"],
                y=bar_plot["state"],
                orientation="h",
                name="Annual Live Births",
                marker=dict(
                    color=BLUE,
                    line=dict(color="white", width=1),
                ),
                text=bar_plot["abs"].map(lambda value: f"{value:,.0f}"),
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Annual Live Births: %{x:,.0f}"
                    "<extra></extra>"
                ),
            ),
            row=1,
            col=1,
        )

        # Right panel: primary school completion rate
        fig3.add_trace(
            go.Bar(
                x=bar_plot["completion"],
                y=bar_plot["state"],
                orientation="h",
                name="School Completion Rate",
                marker=dict(
                    color=TEAL,
                    line=dict(color="white", width=1),
                ),
                text=bar_plot["completion"].map(lambda value: f"{value:.1f}%"),
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "School Completion Rate: %{x:.2f}%"
                    "<extra></extra>"
                ),
            ),
            row=1,
            col=2,
        )

        fig3.update_xaxes(
            title_text="Number of Live Births",
            showgrid=True,
            gridcolor="#E8EEF6",
            zeroline=False,
            rangemode="tozero",
            row=1,
            col=1,
        )
        fig3.update_xaxes(
            title_text="Completion Rate (%)",
            showgrid=True,
            gridcolor="#E8EEF6",
            zeroline=False,
            rangemode="tozero",
            row=1,
            col=2,
        )
        fig3.update_yaxes(
            title_text="Malaysian State",
            showgrid=False,
            autorange="reversed",
            row=1,
            col=1,
        )
        fig3.update_yaxes(
            showticklabels=False,
            showgrid=False,
            row=1,
            col=2,
        )

        chart_height = max(560, 34 * len(bar_plot) + 170)
        fig3.update_layout(
            template="plotly_white",
            title=dict(
                text="Annual Live Births and School Completion by State",
                x=0.02,
                xanchor="left",
                font=dict(size=20, color=DARK_BLUE),
            ),
            height=chart_height,
            autosize=True,
            showlegend=False,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Arial", size=12, color="#334155"),
            margin=dict(l=110, r=75, t=105, b=75),
            bargap=0.28,
            hoverlabel=dict(bgcolor="white", font_size=12),
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.info(
            "The left bar chart compares the average annual live births for each "
            "state, while the right bar chart compares the average primary school "
            "completion rate. The two measures use separate horizontal scales "
            "because they have different units."
        )

        with st.expander("View Objective 3 state-level data"):
            display_bar = bar_plot[
                ["state", "abs", "completion"]
            ].rename(
                columns={
                    "state": "State",
                    "abs": "Average Annual Live Births",
                    "completion": "Average School Completion Rate (%)",
                }
            )
            display_bar["Average Annual Live Births"] = (
                display_bar["Average Annual Live Births"].round(0).astype(int)
            )
            display_bar["Average School Completion Rate (%)"] = (
                display_bar["Average School Completion Rate (%)"].round(2)
            )
            st.dataframe(
                display_bar.sort_values(
                    "Average Annual Live Births", ascending=False
                ),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.warning("No data available for Objective 3 under the selected filters.")
else:
    st.warning("No data available for Objective 3 under the selected filters.")

# =========================================================
# 12. FOOTER
# =========================================================
st.divider()
st.markdown(
    "<div style='text-align:center; color:#718096; font-size:12px;'>"
    "Malaysia Data Visualization Dashboard · Scientific Visualisation Assignment · JIE42403"
    "</div>",
    unsafe_allow_html=True,
)
