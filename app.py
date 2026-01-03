import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import warnings
# Show the `use_column_width` deprecation warning only once (avoid repeated warnings per image)
warnings.filterwarnings("once", message=".*use_column_width.*")

# Page config
st.set_page_config(page_title="Event Impact Model", layout="wide")
st.title("📈 Event Impact Model Dashboard")
st.markdown("""
Market reactions to scheduled macro events (FOMC & CPI) across assets.
Data from 2024–2025 rate cycle.
""")

# Load data
data_file = "event_impact_results.xlsx"
if not os.path.exists(data_file):
    st.error(f"⚠️ {data_file} not found! Run your notebook first and export results using:")
    st.code('all_results.to_excel("event_impact_results.xlsx", index=False)')
    st.stop()

try:
    all_results = pd.read_excel(data_file)
except (ImportError, ModuleNotFoundError) as e:
    st.error("Missing dependency 'openpyxl'. Run `pip install openpyxl` in the environment running Streamlit and restart the app.")
    st.markdown("**Environment diagnostic**")
    st.info(f"Python executable: `{sys.executable}`")
    try:
        import openpyxl
        st.info(f"openpyxl version: {openpyxl.__version__}")
    except Exception as import_e:
        st.info(f"openpyxl import failed: {import_e}")
    st.stop()
except Exception as e:
    st.error(f"Could not read {data_file}: {e}")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")
assets = st.sidebar.multiselect(
    "Select Assets",
    options=sorted(all_results['Asset'].unique()),
    default=sorted(all_results['Asset'].unique())
)

events_list = st.sidebar.multiselect(
    "Select Events",
    options=sorted(all_results['Event'].unique()),
    default=sorted(all_results['Event'].unique())
)

# Filter data
filtered = all_results[
    all_results['Asset'].isin(assets) &
    all_results['Event'].isin(events_list)
]

# Summary table
st.header("📊 Average Reaction by Asset")
summary = filtered.pivot_table(
    index='Asset',
    values=['Immediate Return (30min)', 'Vol Change (%)', 'Max Drawdown (%)', 'Time to Peak (min)'],
    aggfunc='mean'
).round(4)

st.dataframe(summary.style.background_gradient(cmap='RdYlGn', axis=0))

# Bar chart: Speed of pricing
st.header("⏱️ Speed of Information Pricing")
fig_bar = px.bar(
    summary.reset_index(),
    x='Asset',
    y='Time to Peak (min)',
    title="Average Minutes to Peak Reaction",
    color='Time to Peak (min)',
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Detailed metrics
st.header("📈 Detailed Event Metrics")
st.dataframe(filtered.style.format({
    'Immediate Return (30min)': '{:.2%}',
    'Post Return (24h)': '{:.2%}',
    'Vol Change (%)': '{:.1f}%',
    'Max Drawdown (%)': '{:.2f}%',
    'Time to Peak (min)': '{:.0f}'
}))

st.success("🎉 Dashboard loaded successfully! Built from your event impact model.")
st.caption("Fastest pricing = lowest time to peak. Bonds/Forex usually win.")