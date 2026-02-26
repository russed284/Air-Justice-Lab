#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 00:16:37 2026

@author: daltonrussell
"""

import dash
from dash import dcc, html, Input, Output, callback
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
from utils.transformation.data_transformer import PieGraphDataTransformer

dash.register_page(
    __name__,
    path='/monthly',
    name='Monthly AQI',
    title='MonthlyAQI'
)

p_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../utils/data/heatmap_df2.csv'))
##print("pie df check:\n", p_df.head())

newsensor = ['North Central Troy #1']
newmonth=12
newyear=2025


def initiate_piegraph(sensorName=newsensor, monthz=newmonth, yearz=newyear):
    
    pgraph_transformer = PieGraphDataTransformer(p_df)
    
    monthz = [monthz] if not isinstance(monthz, list) else monthz
    yearz = [yearz] if not isinstance(yearz, list) else yearz

    piedf = pgraph_transformer.sensorNamefix().piegraphTable(sensorName, monthz, yearz)
    
    figpie = px.pie(piedf, values='Total', names='AQI Range', color='AQI Range', color_discrete_map={'Good':'green','Moderate':'yellow', 'Unhealthy for Sensitive Groups':'orange', 'Unhealthy':'red', 'Very Unhealthy': 'violet', 'Hazardous': 'darkred', 'NaN': 'cyan'})
    
    figpie.update_layout(
        # Optional: make background match your app better
        paper_bgcolor='rgba(0,0,0,0)',      # transparent → uses app background
        margin=dict(t=60, l=10, r=10, b=10) # tighter margins if you want
    )
    return figpie

def initiate_linegraph(sensorName=newsensor, monthz=newmonth, yearz=newyear):
    
    lgraph_transformer = PieGraphDataTransformer(p_df)
    
    monthz = [monthz] if not isinstance(monthz, list) else monthz
    yearz = [yearz] if not isinstance(yearz, list) else yearz

    linedf = lgraph_transformer.sensorNamefix().linegraphTable(sensorName, monthz, yearz)
    
    lingraph = px.line(linedf, x='Hour', y='Average AQI', color='SensorName', text='Average AQI')
    
    lingraph.update_layout(
        # Optional: make background match your app better
        paper_bgcolor='rgba(255,255,255,0.8)',      # transparent → uses app background
        margin=dict(t=10, l=10, r=10, b=10),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1) # tighter margins if you want
    )
    lingraph.update_traces(
        mode='lines+text',  # ← Enables text labels (add +markers if you want dots on points)
        texttemplate='%{text:.2s}',  # Formats to 2 significant figures (e.g., '50' or '1.2k')
        textposition='top left',
        textfont = dict(size=10)# Positions above the points
    )
    
    return lingraph

layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            
            html.H1(
                children="Year Selection", style={
                'textAlign': 'center',       # Center the text
                'backgroundColor': '#fffef5', ##fffef5
                'border': '1px solid #EBB866',
                'borderRadius': '0',      # Add rounded corners
                'padding': '10px',
                'font-size': '1.3rem',
                'width': '95%'  # Add some space around the text # Add a border
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
            
            html.Br(),
            
            html.H1(
                children="Month Selection", style={
                'textAlign': 'center',       # Center the text
                'backgroundColor': '#fffef5', ##fffef5
                'border': '1px solid #EBB866',
                'borderRadius': '0',      # Add rounded corners
                'padding': '10px',
                'font-size': '1.3rem',
                'width': '95%'  # Add some space around the text # Add a border
            }),
            
            dcc.Dropdown(
                id='month-dropdown',
                options=[
                    {'label': str(m), 'value': m}
                    for m in range(0, 13)
                    ],
                value=newmonth,
                clearable=False,
                style={'width': '150px'}
                ), html.Div(id='month-label')
            
            ], width = 12, md=2),
        
            dbc.Col([
                # ── Pie Chart Section ───────────────────────────────────────
                html.Div(
                    style={
                        'width': '100%',
                        'maxWidth': '900px',           # ← optional: cap max width so it doesn't stretch too wide on large screens
                        'margin': '0 auto',            # ← this centers the whole block
                        'textAlign': 'center'          # fallback centering
                    },
                    children=[
                        html.H1(
                            "AQI Reading Classifications by Month & Sensor",
                            style={
                                'backgroundColor': '#fffef5',
                                'border': '1px solid #EBB866',
                                'padding': '10px',
                                'fontSize': '1.3rem',
                                'margin': '0 0 12px 0',    # spacing below header
                                'width': '100%'            # full width of container
                            }
                        ),
                        dcc.Graph(
                            id='pie-graph-chart',
                            style={
                                'width': '100%',
                                'height': '300px'
                            },
                            figure=initiate_piegraph()
                        )
                    ]
                ),
            
                html.Br(),  # or use margin-bottom on previous div
            
                # ── Line Chart Section ──────────────────────────────────────
                html.Div(
                    style={
                        'width': '100%',
                        'maxWidth': '900px',
                        'margin': '0 auto',
                        'textAlign': 'center'
                    },
                    children=[
                        html.H1(
                            "Average AQI by Hour & Sensor",
                            style={
                                'backgroundColor': '#fffef5',
                                'border': '1px solid #EBB866',
                                'padding': '10px',
                                'fontSize': '1.3rem',
                                'margin': '0 0 12px 0',
                                'width': '100%'
                            }
                        ),
                        dcc.Graph(
                            id='line-graph-chart',
                            style={
                                'width': '100%',
                                'height': '300px'
                            },
                            figure=initiate_linegraph()
                        )
                    ]
                )
            ], width=12, md=7, className="mb-4"),
        
        dbc.Col([
            
               html.Div(
                   style={
                       'width': '100%',
                       'maxWidth': '900px',           # ← optional: cap max width so it doesn't stretch too wide on large screens
                       'margin': '0 auto'            # ← this centers the whole block        # fallback centering
                   },
                   children=[
                        html.H1(
                            children="Sensor Selection", style={
                            'textAlign': 'center',       # Center the text
                            'backgroundColor': '#fffef5', ##fffef5
                            'border': '1px solid #EBB866',
                            'borderRadius': '0',      # Add rounded corners
                            'padding': '10px',
                            'font-size': '1.3rem',
                            'width': '95%'  # Add some space around the text # Add a border
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
                            value=["North Central Troy #1"],
                            style={'backgroundColor': '#ffffff', 'padding': '10px', 'border': '1px solid #e0d8b0'}, # Initial selected values
                            labelStyle={"display": "block"}, # Display options vertically
                            ), html.Div(id="output-container")
                               ]
                           ),
            
            ], width=12, md=3, className="mb-4")
        
    ], className="gx-4")
    
], fluid=True)

# 5. Define the Dash callback
@callback(
    
    [
     Output('pie-graph-chart', 'figure'),
     Output('line-graph-chart', 'figure')
     
     ],
    
    [
        Input('month-dropdown', 'value'),
        Input('city-checklist', 'value'),
        Input('year-dropdown', 'value')
    ]
)
def update_map(month, sensors, year):

    # Use the selected sensors, fall back to default list if nothing selected
    selected_sensors = sensors if sensors else newsensor
    
    # Same for year (although year-dropdown has clearable=False so this is less critical)
    selected_year = year if year is not None else newyear
    
    selected_month = month if month is not None else newmonth
    # ---- Day filter ----
        
    pieG = initiate_piegraph(
        sensorName=selected_sensors,
        monthz=selected_month,
        yearz=selected_year
    )
    
    lineG = initiate_linegraph(
        sensorName=selected_sensors,
        monthz=selected_month,
        yearz=selected_year
    )

    return pieG, lineG