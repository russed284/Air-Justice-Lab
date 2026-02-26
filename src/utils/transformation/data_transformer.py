#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 18:12:06 2026

@author: daltonrussell
"""

import pandas as pd
import base64
import io
from datetime import date
import numpy as np


############
## Set up sensor name transformation for all sensors
############
transform_dict = {'/ Capital Region Air Justice Lab #2 (South Troy) Info at: www.mediasanctuary.org': 'South Troy #2',
'Rensselaer Environmental Coalition / Capital Region Air Justice Lab #10': 'Rensselaer #10',
'Lights Out Norlite / Capital Region Air Justice Lab (Cohoes) Info at: www.mediasanctuary.org/ajl': 'Cohoes ##',
'Lights Out Norlite / Capital Region Air Justice Lab #17 (Cohoes) Info at: www.mediasanctuary.org/ajl': 'Cohoes #17',
'Lights Out Norlite / Capital Region Air Justice Lab #16 (Cohoes) Info at: www.mediasanctuary.org/ajl': 'Cohoes #16',
'Lights Out Norlite / Capital Region Air Justice Lab #15 (Cohoes) Info at: www.mediasanctuary.org/ajl': 'Cohoes #15',
'/ Capital Region Air Justice Lab #8 (Lansingburgh) Info at: www.mediasanctuary.org': 'Lansingburgh #8',
'NATURE Lab/Capital Region Air Justice Lab #22': 'Capital Region #22',
'Rensselaer Environmental Coalition / Capital Region Air Justice Lab #9 (Rensselaer) Info at: www.mediasanctuary.org': 'Rensselaer #9',
'Clean Air Coalition of Greater Ravena-Coeymans / Capital Region Air Justice Lab #18 (Selkirk) Info at: www.mediasanctuary.org/ajl': 'Selkirk #18',
'Clean Air Coalition of Greater Ravena-Coeymans / Capital Region Air Justice Lab #12 (Coeymans) Info at: www.mediasanctuary.org/ajl': 'Greater Ravena - Coeymans #12',
'Clean Air Coalition of Greater Ravena-Coeymans / Capital Region Air Justice Lab #19 (Coeymans) Info at: www.mediasanctuary.org/ajl': 'Greater Ravena - Coeymans #18',
'Clean Air Coalition of Greater Ravena-Coeymans / Capital Region Air Justice Lab #20 (Coeymans) Info at: www.mediasanctuary.org/ajl': 'Greater Ravena - Coeymans #20',
'Clean Air Coalition of Greater Ravena- Coeymans/ Capital Region Air Justice Lab # 13': 'Greater Ravena - Coeymans #13',
'NATURE Lab/ Capital Region Air Justice Lab # 31 (Ravena) ': 'Ravena #31',
'NATURE Lab/Capital Region Air Justice #28 (Albany)': 'Albany #28',
'NATURE Lab/Capital Region Air Justice #23 (Schenectady) ': 'Schenectady #23',
'/ Capital Region Air Justice Lab #1 (North Central Troy) Info at: www.mediasanctuary.org': 'North Central Troy #1'}


###########
## Apply function for all sensors
###########
def change_sensname(string):
    
    for key, value in transform_dict.items():
        
        if key == string:
            string = value
            
    return string

def intensity_norm(num):
    if num > 1:
        return 1
    else:
        return np.round(num, 2)


class TreeMapDataTransformer:
    
    def __init__(self, df):
        self.df = df.copy()
        
    def sensorNamefix(self, sensordict=transform_dict):
        self.df['SensorName'] = self.df['SensorName'].apply(lambda x: change_sensname(x))
        return self
    
    def sensordataTable(self, sensorlist, selected_year):
        self.df['Count'] = self.df['AQI_Range']
        masksensor = self.df['SensorName'].isin(sensorlist)
        maskyear = self.df['year'] == selected_year
        
        filtered_df = self.df[masksensor & maskyear]
        
        table1 = filtered_df.groupby(['SensorName', 'year', 'AQI_Range'], as_index=False)['Count'].count()
        
        health_list = {'Unhealthy for Sensitive Groups': 0, 'Unhealthy': 1, 'Very Unhealthy': 2, 'Hazardous': 3}
        
        table2 = table1.sort_values(by='AQI_Range', key=lambda s: s.map(health_list))
        table2 = table2.rename(columns={'year': 'Year', 'AQI_Range': 'AQI Range', 'Count': 'Total Occurences'})
        
        
        return table2
    
    def treemapTable(self, sensorlist, selected_year):
              
        self.df['Range2'] = self.df['AQI_Range']
        masksensor = self.df['SensorName'].isin(sensorlist)
        maskyear = self.df['year'] == selected_year
    
        filtered_df = self.df[masksensor & maskyear]
    
        table1 = filtered_df.groupby(['SensorName', 'year', 'AQI_Range'], as_index=False)['Range2'].count()
        table_tmap = table1.rename(columns={'Range2': 'Total Bad Readings'})
        
        return table_tmap

class PieGraphDataTransformer:
    
    def __init__(self, df):
        self.df = df.copy()
        
    def sensorNamefix(self, sensordict=transform_dict):
        self.df['SensorName'] = self.df['SensorName'].apply(lambda x: change_sensname(x))
        return self
    
    def piegraphTable(self, sensorlist, monthlist, yearlist):
        
        masksensor = self.df['SensorName'].isin(sensorlist)
        maskmonth = self.df['month'].isin(monthlist)
        maskyear = self.df['year'].isin(yearlist)
        
        self.df['Total'] = self.df['AQI_Range']
        piecopy = self.df.copy()
    
        filtered_pie = piecopy[masksensor & maskyear & maskmonth]
    
        piedf = filtered_pie.groupby(['SensorName', 'month', 'AQI_Range'], as_index=False)['Total'].count()
        piedf = piedf.rename(columns={'AQI_Range': 'AQI Range', 'month': 'Month'})
        
        return piedf
    
    def linegraphTable(self, sensorlist, monthlist, yearlist):
        
        masksensor = self.df['SensorName'].isin(sensorlist)
        maskmonth = self.df['month'].isin(monthlist)
        maskyear = self.df['year'].isin(yearlist)
        
        linecopy = self.df.copy()
        filtered_line = linecopy[masksensor & maskyear & maskmonth]
        linedf = filtered_line.groupby(['SensorName', 'month', 'hour'], as_index=False)['avg_AQI'].mean()
        linedf = linedf.rename(columns={'month': 'Month', 'hour': 'Hour', 'avg_AQI': 'Average AQI'})
        
        return linedf
    
class HeatMapDataTransformer:

    def __init__(self, df):
        self.df = df[['SensorName', 'hour', 'day', 'month', 'year', 'latitude', 'longitude', 'avg_AQI']].copy()
        
    def sensorNamefix(self, sensordict=transform_dict):
        self.df['SensorName'] = self.df['SensorName'].apply(lambda x: change_sensname(x))
        print("Unique sensors after fix:", self.df['SensorName'].unique())  # Should be short names now
        return self
    
    def heatmapIntensity(self):
        
        self.df['intensity'] = self.df['avg_AQI'] / 300
        self.df['intensity'] = self.df['intensity'].apply(lambda x: intensity_norm(x))
        
        return self

    def heatmapTable(self, selected_intensity, sensorlist, selected_day, selected_month, selected_year, selected_hour):
        print("In table - Sensor list received:", sensorlist)  # Confirm same as callback (multiple?)
        print("In table - DF unique sensors:", self.df['SensorName'].unique())  # Short names—compare to sensorlist
        
        maskintensity = self.df['intensity'] >= selected_intensity
        masksensors = self.df['SensorName'].isin(sensorlist)
        maskmonth = self.df['month'] == selected_month
        maskyear = self.df['year'] == selected_year
        maskday = self.df['day'] == selected_day
        maskhour = self.df['hour'] == selected_hour
        
        # Existing mask sums - keep
        print("Mask sums - intensity:", maskintensity.sum(), "sensors:", masksensors.sum(), 
              "day:", maskday.sum(), "month:", maskmonth.sum(), "year:", maskyear.sum(), "hour:", maskhour.sum())
        
        # NEW: Combined masks step-by-step
        month_year = maskmonth & maskyear
        print("Rows after month/year:", month_year.sum())
        day_hour = month_year & maskday & maskhour
        print("Rows after day/hour:", day_hour.sum())
        day_hour_intensity = day_hour & maskintensity
        print("Rows after +intensity:", day_hour_intensity.sum())
        full_mask = day_hour_intensity & masksensors
        print("Rows after +sensors:", full_mask.sum())  # Should match filtered_df rows
        
        filtered_df = self.df[full_mask]  # Use full_mask
        print("Filtered DF shape:", filtered_df.shape)
        print("Filtered sensors count:\n", filtered_df['SensorName'].value_counts())
        print("Filtered intensities:\n", filtered_df['intensity'].value_counts())
        
        self.df = filtered_df
        return self.df
'''
    def heatmapTable(self, selected_intensity, sensorlist, selected_day, selected_month, selected_year, selected_hour):
        
        maskintensity = self.df['intensity'] >= selected_intensity
        masksensors = self.df['SensorName'].isin(sensorlist)
        maskday = self.df['day'] == selected_day
        maskmonth = self.df['month'] == selected_month
        maskyear = self.df['year'] == selected_year
        maskhour = self.df['hour'] == selected_hour
        
        print("Mask sums - intensity:", maskintensity.sum(), "sensors:", masksensors.sum(), 
          "day:", maskday.sum(), "hour:", maskhour.sum())
        # Filter data based on the slider value
        filtered_df = self.df[maskintensity & masksensors & maskday & maskmonth & maskyear & maskhour]
        print("Filtered DF shape:", filtered_df.shape)
        print("filtered df sensors:", filtered_df['SensorName'].value_counts())
        print("filtered df aqi: ", filtered_df['intensity'].value_counts())
        self.df = filtered_df
        return self.df
'''