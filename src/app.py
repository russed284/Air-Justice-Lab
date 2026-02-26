#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 20:12:25 2026

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

from components.navbar import navbar

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title='Air Justice Dash App'
    )

def serve_layout():
    
    return html.Div(
        [
            navbar,
            dbc.Container(
                dash.page_container,
                class_name='my-2'      
                )
            
            ]
        
        )

app.layout = serve_layout
server = app.server

if __name__ == "__main__":
    app.run(debug=True, port=8058)