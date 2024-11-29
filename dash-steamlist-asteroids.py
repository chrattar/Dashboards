import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Asteroid Analysis")
custom_theme = {'bgcolor': '#0E1117', 'font_color': '#FFFFFF', 'accent_color': '#336699'}

@st.cache_data
def load_data():
    df = pd.read_csv('C:\\nasaneo\\dashboards\\dash_hazard\\data\\orbits.csv', encoding='utf-8')  # or encoding='cp1252'
    return df

df = load_data()
st.title("Asteroid Analysis Dashboard")
st.sidebar.header("Filters")

# Global filter
global_filter = st.sidebar.radio(
   "Global Hazard Filter",
   options=['All', 'Hazardous Only', 'Non-Hazardous Only']
)

# Apply filter
if global_filter == 'Hazardous Only':
   filtered_df = df[df['Hazardous Group'] == 'Hazaardous']
elif global_filter == 'Non-Hazardous Only':
   filtered_df = df[df['Hazardous Group'] == 'Non-Hazardous']
else:
   filtered_df = df

# Create layout
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
# Plot 1: Orbital Classification
with col1:
    st.subheader("Orbital Parameters")
    fig1 = px.scatter(filtered_df,
                     x='Orbit Axis (AU)',
                     y='Orbit Eccentricity',
                     color='Object Class Group',
                     hover_data=['Object Name'],
                     template='plotly_dark')
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)
# Plot 2: Size Analysis
with col2:
    st.subheader("Size Distribution")
    fig2 = px.scatter(filtered_df,
                     x='Orbital Period (yr)',
                     y='Asteroid Magnitude',
                     color='Object Class Group',
                     hover_data=['Object Name'],
                     template='plotly_dark')
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
# Plot 3: Orbital Dynamics
with col3:
    st.subheader("Inclination vs Distance")
    fig3 = px.scatter(filtered_df,
                     x='Perihelion Distance (AU)',
                     y='Orbit Inclination (deg)',
                     color='Object Class Group',
                     hover_data=['Object Name'],
                     template='plotly_dark')
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
# Plot 4: Risk Assessment
with col4:
    st.subheader("Risk Assessment")
    fig4 = px.scatter(filtered_df,
                     x='Minimum Orbit Intersection Distance (AU)',
                     y='Orbit Eccentricity',
                     color='Object Class Group',
                     hover_data=['Object Name'],
                     template='plotly_dark')
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)
# Add metrics
st.subheader("Key Metrics")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Asteroids", len(filtered_df))
m2.metric("Avg Orbital Period", f"{filtered_df['Orbital Period (yr)'].mean():.2f} years")
m3.metric("Avg MOID", f"{filtered_df['Minimum Orbit Intersection Distance (AU)'].mean():.3f} AU")
m4.metric("Potentially Hazardous", len(filtered_df[filtered_df['Hazardous Group'] == 'Hazardous']))
