import pyTigerGraphBeta as tg
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import json
import plotly.express as px
from geopy.geocoders import Nominatim
from util import *

def set_map(data, color):
    data = set_score(data)
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.data_utils.compute_view(data[['lng','lat']]),
        tooltip={"text": "{Vertex_ID}\n{name}"},
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=data,
                pickable=True,
                opacity=0.4,
                stroked=True,
                filled=True,
                radius_scale=6,
                get_radius=["score"],
                radius_pixels=["score"],
                radius_min_pixels=3,
                radius_max_pixels=200,
                # line_width_min_pixels=1,
                get_position=['lng', 'lat'],
                get_fill_color=color,
            ),
        ]
    ))

def custom_dc(conn, airports):
    new_list = {}
    i = 0
    json = []

    #since some country has hundreds of airports, which would cause 414 error
    #separate the request to small pieces
    if len(airports) < 20:
        for i in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
        json.extend(conn.runInstalledQuery('degreeCentrality',
                                           params=new_list, timeout=16000)[0]['@@topScores'])
    else:
        for index in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
            i += 1
            if (index % 20 == 0 and i != 0):
                json.extend(conn.runInstalledQuery(
                    'degreeCentrality', params=new_list, timeout=16000)[0]['@@topScores'])
                new_list = {}
                i = 0
    res = pd.DataFrame(json)
    return res

def custom_cc(conn, airports, maxHops):
    new_list = {}
    i = 0
    json = []

    #since some country has hundreds of airports, which would cause 414 error
    #separate the request to small pieces
    if len(airports) < 20:
        for i in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
        new_list['display'] = False
        new_list['maxHops'] = maxHops
        json.extend(conn.runInstalledQuery('custom_cc',
                                           params=new_list, timeout=16000)[0]['@@topScores'])
    else:
        for index in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
            i += 1
            if (index % 20 == 0 and i != 0):
                new_list['display'] = False
                new_list['maxHops'] = maxHops
                json.extend(conn.runInstalledQuery(
                    'custom_cc', params=new_list, timeout=16000)[0]['@@topScores'])
                new_list = {}
                i = 0

    res = pd.DataFrame(json)
    return res

def custom_bc(conn, airports, maxHops):
    new_list = {}
    i = 0
    json = []

    #since some country has hundreds of airports, which would cause 414 error
    #separate the request to small pieces
    if len(airports) < 20:
        for i in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
        new_list['maxHops'] = maxHops
        json.extend(conn.runInstalledQuery('custom_bc',
                                           params=new_list, timeout=16000)[0]['Start'])
    else:
        for index in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
            i += 1
            if (index % 20 == 0 and i != 0):
                new_list['maxHops'] = maxHops
                json.extend(conn.runInstalledQuery(
                    'custom_bc', params=new_list, timeout=16000)[0]['Start'])
                new_list = {}
                i = 0

    res = pd.DataFrame(json)
    data = pd.DataFrame([], columns=['Vertex_ID', 'name', 'lat', 'lng', 'score'])
    for i in range(len(res)):
        id = res.loc[i,'attributes']['Start.id']
        name = res.loc[i,'attributes']['Start.name']
        lat = res.loc[i,'attributes']['Start.latitude']
        lng = res.loc[i,'attributes']['Start.longitude']
        score = res.loc[i,'attributes']['Start.@cent']
        data.loc[i] = [id, name, lat, lng, score]
    return data

def custom_pr(conn, airports):
    new_list = {}
    i = 0
    json = []

    #since some country has hundreds of airports, which would cause 414 error
    #separate the request to small pieces
    if len(airports) < 20:
        for i in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
        json.extend(conn.runInstalledQuery('custom_pr',
                                           params=new_list, timeout=16000)[0]['@@topScores'])
    else:
        for index in range(len(airports)):
            new_list["source[{}]".format(i)] = airports.loc[i, 'Vertex_ID']
            new_list["source[{}].type".format(i)] = "Airport"
            i += 1
            if (index % 20 == 0 and i != 0):
                json.extend(conn.runInstalledQuery(
                    'custom_pr', params=new_list, timeout=16000)[0]['@@topScores'])
                new_list = {}
                i = 0

    res = pd.DataFrame(json)
    return res

def custom_overall_chart(dc, cc, bc, pr):
    # if (airports == "None"):
    #     return
    if len(dc) > 30:
        dc = dc.head(30)
        cc = cc.head(30)
        bc = bc.head(30)
        pr = pr.head(30)
    source = pd.DataFrame([], columns=['name', 'score', 'centrality'])
    idx = 0
    source, idx = combine_data(dc, idx, source, "degree centrality")
    source, idx = combine_data(cc, idx, source, "closeness centrality")
    source, idx = combine_data(bc, idx, source, "betweennes centrality")
    source, idx = combine_data(pr, idx, source, "page rank")
    with st.beta_expander('See raw data'):
        st.dataframe(source)
    st.write("")
    st.write('')
    st.altair_chart(set_chart(source))

def nearby_airport(conn, city, distance, maxHops):
    #get geo info from input city
    geolocator = Nominatim(user_agent="hackathon")
    location = geolocator.geocode(city)
    if not location:
        st.sidebar.error("City not found!")
        return
    lat = location.latitude
    lng = location.longitude
    params = {'lat':lat, 'lng': lng, 'distance':distance}

    #get nearby airports from 
    airports = conn.runInstalledQuery('calculateWeights', params=params, timeout=16000)
    airports = airports[0]['@@resultSet']
    if len(airports) == 0:
        st.sidebar.error('No airport nearby!')
        return
    airports = pd.DataFrame(airports)

    #get the centrality data
    dc = custom_dc(conn, airports)
    cc = custom_cc(conn, airports, maxHops)
    bc = custom_bc(conn, airports, maxHops)
    pr = custom_pr(conn, airports)

    #set map layout
    col1, col2 = st.beta_columns(2)
    col3, col4 = st.beta_columns(2)
    with col1:
        st.write('Degree Centrality')
        set_map(dc, color_dic.get('dc'))
    with col2:
        st.write('Closeness Centrality')
        set_map(cc, color_dic.get('cc'))
    with col3:
        st.write('Betweenness Centrality')
        set_map(bc, color_dic.get('bc'))
    with col4:
        st.write('Page Rank')
        set_map(pr, color_dic.get('pr'))

    #show the chart
    st.write("")
    st.write("")
    if len(dc) > 30:
        st.subheader("Centrality Values Overview(top 30)")
    else:
        st.subheader("Centrality Values Overview")
    custom_overall_chart(dc, cc, bc, pr)
    st.sidebar.text("City: \n" +  str(location))