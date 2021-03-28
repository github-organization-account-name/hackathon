import streamlit as st
import streamlit.components.v1 as components
import pyTigerGraphBeta as tg
from map import *
from centrality import *
from customCentrality import *
import numpy as np
from weighted import *
from unweight import *
import graphistry
import streamlit.components.v1 as components


#set layout as wide 
st.set_page_config(layout="wide")

#connect with tigergraph database 
conn = tg.TigerGraphConnection(host="https://graph.i.tgcloud.io", graphname="MyGraph",
                               username="tigergraph", password="123456", apiToken="r633lnmiia9sad9dd3u1pl79787ploqu")
#set debug mode as true
# conn.debug = True

#connect with graphistry
graphistry.register(api=3, protocol="https", server="hub.graphistry.com", username="qi2", password="Chico1053432784")

#read country from csv file
country = pd.read_csv('./country.csv', usecols=['0'])
country = country.drop([1]).reset_index(drop=True)

st.sidebar.title('Choose your favorite Graph')
sidebar = st.sidebar
graph_option = sidebar.selectbox(
    'select graph', ('Data overview', 'Shortest path', 'Centrality'))


# plotly set lat & lon range
def setCoordinateRange(df):
    if df.max() - df.min() < 20:
        return [df.min() - 20, df.max() + 20]
    return [df.min(), df.max()]

@st.cache
def data_overview():
    result = conn.runInstalledQuery('data_overview', timeout = 16000)
    data = pd.DataFrame(result[0]['@@edgeList'])
    g = graphistry.edges(data, 'from_id', 'to_id')
    graph = g.plot(render=False)
    return graph

if graph_option == 'Data overview':
    st.title('Have a look of the data')
    graph = data_overview()
    components.iframe(graph, width=1200, height=600)

# shortest path option
elif graph_option == "Shortest path":
    path = st.sidebar.radio('',['shortest path unweight', 'shortest path weighted'], index = 0)
    if path == 'shortest path weighted':
        # country_opt = sidebar.selectbox('Choose a country', country)
        st.title("Shortest path with weighted")
        # st.multiselect('choose airports', country)
        # col1, col2, col3 = st.beta_columns((2,2,1))
        # with col1:
        #     start = st.text_input('from')
        # with col2:
        #     to = st.text_input('to')
        # with col3:
        #     st.write("")
        #     st.write("")
        #     st.button("search")
        # if not start or not to:
        #     st.error("Please input airports")
        # else:
        weighted_path(conn, country)
    elif path == 'shortest path unweight':
        shortest_path_unweighted(conn)
    

# centrality measurement
elif graph_option == "Centrality":
    #sidebar
    country_opt = sidebar.selectbox('Choose a country', country)
    #centrality page
    st.title("Centrality")
    maxHops = st.sidebar.slider('Max hops', 1, 10, 3)
    check = st.sidebar.checkbox(
            'Want to check out your nearby airport centrality?', key="check")
        
    if check:
        city = st.sidebar.text_input('Type a city you want to check with', "")
        miles = st.sidebar.slider("Within miles", 50, 250, 100)
        if city != '':
            st.subheader("Differenct Centrality Value on the Map")
            text = nearby_airport(conn, city, miles, maxHops)
        st.write("Notice: To make the data more visible. \n The printed centrality = normalize(origin centrality) * number of displayed airports")
    else:
        if country_opt != "None":
            st.subheader("Differenct Centrality Value on the Map")
            getCountryCentrality(conn, country_opt, maxHops)
            st.write("Notice: To make the data more visible. \n The printed centrality = normalize(origin centrality) * number of displayed airports")
