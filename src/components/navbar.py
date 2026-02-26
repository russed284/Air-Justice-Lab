#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 17:40:41 2026

@author: daltonrussell
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Heatmap", href="/heatmap", active="exact")),
        dbc.NavItem(dbc.NavLink("Treemap", href="/treemap", active="exact")),
        dbc.NavItem(dbc.NavLink("Piegraph", href="/piegraph", active="exact"))
    ],
    brand="Air Justice Lab",
    brand_href="/",
    color="dark",
    dark=True,
    fluid=True,
    sticky="top",
    className="full-width-navbar mb-3",
)