
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Malaysia Data Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F5F7FB;
}
.main-title {
    color: #183B70;
    font-size: 32px;
    font-weight: 800;
}
.subtitle {
    color: #64748B;
    font-size: 15px;
}
.section-title {
    color: #183B70;
    font-size: 23px;
    font-weight: 700;
}
div[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOAD DATASETS
# ==========================================

BASE_DIR = Path(__file__).parent

@st.cache_data
def load_data(filename):
    return pd.read_csv(BASE_DIR / filename)

try:
    df_birth_income = load_data("birth_income_merged.csv")
    df_school_income = load_data("school_income_merged.csv")
    df_birth_school = load_data("birth_school_merged.csv")

except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

# Clean column values
datasets = [df_birth_income, df_school_income, df_birth_school]

for df in datasets:
    df["state"] = df["state"].astype(str).str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    for col in ["abs", "rate", "completion",
                "income_mean", "income_median"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================
# 4. DASHBOARD HEADER
# ==========================================

st.markdown(
    '<div class="main-title">Malaysia Data Visualization Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">An Analysis of Annual Live Births, '
    'Household Income and Primary School Completion Rates '
    'Across Malaysian States</div>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# 5. SIDEBAR FILTER
# ==========================================

st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("Select states to explore the data.")

all_states = sorted(
    set(df_birth_income["state"].dropna()) |
    set(df_school_income["state"].dropna()) |
    set(df_birth_school["state"].dropna())
)

selected_states = st.sidebar.multiselect(
    "Select State",
    options=all_states,
    default=all_states
)

if not selected_states:
    st.warning("Please select at least one state.")
    st.stop()

# Apply state filter
birth_income = df_birth_income[
    df_birth_income["state"].isin(selected_states)
].copy()

school_income = df_school_income[
    df_school_income["state"].isin(selected_states)
].copy()

birth_school = df_birth_school[
    df_birth_school["state"].isin(selected_states)
].copy()

# Individual year filters
def year_filter(df, label, key):
    years = sorted(df["year"].dropna().astype(int).unique())

    options = ["All Years"] + years

    selected_year = st.selectbox(
        label,
        options=options,
        key=key
    )

    if selected_year != "All Years":
        return df[df["year"] == selected_year].copy()

    return df.copy()

# ==========================================
# 6. DASHBOARD OVERVIEW
# ==========================================

st.markdown(
    '<div class="section-title">Dashboard Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Number of States",
        birth_income["state"].nunique()
    )

with col2:
    st.metric(
        "Total Annual Live Births",
        f"{birth_income['abs'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Average Household Income",
        f"RM {birth_income['income_mean'].mean():,.0f}"
    )

st.caption(
    "The dashboard explores relationships between "
    "birth statistics, household income and school completion "
    "across Malaysian states."
)

st.divider()

# ==========================================
# 7. OBJECTIVE 1
# Births vs Household Income
# Bubble Chart
# ==========================================

st.markdown(
    '<div class="section-title">Objective 1: '
    'Births vs Household Income</div>',
    unsafe_allow_html=True
)

st.write(
    "To identify the relationship between annual live births "
    "and household income across Malaysian states."
)

birth_plot = year_filter(
    birth_income,
    "Select Year - Objective 1",
    "year_obj1"
)

birth_plot = birth_plot.dropna(
    subset=["income_mean", "abs", "rate"]
)

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
            "rate": ":.2f"
        },
        size_max=40,
        title="Relationship Between Household Income "
              "and Annual Live Births",
        labels={
            "income_mean": "Mean Household Income (MYR)",
            "abs": "Annual Live Births",
            "rate": "Birth Rate",
            "state": "State"
        }
    )

    fig1.update_layout(
        template="plotly_white",
        height=550,
        legend_title="States"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.info(
        "Bubble size represents birth rate. "
        "Each colour represents a Malaysian state."
    )

    st.markdown("**Statistical Summary**")

    st.dataframe(
        birth_plot[
            ["state", "year", "income_mean", "abs", "rate"]
        ].describe().round(2),
        use_container_width=True
    )

else:
    st.warning("No data available for Objective 1.")

st.divider()

# ==========================================
# 8. OBJECTIVE 2
# School Completion vs Household Income
# Scatter Plot + Regression Line
# ==========================================

st.markdown(
    '<div class="section-title">Objective 2: '
    'School Completion vs Household Income</div>',
    unsafe_allow_html=True
)

st.write(
    "To examine the relationship between primary school "
    "completion rates and household income across Malaysian states."
)

school_plot = year_filter(
    school_income,
    "Select Year - Objective 2",
    "year_obj2"
)

school_plot = school_plot.dropna(
    subset=["income_mean", "completion"]
)

if not school_plot.empty:

    fig2 = px.scatter(
        school_plot,
        x="income_mean",
        y="completion",
        color="state",
        hover_name="state",
        hover_data=["year"],
        title="Relationship Between Household Income "
              "and Primary School Completion Rate",
        labels={
            "income_mean": "Mean Household Income (MYR)",
            "completion": "Primary School Completion Rate (%)",
            "state": "State"
        }
    )

    # Overall regression line
    if (
        len(school_plot) >= 2
        and school_plot["income_mean"].nunique() >= 2
    ):
        x = school_plot["income_mean"].to_numpy()
        y = school_plot["completion"].to_numpy()

        slope, intercept = np.polyfit(x, y, 1)

        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept

        fig2.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="Overall Regression Line",
                line=dict(color="red", width=3)
            )
        )

    fig2.update_layout(
        template="plotly_white",
        height=550,
        legend_title="States"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Correlation
    if len(school_plot) >= 2:
        correlation = school_plot[
            ["income_mean", "completion"]
        ].corr().iloc[0, 1]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Pearson Correlation",
                f"{correlation:.3f}"
            )

        with col2:
            if pd.isna(correlation):
                strength = "Not available"
            elif abs(correlation) < 0.3:
                strength = "Weak"
            elif abs(correlation) < 0.7:
                strength = "Moderate"
            else:
                strength = "Strong"

            st.metric(
                "Correlation Strength",
                strength
            )

    st.info(
        "The red line represents the overall linear regression trend. "
        "Correlation measures the strength and direction of "
        "the linear relationship."
    )

else:
    st.warning("No data available for Objective 2.")

st.divider()

# ==========================================
# 9. OBJECTIVE 3
# Births vs School Completion
# Geographical Bubble Map
# ==========================================

st.markdown(
    '<div class="section-title">Objective 3: '
    'Births vs School Completion</div>',
    unsafe_allow_html=True
)

st.write(
    "To analyse the geographical distribution of annual live births "
    "and primary school completion rates across Malaysian states."
)

map_plot = year_filter(
    birth_school,
    "Select Year - Objective 3",
    "year_obj3"
)

# Approximate geographical coordinates of Malaysian states
coordinates = {
    "Johor": (1.85, 103.20),
    "Kedah": (6.12, 100.37),
    "Kelantan": (5.33, 102.00),
    "Melaka": (2.19, 102.25),
    "Negeri Sembilan": (2.72, 101.94),
    "Pahang": (3.75, 102.40),
    "Perak": (4.75, 100.90),
    "Perlis": (6.45, 100.20),
    "Pulau Pinang": (5.41, 100.33),
    "Sabah": (5.98, 116.07),
    "Sarawak": (1.55, 110.35),
    "Selangor": (3.20, 101.50),
    "Terengganu": (5.31, 103.13),
    "W.P. Kuala Lumpur": (3.14, 101.69),
    "W.P. Labuan": (5.28, 115.24),
    "W.P. Putrajaya": (2.93, 101.69)
}

map_plot = map_plot.dropna(
    subset=["abs", "completion"]
).copy()

map_plot["latitude"] = map_plot["state"].map(
    lambda s: coordinates.get(s, (np.nan, np.nan))[0]
)

map_plot["longitude"] = map_plot["state"].map(
    lambda s: coordinates.get(s, (np.nan, np.nan))[1]
)

map_plot = map_plot.dropna(
    subset=["latitude", "longitude"]
)

if not map_plot.empty:

    fig3 = px.scatter_geo(
        map_plot,
        lat="latitude",
        lon="longitude",
        size="abs",
        color="completion",
        hover_name="state",
        text="state",
        hover_data={
            "abs": ":,.0f",
            "completion": ":.2f",
            "year": True,
            "latitude": False,
            "longitude": False
        },
        size_max=35,
        color_continuous_scale="Viridis",
        projection="mercator",
        title="Malaysia Geographical Bubble Map",
        labels={
            "abs": "Annual Live Births",
            "completion": "School Completion Rate (%)"
        }
    )

    fig3.update_traces(
        textposition="top center",
        textfont=dict(size=9),
        marker=dict(
            opacity=0.8,
            line=dict(width=1, color="white")
        )
    )

    fig3.update_geos(
        center=dict(lat=4.5, lon=109),
        lataxis_range=[0, 8],
        lonaxis_range=[99, 120],
        showland=True,
        landcolor="#F0F0F0",
        showocean=True,
        oceancolor="#E8F3FA",
        showcountries=True,
        countrycolor="#B8C5D1",
        showcoastlines=True,
        coastlinecolor="#B8C5D1",
        resolution=50
    )

    fig3.update_layout(
        template="plotly_white",
        height=650,
        margin=dict(l=10, r=10, t=70, b=10)
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.info(
        "Bubble size represents annual live births. "
        "Bubble colour represents primary school completion rate. "
        "Hover over each bubble to view state-level details."
    )

else:
    st.warning(
        "No geographical data available. "
        "Please check the state names in your dataset."
    )

st.divider()

# ==========================================
# 10. FOOTER
# ==========================================

st.markdown(
    "<center><small>Malaysia Data Visualization Dashboard "
    "| Scientific Visualization Assignment</small></center>",
    unsafe_allow_html=True
)
