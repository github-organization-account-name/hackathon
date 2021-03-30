import streamlit as st
import pandas as pd
import pyTigerGraph as tg
import plotly.graph_objects as go
import plotly.express as px
import folium
from folium import plugins
from streamlit_folium import folium_static



def shortest_path_unweighted(conn):
    st.title('Find Shortest Path In Unweighted Graph')

    # multi select box
    # json = conn.runInstalledQuery('getAllAirports', timeout=16000)
    # infos = open('infos.csv', 'w', encoding="utf-8")  # will clear all the contents
    # info = json[0]["Result"]
    # for i in info:
    #     infos.write(i['v_id'] + '\n')  # write in header row
    # infos.close()

    # res = json[0]["Result"]
    # infos = []
    # for r in res:
    #     temp = r["v_id"] + ", " + r["attributes"]["city"] + ", " + r["attributes"]["country"]
    #     infos.append(r['v_id'])
    #     infos.append(temp)

    infos = open('infos.csv', encoding="utf-8")
    options = st.multiselect(
        'Select your STOPS',
        pd.DataFrame(infos)
    )
    infos.close()

    world_map = folium.Map(zoom_start=12)
    if len(options) == 0 or len(options) > 2:
        st.error("please select two stops")
    elif len(options) == 1:
        st.error("please select another stop")

        start = options[0]
        params = {'airId': start.rstrip()}
        json = conn.runInstalledQuery('get_airportInfo_by_id', params=params, timeout=16000)
        airInfo = json[0]["Air"][0]["attributes"]
        airName = airInfo["name"]
        latitude = airInfo["latitude"]
        longitude = airInfo["longitude"]

        # add circles into map
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=15,
            popup="START:\n" + airName,
            color="#3186cc",
            fill=True,
            fill_opacity=0.3,
            fill_color="#3186cc"
        ).add_to(world_map)
        folium_static(world_map)

    elif len(options) == 2:
        start = options[0].split()
        termination = options[1].split()
        st.subheader("Your path is from " + start[0] + " to " + termination[0])

        params = {'display': False, 'S': start[0], "S.type": "Airport", "T": termination[0], "T.type": "Airport", "maxDepth": 50}
        json = conn.runInstalledQuery('shortest_nowt_start_end', params=params, timeout=16000)

        result = json[0].get("Result_1")
        result = result[0]["attributes"]["Result_1.@pathResult_1"]

        if len(result) == 0:
            st.error("No Path Found")
            start = options[0]
            end = options[1]

            params_1 = {'airId': start.rstrip()}
            params_2 = {'airId': end.rstrip()}
            json_1 = conn.runInstalledQuery('get_airportInfo_by_id', params=params_1, timeout=16000)
            json_2 = conn.runInstalledQuery('get_airportInfo_by_id', params=params_2, timeout=16000)

            airInfo_1 = json_1[0]["Air"][0]["attributes"]
            airName_1 = airInfo_1["name"]
            latitude_1 = airInfo_1["latitude"]
            longitude_1 = airInfo_1["longitude"]

            airInfo_2 = json_2[0]["Air"][0]["attributes"]
            airName_2 = airInfo_2["name"]
            latitude_2 = airInfo_2["latitude"]
            longitude_2 = airInfo_2["longitude"]

            # add circles into map
            folium.CircleMarker(
                location=[latitude_1, longitude_1],
                radius=15,
                popup="START:\n" + airName_1,
                color="#3186cc",
                fill=True,
                fill_opacity=0.3,
                fill_color="#3186cc"
            ).add_to(world_map)
            folium.CircleMarker(
                location=[latitude_2, longitude_2],
                radius=15,
                popup="END:\n" + airName_2,
                color="crimson",
                fill=True,
                fill_opacity=0.3,
                fill_color="crimson"
            ).add_to(world_map)
            folium_static(world_map)

        else:
            pathResults = result
            selectPath = st.selectbox(
                'Select your path',
                pathResults
            )
            airName = []  # names
            airId = []
            latitude = []
            longitude = []
            points = []
            st.write(selectPath)
            airports = selectPath.split("->")
            for airport in airports:
                params = {'airId': airport}
                json = conn.runInstalledQuery('get_airportInfo_by_id', params=params, timeout=16000)
                airInfo = json[0]["Air"][0]["attributes"]
                airName.append(airInfo["name"])
                airId.append(airInfo["id"])
                latitude.append(airInfo["latitude"])
                longitude.append(airInfo["longitude"])
                points.append([airInfo["latitude"], airInfo["longitude"]])

            st.write("Stops Info: ")
            df = pd.DataFrame({
                'airports shortcut': airId,
                'stop airports': airName,
                'lat': latitude,
                'lon': longitude
            })
            st.write(df)

            # add edges into map
            world_map.add_child(folium.PolyLine(
                locations=points,
                weight=3,
                color='grey'
            ))
            # add circles into map
            folium.CircleMarker(
                location=points[0],
                radius=15,
                popup="START",
                color="#3186cc",
                fill=True,
                fill_opacity=0.3,
                fill_color="#3186cc"
            ).add_to(world_map)
            folium.CircleMarker(
                location=points[len(points) - 1],
                radius=15,
                popup="END",
                color="#008000",
                fill=True,
                fill_opacity=0.3,
                fill_color="#008000"
            ).add_to(world_map)

            for i in range(1, len(points) - 1):
                folium.Circle(
                    radius=10000,
                    location=points[i],
                    popup=airName[i],
                    color="crimson",
                    fill=False,
                ).add_to(world_map)

            # draw the map
            folium_static(world_map)
