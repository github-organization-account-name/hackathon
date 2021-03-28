import pyTigerGraphBeta as tg
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import json
import plotly.express as px
from util import *
import streamlit.components.v1 as components


def set_map(source, pre):
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.data_utils.compute_view(pre[['lng', 'lat']]),
        tooltip={"text": "{from_name}\nto\n{to_name}"},
        layers=[
            pdk.Layer(
                "GreatCircleLayer",
                source,
                pickable=True,
                get_stroke_width=12,
                get_source_position=["from.lng", 'from.lat'],
                get_target_position=["to.lng", 'to.lat'],
                get_source_color=[64, 255, 0],
                get_target_color=[0, 128, 200],
                auto_highlight=True,
                line_width_min_pixels=2,
                width_min_pixals=10,
                get_width=10,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=pre,
                pickable=True,
                opacity=0.4,
                stroked=True,
                filled=True,
                radius_scale=6,
                get_radius=10,
                radius_min_pixels=7,
                radius_max_pixels=200,
                get_position=['lng', 'lat'],
                get_fill_color=[255,140,0],
            )
        ]
    ))


def weighted_path(conn, country):
    country = country.drop([0]).reset_index(drop=True)
    country = country.to_string(index=False)
    _map_compoent = components.declare_component("United States", url="http://localhost:3000")
    component_value=_map_compoent(name="weighted", key=country)

    # params = {"source": start, 'terminal': to}
    # json = conn.runInstalledQuery(
    #     'shortest_path_weighted', params=params, timeout=64000)
    # data = json[0]['total'][0]['attributes']
    # distance = data['total.@minPath.top().dist']
    # st.text('Total distance: ' + str(distance) + ' miles')
    # path = data['total.@path']
    # paths = pd.DataFrame(path)
    # print(paths)
    # source = pd.DataFrame([], columns=['from', 'to'])
    # for i in range(len(paths) - 1):
    #     start = paths.loc[i].to_dict()
    #     to = paths.loc[i+1].to_dict()
    #     source.loc[i] = [start, to]
    # print(source)
    # source["from_name"] = source["from"].apply(lambda f: f["name"])
    # source["to_name"] = source["to"].apply(lambda t: t["name"])
    # set_map(source, paths)
