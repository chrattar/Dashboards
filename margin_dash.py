from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Load your data
df = pd.read_csv('data.csv')

# Convert 'Total Revenue' and 'Total Cost' to numeric, removing non-numeric characters like '$' and commas
df['Total Revenue'] = pd.to_numeric(df['Total Revenue'].replace('[\$,]', '', regex=True), errors='coerce')
df['Total Cost'] = pd.to_numeric(df['Total Cost'].replace('[\$,]', '', regex=True), errors='coerce')

# Calculate Gross Margin % and Gross Profit %
df['Gross Margin %'] = (df['Total Revenue'] - df['Total Cost']) / df['Total Revenue'] * 100
df['Gross Profit %'] = df['Gross Margin %']  # Assuming it's calculated similarly

# Convert 'Period' to datetime if it's not already
df['Period'] = pd.to_datetime(df['Period'])

# Create a consistent color map for 'TopGrp'
unique_groups = df['TopGrp'].unique()
colors = px.colors.qualitative.Plotly  # or any other color palette
color_discrete_map = {group: colors[i % len(colors)] for i, group in enumerate(unique_groups)}

app = Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': '#404040', 'color': 'white', 'padding': '20px', 'fontFamily': 'Verdana'},  # Setting background, text color, and font
    children=[
        html.Div(
            children=[
                html.Img(src='/assets/PeridotLogo.png', style={'height': '100px'}),
                html.H1('Company Dashboard', style={'textAlign': 'left', 'fontFamily': 'Verdana'})
            ],
            style={'textAlign': 'center'}
        ),
        html.Div(
            children=[
                html.A("Revenue vs Gross Margin", href="#revenue-gross-margin-graph", style={'margin-right': '20px', 'color': 'white'}),
                html.A("Gross Profit Percentage", href="#gross-profit-percentage-graph", style={'margin-right': '20px', 'color': 'white'}),
                html.A("Qty Sold vs Unit Avg", href="#qty-vs-unitavg-graph", style={'color': 'white'}),
            ],
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
        dcc.Dropdown(
            id='topgrp-dropdown',
            options=[{'label': i, 'value': i} for i in unique_groups],
            value=[unique_groups[0]],  # Default value as a list
            clearable=False,
            multi=True,  # Enable multi-select
            style={'color': 'black', 'fontFamily': 'Verdana'}  # Set font color to black and font to Verdana
        ),
        html.Div(id='revenue-gross-margin-graph-container', children=[
            dcc.Graph(id='revenue-gross-margin-graph')
        ]),
        html.Div(id='gross-profit-percentage-graph-container', children=[
            dcc.Graph(id='gross-profit-percentage-graph')
        ])
    ]
)

@app.callback(
    [Output('revenue-gross-margin-graph', 'figure'),
     Output('gross-profit-percentage-graph', 'figure')],
    [Input('topgrp-dropdown', 'value')]
)
def update_figures(selected_topgrps):
    # Filter the DataFrame based on selected 'TopGrps'
    filtered_df = df[df['TopGrp'].isin(selected_topgrps)].sort_values('Period')

    # First graph with Period on the x-axis and Gross Margin % on the y-axis
    fig1 = px.scatter(filtered_df, x="Period", y="Gross Margin %",
                      size="Total Revenue", color="TopGrp", hover_name="TopGrp",
                      color_discrete_map=color_discrete_map,
                      symbol="TopGrp", title="Gross Margin % Over Time")

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(
        transition_duration=500,
        xaxis_title="Period",
        yaxis_title="Gross Margin %",
        plot_bgcolor='#404040',  # Dark grey background
        paper_bgcolor='#404040',  # Dark grey background
        font=dict(color='white', family='Verdana'),
        xaxis=dict(showgrid=True, gridcolor='#606060'),
        yaxis=dict(showgrid=True, gridcolor='#606060')
    )

    # Second graph as a bar chart for Gross Profit % over months
    fig2 = px.bar(filtered_df, x='Period', y='Gross Profit %', color='TopGrp',
                  barmode='group',
                  labels={"Period": "Month", "Gross Profit %": "Gross Profit Percentage"},
                  color_discrete_map=color_discrete_map, title="Gross Profit % Over Time")

    fig2.update_layout(
        transition_duration=500,
        plot_bgcolor='#404040',  # Dark grey background
        paper_bgcolor='#404040',  # Dark grey background
        font=dict(color='white', family='Verdana'),
        xaxis=dict(showgrid=True, gridcolor='#606060'),
        yaxis=dict(showgrid=True, gridcolor='#606060')
    )

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
