#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 00:17:08 2026

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
import os
import utils.data
from utils.transformation.data_transformer import HeatMapDataTransformer

dash.register_page(
    __name__,
    path='/',
    name = 'Home',
    title='Home'
)

hmapdf = pd.read_csv(os.path.join(os.path.dirname(__file__), '../utils/data/heatmap_df2.csv'))

##print("interactive map check:\n", hmapdf.head())

newsensors = ['North Central Troy #1', 'Schenectady #23', 'Albany #28', 'Greater Ravena - Coeymans #13',
              'Ravena #31', 'Greater Ravena - Coeymans #20', 'Greater Ravena - Coeymans #18',
              'Greater Ravena - Coeymans #12', 'Selkirk #18', 'Rensselaer #9', 'Capital Region #22',
              'Lansingburgh #8', 'Cohoes #15', 'Cohoes #16', 'Cohoes #17', 'Cohoes ##', 'South Troy #2', 'Rensselaer #10']

newday = 2
newmonth = 12
newyear= 2025
newhour = 12
newintensity = 0.00

# 2. Function to generate the Folium map as an HTML string
def generate_folium_map(min_intensity=newintensity, sensorNames=newsensors,
                        dayz=newday, monthz=newmonth, yearz=newyear, hourz=newhour):
    
    hmap_transformer = HeatMapDataTransformer(hmapdf)
    
    # Debug data availability BEFORE full filtering
##    print("Total unique sensors in DF:", hmapdf['SensorName'].nunique())  # Should match your transform_dict keys
##    day_hour_mask = (hmapdf['day'] == dayz) & (hmapdf['hour'] == hourz)
##    print(f"Rows for day {dayz}, hour {hourz}:", day_hour_mask.sum())  # Total rows for this time, ignoring sensors/intensity
##    print("Sensors with data for this day/hour:", hmapdf[day_hour_mask]['SensorName'].unique())  # Key: Lists which sensors have ANY data here
##    print("Rows per sensor for this day/hour:\n", hmapdf[day_hour_mask].groupby('SensorName').size())  # Breakdown by sensor
##    print("Pre intensity check:", hmapdf[day_hour_mask]['avg_AQI'].describe())
    
    filtered_df = hmap_transformer.sensorNamefix().heatmapIntensity().heatmapTable(min_intensity, sensorNames, dayz, monthz, yearz, hourz)
    print("Post intensity check:", filtered_df['intensity'].describe())
    # Create a base map
    m = folium.Map(location=[42.75105, -73.67981], zoom_start=11)

    # Add heatmap layer
    if not filtered_df.empty:
        filtdf = filtered_df[['longitude', 'latitude', 'intensity']].values.tolist()
        
        HeatMap(data=filtdf,
                radius=25,
                blur=20,
                max_zoom=13,
                min_opacity=0.35,
                gradient={0.0: 'pink', 0.17: 'green', 0.33: 'yellow', 0.5: 'orange', 0.66: 'red', 1: 'purple'}
               ).add_to(m)   

    # Get the HTML content of the map as a string
    src_doc = m.get_root().render()
    return src_doc

# 4. Define the app layout
layout = dbc.Container([

    dbc.Row([
            
            dcc.Slider(
                id='intensity-slider',
                min=0.0,
                max=1.0,
                step=0.10,  # continuous float control
                value=0.0,
                tooltip={"placement": "bottom", "always_visible": True} # smoother experience
            ), html.Div(id='slider-output-container')
        ]),
    html.Br(),
    dbc.Row([
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
                        "Date Selection",
                        style={
                            'backgroundColor': '#fffef5',
                            'border': '1px solid #EBB866',
                            'padding': '10px',
                            'fontSize': '1.3rem',
                            'margin': '0 0 12px 0',    # spacing below header
                            'width': '100%'            # full width of container
                        }
                    ),
                    dcc.DatePickerSingle(
                        id='my-date-picker-single',
                        min_date_allowed=date(2023, 3, 10),
                        max_date_allowed=date(2025, 12, 29),
                        initial_visible_month=date(2025, 12, 2),
                        date=date(2025, 12, 2)
                    ), html.Div(id='output-container-date-picker-single')
                    
                ]
            ),
        
            html.Br(),  # or use margin-bottom on previous div
        
            # ── Line Chart Section ──────────────────────────────────────
            html.Div(
                style={
                    'width': '95%',
                    'maxWidth': '900px',
                    'margin': '0 auto',
                    'textAlign': 'center'
                },
                children=[
                    html.H1(
                        "Hour Selection",
                        style={
                            'backgroundColor': '#fffef5',
                            'border': '1px solid #EBB866',
                            'padding': '10px',
                            'fontSize': '1.3rem',
                            'margin': '0 0 12px 0',
                            'width': '100%'
                        }
                    ),
                    dcc.Dropdown(
                        id='hour-dropdown',
                        options=[
                            {'label': f'{h:02d}:00', 'value': h}
                            for h in range(24)
                            ],
                        value=newhour,
                        clearable=False,
                        style={'width': '150px'}
                        ), html.Div(id='hour-label')
                    
                    ])
                ], width = 12, md=2, className="mb-4"),
        
            dbc.Col([
                # ── Pie Chart Section ───────────────────────────────────────
                html.Div(
                    style={
                        'width': '95%',
                        'maxWidth': '900px',           # ← optional: cap max width so it doesn't stretch too wide on large screens
                        'margin': '0 auto',            # ← this centers the whole block
                        'textAlign': 'center'          # fallback centering
                    },
                    children=[
                        html.H1(
                            "AQI Intensity Readings from Prior Week",
                            style={
                                'backgroundColor': '#fffef5',
                                'border': '1px solid #EBB866',
                                'padding': '10px',
                                'fontSize': '1.3rem',
                                'margin': '0 0 12px 0',    # spacing below header
                                'width': '100%'            # full width of container
                            }
                        ),
                        html.Iframe(
                            id='folium-iframe',
                            srcDoc=generate_folium_map(), # Initial map
                            style={'width': '100%', 'height': '600px', 'border': 'none'})
                    ]
                ),
            
            ], width=12, md=7, className="mb-4"),
        
        dbc.Col([
            # ── Pie Chart Section ───────────────────────────────────────
            html.Div(
                style={
                    'width': '95%',
                    'maxWidth': '900px',           # ← optional: cap max width so it doesn't stretch too wide on large screens
                    'margin': '0 auto'        # fallback centering
                },
                children=[
                    html.H1(
                        "Sensor Selection",
                        style={
                            'backgroundColor': '#fffef5',
                            'border': '1px solid #EBB866',
                            'padding': '10px',
                            'fontSize': '1.3rem',
                            'margin': '0 0 12px 0',    # spacing below header
                            'width': '100%',
                            'text-align': 'center' # full width of container
                        }
                    ),
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
                        value=["North Central Troy #1",
                               "Schenectady #23", "Albany #28",
                               "Greater Ravena - Coeymans #13",
                               "Greater Ravena - Coeymans #13",
                               "Greater Ravena - Coeymans #20",
                               "Greater Ravena - Coeymans #19",
                               "Greater Ravena - Coeymans #12",
                               "Greater Ravena - Coeymans #18",
                               "Rensselaer #9",
                               "Capital Region #22",
                               "Lansingburgh #8",
                               "Cohoes #15",
                               "Cohoes #16",
                               "Cohoes #17",
                               "Cohoes ##",
                               "South Troy #2",
                               "Rensselaer #10"],
                        style={'backgroundColor': '#ffffff', 'padding': '10px', 'border': '1px solid #e0d8b0'}, # Initial selected values
                        labelStyle={"display": "block"}, # Display options vertically
                        ), html.Div(id="output-container")
                ]
            )
        ], width=12, md=3, className="mb-4")
    
    ], className="g-0")
], fluid=True)

# 5. Define the Dash callback
@callback(
    Output('folium-iframe', 'srcDoc'),
    [
        Input('intensity-slider', 'value'),
        Input('my-date-picker-single', 'date'),
        Input('city-checklist', 'value'),
        Input('hour-dropdown', 'value')
    ]
)
def update_map(intensity, date_value, sensors, hour):
    
    print("Selected sensors (raw input):", sensors)  # Should be a list like ['North Central Troy #1', 'Schenectady #23', ...]
   
    selected_intensity = intensity if intensity is not None else newintensity
        
    # Use the selected sensors, fall back to default list if nothing selected
    selected_sensors = sensors if sensors else newsensors
    print("Final selected_sensors count:", len(selected_sensors))  # Should be >1 if multiple checked
    
    # Same for year (although year-dropdown has clearable=False so this is less critical)
    selected_day = date.fromisoformat(date_value).day if date_value is not None else newday
    selected_month = date.fromisoformat(date_value).month if date_value is not None else newmonth
    selected_year = date.fromisoformat(date_value).year if date_value is not None else newyear
    
    selected_hour = hour if hour is not None else newhour
    
    Hmap = generate_folium_map(
        min_intensity=selected_intensity,
        sensorNames=selected_sensors,
        dayz=selected_day,
        monthz=selected_month,
        yearz=selected_year,
        hourz=selected_hour
    )

    return Hmap