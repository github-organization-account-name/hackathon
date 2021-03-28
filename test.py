import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np
import pyTigerGraph as tg
import pandas as pd
import os
from map import *
import pydeck as pdk
import math


# st.title('test')
# conn = tg.TigerGraphConnection(host="https://graph.i.tgcloud.io", graphname="MyGraph",
#                                username="tigergraph", password="123456", apiToken="r633lnmiia9sad9dd3u1pl79787ploqu")
# country = pd.read_csv('./country.csv', usecols=['0'])

# data = load_coordinate("United States", conn)

_map_compoent = components.declare_component("United States", url="http://localhost:3000")

def map_component(name, key):
    component_value=_map_compoent(name=name, key=key)


st.subheader("Component with constant args")
res = map_component("map", "United States")
print(res)

# _RELEASE = False



# if not _RELEASE:
#     _component_func = components.declare_component(      
#         "my_component",
#         url="http://localhost:3000",
#     )
# else:
#     parent_dir = os.path.dirname(os.path.abspath(__file__))
#     build_dir = os.path.join(parent_dir, "frontend/build")
#     _component_func = components.declare_component("my_component", path=build_dir)


# def my_component(name, key=None):
#     component_value = _component_func(name=name, key=key, default=0)
#     return component_value


# if not _RELEASE:
#     import streamlit as st


#     st.subheader("Component with constant args")
#     # data = data.to_json(orient="records")
#     num_clicks = my_component("World"
#     , key="China"
#     )
#     print(num_clicks)
#     st.markdown("You've clicked %s times!" % int(num_clicks))

#     # st.markdown("---")
#     # st.subheader("Component with variable args")

#     name_input = st.text_input("Enter a name", value="Streamlit")
#     num_clicks = my_component(name_input, key="foo")
#     st.markdown("You've clicked %s times!" % int(num_clicks))

# def degreeCentrality(conn, data):
#     id_list = data['id'].values.tolist()
#     new_list = {}
#     i = 0
#     json = []

#     # since some country has hundreds of airports, which would cause 414 error
#     # separate the request to small pieces
#     if len(id_list) < 20:
#         for i in range(len(id_list)):
#             new_list["source[{}]".format(i)] = id_list[i]
#             new_list["source[{}].type".format(i)] = "Airport"
#         json.extend(conn.runInstalledQuery('degreeCentrality',
#                                            params=new_list, timeout=16000)[0]['@@topScores'])
#     else:
#         for element in id_list:
#             new_list["source[{}]".format(i)] = element
#             new_list["source[{}].type".format(i)] = "Airport"
#             i += 1
#             if (i % 20 == 0 and i != 0):
#                 json.extend(conn.runInstalledQuery(
#                     'degreeCentrality', params=new_list, timeout=16000)[0]['@@topScores'])
#                 new_list = {}
#                 i = 0

#     res = json
#     points = pd.DataFrame([], columns=['id', 'lat', 'lng', 'score'])
#     for i in range(len(res)):
#         id = res[i]['Vertex_ID']
#         score = int(res[i]['score']) * 20
#         airport = conn.runInstalledQuery('getAirportById', params="id=" + id)
#         airport = airport[0]['result'][0]['attributes']
#         lat = airport['latitude']
#         lon = airport['longitude']
#         points.loc[i] = [id, lat, lon, score]

#     set_map(points)

# col1, col2 = st.set_page_config(layout='wide')

# DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json"
# df = pd.read_json(DATA_URL)
# df["exits_radius"] = df["exits"].apply(lambda exits_count: math.sqrt(exits_count))
# print(df)

# view = pdk.data_utils.compute_view(df["coordinates"])
# view.pitch = 75
# view.bearing = 60

# st.write(pdk.Deck(
#     map_style="mapbox://styles/mapbox/light-v9",
#     initial_view_state=view,
#     map_provider="mapbox",
#     layers=[
#         pdk.Layer(
#             "ScatterplotLayer",
#             df,
#             pickable=True,
#             opacity=0.8,
#             stroked=True,
#             filled=True,
#             radius_scale=6,
#             radius_min_pixels=1,
#             radius_max_pixels=100,
#             line_width_min_pixels=1,
#             get_position="coordinates",
#             get_radius="exits_radius",
#             get_fill_color=[255, 140, 0],
#             get_line_color=[0, 0, 0],
#         )
#     ]
# ))

# import altair as alt

# st.vega_lite_chart(bars + text)

# import streamlit as st
# import pandas as pd
# import altair as alt
# from streamlit_vega_lite import altair_component
# from vega_datasets import data
# from util import *

# print(type(color_dic))

# source=data.barley()
# print(source)

# st.title("Penguin Data Explorer 🐧")

# st.write("Hover over the scatterplot to reveal details about a penguin. The code for this demo is at https://github.com/domoritz/streamlit-vega-lite-demo.")

# @st.cache
# def load(url):
#     return  pd.read_json(url)

# df = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")

# if st.checkbox("Show Raw Data"):
#     st.write(df)

# @st.cache
# def make_altair_scatterplot():
#     bars = alt.Chart(source).mark_bar().encode(
#         x=alt.X('sum(yield):Q', stack='zero'),
#         y=alt.Y('variety:N'),
#         color=alt.Color('site')
#     )

#     text = alt.Chart(source).mark_text(dx=-15, dy=3, color='white').encode(
#         x=alt.X('sum(yield):Q', stack='zero'),
#         y=alt.Y('variety:N'),
#         detail='site:N',
#         text=alt.Text('sum(yield):Q', format='.1f')
#     )
#     return bars + text



# selection = altair_component(make_altair_scatterplot())

# if "_vgsid_" in selection:
#     # the ids start at 1
#     st.write(selection)
# else:
#     st.info("Hover over the chart above to see details about the Penguin here.")

# GREAT_CIRCLE_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/flights.json"  # noqa

# df = pd.read_json(GREAT_CIRCLE_LAYER_DATA)
# print(type(df.loc[0, 'from']))

# # Use pandas to prepare data for tooltip
# df["from_name"] = df["from"].apply(lambda f: f["name"])
# df["to_name"] = df["to"].apply(lambda t: t["name"])

# # Define a layer to display on a map
# layer = pdk.Layer(
#     "GreatCircleLayer",
#     df,
#     pickable=True,
#     get_stroke_width=12,
#     get_source_position="from.coordinates",
#     get_target_position="to.coordinates",
#     get_source_color=[64, 255, 0],
#     get_target_color=[0, 128, 200],
#     auto_highlight=True,
# )

# # Set the viewport location
# view_state = pdk.ViewState(latitude=50, longitude=-40, zoom=1, bearing=0, pitch=0)

# # Render
# r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{from_name}\nto\n{to_name}"},)
# r.picking_radius = 10
# st.pydeck_chart(r)