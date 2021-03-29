import pyTigerGraphBeta as tg
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import json
import plotly.express as px
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
                opacity=0.6,
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


def degreeCentrality(conn, country):

    if (country == "None"):
        return
    params = "country=" + country
    # conn.debug = True
    res = conn.runInstalledQuery('dc_by_country', params=params, timeout=16000)
    res = pd.DataFrame(res[0]["@@topScores"])
    return res


def ClosenessCentrality(conn, country, maxHops):
    if (country == "None"):
        return
    # maxHops = st.slider('Max hops', 1, 10, 3)
    params = "country=" + country + "&" + "maxHops=" + str(maxHops) + "&" + "display=" + str(False)
    res = conn.runInstalledQuery('cc_by_country', params=params, timeout=16000)
    res = res[0]["@@topScores"]
    res = pd.DataFrame(res)
    return res

def betweennessCentrality(conn, country, maxHops):
    if (country == "None"):
        return
    # maxHops = st.slider('Max hops', 1, 10, 3)
    params = "country=" + country + "&" + "maxHops=" + str(maxHops)
    res = conn.runInstalledQuery('betweenness_cent', params=params, timeout=16000)
    res = res[0]['Start']
    data = pd.DataFrame([], columns=['Vertex_ID', 'name', 'lat', 'lng', 'score'])
    for i in range(len(res)):
        id = res[i]['attributes']['Start.id']
        name = res[i]['attributes']['Start.name']
        lat = res[i]['attributes']['Start.latitude']
        lng = res[i]['attributes']['Start.longitude']
        score = res[i]['attributes']['Start.@cent']
        data.loc[i] = [id, name, lat, lng, score]
    return data

def PageRank(conn, country):
    if (country == "None"):
        return
    # maxHops = st.slider('Max hops', 1, 10, 3)
    params = "country=" + country
    res = conn.runInstalledQuery('pageRank_by_country', params=params, timeout=16000)
    res = pd.DataFrame(res[0]['@@topScores'])
    return res

def set_degreeCentrality_map(conn, data, maxHops):
    if (data == "None"):
        return
    res = degreeCentrality(conn, data)
    set_map(res, color_dic.get('dc'))

def set_closenessCentrality_map(conn, data, maxHops):
    if (data == "None"):
        return
    res = ClosenessCentrality(conn, data, maxHops)
    set_map(res, color_dic.get('cc'))

def set_betweennessCentrality_map(conn, data, maxHops):
    if (data == "None"):
        return
    res = betweennessCentrality(conn, data, maxHops)
    set_map(res, color_dic.get('bc'))

def set_pageRank_map(conn, data, maxHops):
    if (data == "None"):
        return
    res = PageRank(conn, data, maxHops)
    set_map(res, color_dic.get('pr'))


def overall_chart(bc, cc, dc, pr):
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

def getCountryCentrality(conn, data, maxHops):
    if (data == "None"):
        return
    #get the centrality data
    dc = degreeCentrality(conn, data)
    cc = ClosenessCentrality(conn, data, maxHops)
    bc = betweennessCentrality(conn, data, maxHops)
    pr = PageRank(conn, data)

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
    
    print(bc)
    print(cc)
    print(dc)
    print(pr)

    st.write("")
    st.write("")
    if len(dc) > 30:
        st.subheader("Centrality Values Overview(top 30)")
    else:
        st.subheader("Centrality Values Overview")
    overall_chart(bc, cc, dc, pr)
