#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 00:16:03 2026

@author: daltonrussell
"""

import dash
from dash import dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import folium
from folium.plugins import HeatMap
import pandas as pd
import base64
import io
from datetime import date
import numpy as np
import plotly.express as px
import os

from utils.transformation.data_transformer import TreeMapDataTransformer

dash.register_page(
    __name__,
    path='/badAQI',
    name='Annual Bad AQI',
    title='AnnualBadAQI'
)

tmap_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../utils/data/treemap_df.csv'))
##print("heatmap df check:\n", tmap_df.head())

newsensor = ['North Central Troy #1',
             'South Troy #2',
             'Albany #28']
newyear=2025

dtable_transform = TreeMapDataTransformer(tmap_df)

bad_table = dtable_transform.sensorNamefix().sensordataTable(newsensor, newyear)


def initiate_treemap(sensorName=newsensor, yearz=newyear):
    
    tmap_transformer = TreeMapDataTransformer(tmap_df)

    treedf = tmap_transformer.sensorNamefix().treemapTable(sensorName, yearz)
    
    all_tree_fig = px.treemap(
        treedf,
        path=[px.Constant("Year Selected"), 'SensorName'],  # Add a root node for clarity
        values='Total Bad Readings',
        color='Total Bad Readings',  # Optional: color based on a numerical value
        color_continuous_scale='reds'  # Optional: choose a color scale
    )
    
    # Add this to set the border/line color around each rectangle
    all_tree_fig.update_traces(
        marker=dict(
            line=dict(
                color='#e0d8b0',    # ← matches your dropdown border
                width=2             # ← adjust thickness as needed (1–3 looks good usually)
            )
        ),
        hovertemplate='%{label}<br>Total Bad Readings: %{value}<extra></extra>' 
    )
    
    # Your existing layout update
    all_tree_fig.update_layout(
        # Optional: make background match your app better
        paper_bgcolor='rgba(0,0,0,0)',      # transparent → uses app background
        margin=dict(t=60, l=10, r=10, b=10) # tighter margins if you want
    )
    return all_tree_fig

def initiate_table(sensorName=newsensor, yearz=newyear):
    
    bad_table = dtable_transform.sensorNamefix().sensordataTable(sensorName, yearz)
    
    return bad_table

# 4. Define the app layout
layout = html.Div([

    dbc.Container([
    
        dbc.Row([
            dbc.Col([
                html.H1(
                    children="Year Selection", style={
                    'textAlign': 'center',       # Center the text
                    'backgroundColor': '#fffef5', ##fffef5
                    'border': '1px solid #EBB866',
                    'borderRadius': '0',      # Add rounded corners
                    'padding': '10px',
                    'font-size': '1.3rem' # Add some space around the text # Add a border
                }),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[
                        {'label': str(y), 'value': y}
                        for y in range(2023, 2026)  # 2023, 2024, 2025
                        ],
                    value=newyear,
                    clearable=False,
                    style={'width': '150px'}
                    ), html.Div(id='year-label'),
                
                html.Br() 
                ], width = 12, md=2),
            
            dbc.Col([
                html.H1(
                    children="Bad AQI Readings by Year", style={
                    'textAlign': 'center',       # Center the text
                    'backgroundColor': '#fffef5', ##fffef5
                    'border': '1px solid #EBB866',
                    'borderRadius': '0',      # Add rounded corners
                    'padding': '10px',
                    'font-size': '1.3rem' # Add some space around the text # Add a border
                }),
                html.Div(style={'display': 'flex', 'justify-content': 'center'}, children=[
                                   dcc.Graph(id='tree-map-vis', figure = initiate_treemap())]),
                html.Br(),
                html.Div(
                    style={'width': '100%'},
                    children=[
                        dash_table.DataTable(
                            id='tbl',
                            columns=[{"name": i, "id": i} for i in bad_table.columns],
                            data=bad_table.sort_values('AQI Range').to_dict('records'),
                            sort_action='none',
                            style_table={
                                'width': '100%',
                                'minWidth': '100%',
                                'overflowX': 'auto',
                            },
                            style_cell={
                                'minWidth': 80, 'width': 80, 'maxWidth': 180,   # ← adjust these values to your needs
                                'whiteSpace': 'normal',       # allow text wrapping
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                },   # as above
                        )
                    ]
                )
                
            ], width=12, md=8, className="mb-4"),
            
            dbc.Col([
                html.H1(
                    children="Sensor Selection", style={
                    'textAlign': 'center',       # Center the text
                    'backgroundColor': '#fffef5', ##fffef5
                    'border': '1px solid #EBB866',
                    'borderRadius': '0',      # Add rounded corners
                    'padding': '10px',
                    'font-size': '1.3rem' # Add some space around the text # Add a border
                }),
                dcc.Checklist(
                    id="city-checklist",
                    options=[
                        {"label": "North Central Troy #1", "value": "North Central Troy #1"},
                        {"label": "Schenectady #23", "value": "Schenectady #23"},
                        {"label": "Albany #28", "value": "Albany #28"},
                        {"label": "Greater Ravena - Coeymans #13", "value": "Greater Ravena - Coeymans #13"},
                        {"label": "Ravena #31", "value": "Ravena #31"},
                        {"label": "Greater Ravena - Coeymans #20", "value": "Greater Ravena - Coeymans #20"},
                        {"label": "Greater Ravena - Coeymans #19", "value": "Greater Ravena - Coeymans #19"},
                        {"label": "Greater Ravena - Coeymans #12", "value": "Greater Ravena - Coeymans #12"},
                        {"label": "Greater Ravena - Coeymans #18", "value": "Greater Ravena - Coeymans #18"},
                        {"label": "Rensselaer #9", "value": "Rensselaer #9"},
                        {"label": "Capital Region #22", "value": "Capital Region #22"},
                        {"label": "Lansingburgh #8", "value": "Lansingburgh #8"},
                        {"label": "Cohoes #15", "value": "Cohoes #15"},
                        {"label": "Cohoes #16", "value": "Cohoes #16"},
                        {"label": "Cohoes #17", "value": "Cohoes #17"},
                        {"label": "Cohoes ##", "value": "Cohoes ##"},
                        {"label": "South Troy #2", "value": "South Troy #2"},
                        {"label": "Rensselaer #10", "value": "Rensselaer #10"}
                        ],
                    value=['North Central Troy #1',
                                 'South Troy #2',
                                 'Albany #28'],
                    style={'backgroundColor': '#ffffff', 'padding': '10px', 'border': '1px solid #e0d8b0'}, # Initial selected values
                    labelStyle={"display": "block"}, # Display options vertically
                    ), html.Div(id="output-container")
                
                ], width=12, md=2, className="mb-4")
            
            ], className="gx-4")
    
    ], fluid=True)
])

# 5. Define the Dash callback
@callback(
    [
     Output('tree-map-vis', 'figure'),
     Output('tbl', 'data')
     ],
    [
        Input('city-checklist', 'value'),
        Input('year-dropdown', 'value')
    ]
)
def update_map(sensors, year):
    # Use the selected sensors, fall back to default list if nothing selected
    selected_sensors = sensors if sensors else newsensor
    
    # Same for year (although year-dropdown has clearable=False so this is less critical)
    selected_year = year if year is not None else newyear

    fig = initiate_treemap(
        sensorName=selected_sensors,
        yearz=selected_year
    )
    
    table_df = initiate_table(
        sensorName=selected_sensors,
        yearz=selected_year
    )
    
    return fig, table_df.to_dict('records')