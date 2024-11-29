import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# Page setup - removed base_path
st.set_page_config(page_title="NEO Dashboard", layout="wide")
#DATA LOAD WITH ABSOLUTE FILEPATH. ***CHANGE WHEN UPLOADING ***
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "data", "neo_v2.csv")
    df = pd.read_csv(file_path)
    df['avg_diameter'] = (df['est_diameter_min'] + df['est_diameter_max']) / 2
    return df

df = load_data()

#My return Links - Change when uploading to server
st.markdown("[← Back to Main Page](http://127.0.0.1:5000)")
st.markdown("""
    <a href="http://127.0.0.1:5000" style="
        color: #339966;
        text-decoration: none;
        padding: 10px;
        display: inline-block;
        margin-bottom: 20px;
    ">← Back to Main Page</a>
""", unsafe_allow_html=True)


# Or for more formatted text using markdown
st.markdown("""
## About This Dashboard
This interactive dashboard visualizes NASA's NEO data, helping you understand:
* Size distributions of asteroids
* Relationship between asteroid size and velocity
* Miss distances and their correlation with other factors

The potentially hazardous designation is based on the asteroid's orbit and size.
""")

st.markdown(r"""
#### LaTeX Examples

Inline equation: $E = mc^2$

Display equation: 
$$\frac{d}{dx}(x^n) = nx^{n-1}$$


""")
# FILTER - SIDEBAR
st.sidebar.header("Filters")
hazard_status = st.sidebar.radio(
    "Hazard Status",
    options=['All', 'Hazardous Only', 'Non-Hazardous Only']
)

### LOG SCALE TOGGLE:
st.sidebar.header("Scale Options")
transform_type = st.sidebar.selectbox(
    "Transform Scale",
    options=['None', 'Cube Root', 'Scale Factor']
)

scale_factor = 1
if transform_type == 'Scale Factor':
    scale_factor = st.sidebar.slider("Scale Factor", 1, 1000, 100)
    
### FILTER REGION ###
if hazard_status == 'Hazardous Only':
    filtered_df = df[df['hazardous'] == True]
elif hazard_status == 'Non-Hazardous Only':
    filtered_df = df[df['hazardous'] == False]
else:
    filtered_df = df


# Calculate average diameter AFTER filtering
filtered_df['avg_diameter'] = (filtered_df['est_diameter_min'] + filtered_df['est_diameter_max']) / 2

# TRANSFORMS - Update therse in the tabs
transformed_df = filtered_df.copy()
if transform_type == 'Cube Root':
    transformed_df['avg_diameter'] = np.cbrt(filtered_df['avg_diameter'])
elif transform_type == 'Scale Factor':
    transformed_df['avg_diameter'] = filtered_df['avg_diameter'] * scale_factor
# Main dashboard
st.title("Near-Earth Objects (NEO) Analysis Dashboard")

# DB Color Scheme
COLORS= {
    'hazardous' :'#ff6b6b',
    'non-hazardous' :'#339966',
    'background' :'#1e2330',
    'paper_bg' :'#0e1117',
    'text' :'#FAFAFA'
}
# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total NEOs", len(filtered_df))
with col2:
    st.metric("Average Diameter (km)", f"{filtered_df['avg_diameter'].mean():.2f}")
with col3:
    st.metric("Potentially Hazardous", len(filtered_df[filtered_df['hazardous'] == True]))

# Visualization sections
tab1, tab2, tab3 = st.tabs(["Size Distribution", "Velocity Analysis", "Miss Distance"])

with tab1:
    # Size distribution plot - HISTOGRAM
    fig = px.histogram(transformed_df, x='avg_diameter',
                      title=f"Size Distribution of NEOs ({transform_type} transform)",
                      color='hazardous',
                      color_discrete_sequence=[COLORS['non-hazardous'], COLORS['hazardous']],
                      labels={'avg_diameter': 'Average Diameter (km)'})
    
    # Add all figure updates BEFORE displaying the chart
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['paper_bg'],
        font_color=COLORS['text'],
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)',
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)',
        )
    )
    
    # Display the chart LAST
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Velocity plot - SCATTER
    fig = px.scatter(transformed_df, x='avg_diameter', y='relative_velocity',
                    color='hazardous', 
                    color_discrete_sequence=[COLORS['non-hazardous'], COLORS['hazardous']],
                    title=f"Size vs Relative Velocity ({transform_type} Transform)",
                    labels={'relative_velocity': 'Relative Velocity (km/s)',
                           'avg_diameter': 'Average Diameter (km)'})
    
    fig.update_layout(
    plot_bgcolor=COLORS['background'],
    paper_bgcolor=COLORS['paper_bg'],
    font_color=COLORS['text'],
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.2)',
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.2)',
        )
    )
        # Display the chart LAST
    st.plotly_chart(fig, use_container_width=True)  

with tab3:
    # Miss distance plot - SCATTER
    fig = px.scatter(transformed_df, x='miss_distance', y='relative_velocity',
                    color='hazardous',
                    color_discrete_sequence=[COLORS['non-hazardous'], COLORS['hazardous']],
                    title=f"Miss Distance vs Velocity({transform_type} Transform)",
                    labels={'miss_distance': 'Miss Distance (km)',
                           'relative_velocity': 'Relative Velocity (km/s)'})
    
    fig.update_layout(
    plot_bgcolor=COLORS['background'],
    paper_bgcolor=COLORS['paper_bg'],
    font_color=COLORS['text'],
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.2)',
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.2)',
        )
    )
    st.plotly_chart(fig, use_container_width=True)

# Add a data table at the bottom
st.subheader("Raw Data")
st.dataframe(filtered_df)
