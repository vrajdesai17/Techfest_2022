import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go 

# df = pd.read_csv('Sample_driver.csv')

st.set_page_config(
    page_title = "Real-Time Fleet Risk Dashboard",
    page_icon = '❤️',
    layout = 'wide',   
)

st.title('Fleet Risk Dashboard')
dsp_data = ['DSP 1', 'DSP 2', 'DSP 3']

dsp_filter = st.selectbox("Select DSP", pd.unique(dsp_data))



if dsp_filter=='DSP 1':
    df = pd.read_csv('./DSP1/driver_dsp1.csv')
elif dsp_filter == 'DSP 2':
    df = pd.read_csv('./DSP2/driver_dsp2.csv')

df2 = df[['RANK','DRIVER_NAME','RISK_SCORE_2']]
df2 = df2.sort_values(by='RANK',ascending=True).head(10)
df2 = df2.set_index('DRIVER_NAME')
avg_risk = df['RISK_AVERAGE_2'][0]


st.markdown('### Leader Board')

cell_hover = {
    "selector": "td:hover",
    "props": [("background-color", "#063970")]
}
index_names = {
    "selector": "th:not(.index_name)",
    "props": "font-style: italic; color: darkgrey; font-weight:strong; text-align:center; text-decoration: bold",
}
# headers = {
#     "selector": "th:not(.index_name)",
#     "props": "background-color: #800000; color: white;"
# }
headers = {
    "selector": "th:not(.index_name)",
    "props": "background-color: #1e81b0; color: white; text-align: center"
}
# properties = {"border": "1px solid black", "width": "65px", "text-align": "center"}
properties = {"border": "1px solid #1e81b0", "text-align": "center"}

st.table(df2.style.format(precision=0).set_table_styles([cell_hover, index_names,headers]).set_properties(**properties))
# st.table(df2.style.hide(axis="index").format(precision=2).set_table_styles([cell_hover, index_names]))
# st.table(df.style.hide() )
#Filter
# avg_risk = df['RISK_AVERAGE'][0]

job_filter = st.selectbox("Select Driver Name", pd.unique(df['DRIVER_NAME']))

placeholder = st.empty()

df = df[df['DRIVER_NAME']==job_filter]

# for seconds in range(200):


# df['RISK_SCORE_NEW'] = df['RISK_SCORE'] * np.random.choice(range(1,3))
# avg_risk = (df['RISK_AVERAGE'][0])
# dri_name = df['DRIVER_NAME']
risk_score = df['RISK_SCORE_2']
rank = df['RANK']
with placeholder.container():
    sp,kpi1,kpi2,kpi3 = st.columns((2,3,3,3))

    # kpi1.metric(label='Name ',value= dri_name)
    kpi1.metric(label='DSP Average Safety Score',value= round(avg_risk))
    kpi2.metric(label='Driver Safety Score',value= int(round(risk_score)),delta= round(int(risk_score) - (avg_risk)))
    kpi3.metric(label='Rank',value= rank)

    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        # st.markdown('<div style="text-align: center; text-decoration: bold">Average Safety Meter</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = float(avg_risk),
            # value = 1002,
            domain = {'x': [0,1], 'y': [0,1]},
            title = {'text': 'DSP Average Safety Score'},
            gauge= {'axis': {'range': [None, 100]},'bar': {'color':'green'}})) 
        st.write(fig)

    # fig_col1, fig_col2, fig_col3, fig_col4 = st.columns(4)
    with fig_col2:
        # st.markdown('<div style="text-align: center; text-decoration: bold">Driver Safety Score</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = float(df['RISK_SCORE_2']),
            # value = 1002,
            domain = {'x': [0,1], 'y': [0,1]},
            title = {'text': 'Driver Safety Score'},
            delta= {'reference': avg_risk},
            gauge= {'axis': {'range': [None, 100]},'bar': {'color':'green'}})) 
        st.write(fig)
    
    source = pd.DataFrame({
        'Categories' : ['ACCELERATION','BRAKING','CORNERING','SPEEDING','SEATBELT','DISTRACTION','NUMBER_OF_TICKETS_RECEIVED'],
        'Values' : [int(df['ACCELERATION']),int(df['BRAKING']),int(df['CORNERING']),int(df['SPEEDING']),int(df['SEATBELT']),int(df['DISTRACTION']),int(df['NUMBER_OF_TICKETS_RECEIVED']),]
    })
    # source = source.set_index("Categories")
    # source.encode(
    #     y = 'Values',
    #     x = 'Categories',
    # )
    # bar_col1, bar_col2, bar_col3 = st.columns(3)
    # with bar_col2:
    # st.bar_chart(source,width=150,height=750)
    sp,c1,c2,c3 = st.columns((3,3,3,3))
    with c1:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=source['Categories'], y = source['Values'], marker_color='#1e81b0',hoverlabel= None))
        # st.plotly_chart(fig_bar)
        fig_bar.update_layout(
        title='Risk Parameters',
        xaxis=dict(title = 'Metrics'),
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Values',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ))
        st.write(fig_bar)
    st.markdown('### Detailed view')
    st.table(df.set_index('DRIVER_NAME').style.format(precision=2).set_table_styles([cell_hover, index_names, headers]).set_properties(**properties))
    
    from urllib.request import urlopen
    import json
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    # import pandas as pd
    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    #                 dtype={"fips": str})

    # import plotly.express as px
    # df3 = pd.read_csv('route.csv',dtype={'GEOPOINTS':str})
    # fig_map = px.choropleth_mapbox(df3, geojson=counties, locations='GEOPOINTS',
    #                         color_continuous_scale="Viridis",
    #                         range_color=(0, 12),
    #                         mapbox_style="carto-positron",
    #                         zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
    #                         opacity=0.5,
    #                         labels={'unemp':'unemployment rate'}
    #                         )
    # fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # st.write(fig_map)
    
    time.sleep(0.5)