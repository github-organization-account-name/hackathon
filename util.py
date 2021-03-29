import pandas as pd
import altair as alt
import math

#color define:
color_dic = {}
color_dic["dc"] = [228,87,86]
color_dic["cc"] = [245,133,24]
color_dic['bc'] = [76,120,168]
color_dic['pr'] = [114,183,178]

def set_score(data):
    data = data.sort_values(by=['score']).reset_index(drop=True)
    #normalization first
    min = data.loc[0, 'score']
    max = data.loc[len(data) - 1, 'score']
    if min <= 0:
        min = 0
    for i in range(len(data)):
        if data.loc[i, 'score'] <= 0:
            data.loc[i, 'score'] = 0
        else:
            x = data.loc[i, 'score']
            if max == min:
                data.loc[i, 'score'] = x / max * 10000
            else:
                data.loc[i, 'score'] = ((x - min) / (max - min)) * len(data)*100
    return data

def set_chart(data):
    bars = alt.Chart(data).mark_bar().encode(
        x = alt.X('sum(score):Q', stack='zero'),
        y = alt.Y('name:N', sort='-x'),
        color = alt.Color('centrality'),
        tooltip='score',
    ).properties(
        width=1000
    )
    return bars

def combine_data(source, idx, res, cent_name):
    for i in range(len(source)):
        name = source.loc[i, 'name']
        score = source.loc[i, 'score']
        centrality = cent_name
        res.loc[idx] = [name, score, centrality]
        idx += 1
    return res, idx
