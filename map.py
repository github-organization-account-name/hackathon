import pandas as pd;
import streamlit as st
import pyTigerGraphBeta as tg
import numpy as np
import json


def load_coordinate(option, conn):
    if (option == 'All airports'):
        airports = conn.runInstalledQuery("getAllAirports", params=None, timeout=16000)
    else:
        params = "country=" + option
        airports = conn.runInstalledQuery('getAirportsByCountry',params= params, timeout=16000)
    df = pd.DataFrame(airports[0])
    points = pd.DataFrame([], columns=['id', 'lat', 'lon', 'name'])
    for i in range(len(df)):
        a_id = df.loc[i, "Result"]['attributes']['id']
        lat = df.loc[i, "Result"]['attributes']['latitude']
        lon = df.loc[i, "Result"]['attributes']['longitude']
        name = df.loc[i, "Result"]['attributes']['name']
        points.loc[i] = [a_id, lat, lon, name]
    return points



