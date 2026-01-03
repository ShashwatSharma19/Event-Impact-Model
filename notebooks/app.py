import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
import warnings
# Show the `use_column_width` deprecation warning only once (avoid repeated warnings per image)
warnings.filterwarnings("once", message=".*use_column_width.*")

st.set_page_config(page_title="Event Impact Model", layout="wide")
st.title("📈 Event Impact Model Dashboard")
st.markdown("""
Market reactions to FOMC & CPI announcements (2024–2025 rate cycle).
Interactive plots show how assets price macro news.
""")

# Load data
data_file = "event_impact_results.xlsx"
if not os.path.exists(data_file):
    st.error(f"⚠️ {data_file} not found! Run notebook and export: all_results.to_excel('event_impact_results.xlsx')")
    st.stop()

df = pd.read_excel(data_file)

# Sidebar
st.sidebar.header("🔍 Filters")
assets = st.sidebar.multiselect("Assets", sorted(df['Asset'].unique()), default=sorted(df['Asset'].unique()))
events_list = st.sidebar.multiselect("Events", sorted(df['Event'].unique()), default=sorted(df['Event'].unique()))

filtered = df[(df['Asset'].isin(assets)) & (df['Event'].isin(events_list))]

# 1. Summary Table
st.header("📊 Average Reaction by Asset")
summary = filtered.pivot_table(
    index='Asset',
    values=['Immediate Return (30min)', 'Vol Change (%)', 'Max Drawdown (%)', 'Time to Peak (min)'],
    aggfunc='mean'
).round(4)
st.dataframe(summary.style.background_gradient(cmap='RdYlGn'))

# 2. Speed of Pricing Bar Chart
st.header("⏱️ Speed of Pricing: Time to Peak Reaction")
fig_bar = px.bar(
    summary.reset_index(),
    x='Asset',
    y='Time to Peak (min)',
    color='Time to Peak (min)',
    color_continuous_scale="Viridis",
    title="Average Minutes to Peak Reaction After Announcement"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 3. Simulated Average Price Path Overlay (Classic Event Study Style)
st.header("📈 Average Normalized Price Reaction Across Events")
# Simulate smooth paths using metrics (approximate)
minutes = np.arange(-60, 180, 5)  # -1h pre to +3h post
avg_paths = {}

for asset in summary.index:
    # Approximate path: gradual pre, jump at t=0, peak at time_to_peak, then fade
    time_to_peak = summary.loc[asset, 'Time to Peak (min)']
    imm_return = summary.loc[asset, 'Immediate Return (30min)']
    
    path = np.ones(len(minutes))
    # Pre-event drift
    path[minutes < 0] = 1 + np.linspace(-0.001, 0, sum(minutes < 0))
    # Immediate reaction
    path[minutes >= 0] = 1 + imm_return * (1 - np.exp(-minutes[minutes >= 0] / 30))
    # Peak and fade
    peak_effect = imm_return * 1.2
    path += peak_effect * np.exp(-np.abs(minutes - time_to_peak) / 40)
    
    avg_paths[asset] = path

path_df = pd.DataFrame(avg_paths, index=minutes)
path_df = path_df.reset_index().melt(id_vars='index', var_name='Asset', value_name='Normalized Price')
path_df.rename(columns={'index': 'Minutes from Announcement'}, inplace=True)

fig_path = px.line(
    path_df,
    x='Minutes from Announcement',
    y='Normalized Price',
    color='Asset',
    title="Simulated Average Price Path Around Announcements"
)
fig_path.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Announcement")
fig_path.update_layout(yaxis_tickformat='.1%')
st.plotly_chart(fig_path, use_container_width=True)

# 4. Detailed Metrics Table
st.header("📋 Detailed Results")
st.dataframe(filtered.style.format({
    'Immediate Return (30min)': '{:.2%}',
    'Post Return (24h)': '{:.2%}',
    'Vol Change (%)': '{:.1f}%',
    'Max Drawdown (%)': '{:.2f}%',
    'Time to Peak (min)': '{:.0f}'
}))

st.success("Dashboard enhanced with price path simulation! Bonds/Forex typically react fastest.")
st.caption("Note: Price paths are approximated from metrics for visualization.")