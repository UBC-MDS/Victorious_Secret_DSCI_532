import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import altair as alt
import pandas as pd
import numpy as np
from pandas_datareader import data as web
from datetime import datetime as dt

alt.data_transformers.enable('default')
alt.data_transformers.disable_max_rows()

# load in the data
df = pd.read_csv('data/Police_Department_Incidents_-_Previous_Year__2016_.csv', sep=',')


app = dash.Dash(__name__, assets_folder='assets')
server = app.server


#Wrangling part
df['datetime'] = pd.to_datetime(df[["Date","Time"]].apply(lambda x: x[0].split()[0] +" "+x[1], axis=1), format="%m/%d/%Y %H:%M")
df['hour'] = df['datetime'].dt.hour
df.dropna(inplace=True)
top_4_crimes = df['Category'].value_counts()[:6].index.to_list()
top_4_crimes
top_4_crimes.remove("NON-CRIMINAL")
top_4_crimes.remove("OTHER OFFENSES")

# Top 4 crimes df subset
df_t4 = df[df["Category"].isin(top_4_crimes)].copy()

crimes = ['ASSAULT', 'LARCENY/THEFT', 'VEHICLE THEFT', 'VANDALISM']

def make_plot():
    chart_1 = alt.Chart(df_t4).mark_circle(size=3, opacity = 0.8).encode(
        longitude='X:Q',
        latitude='Y:Q',
        color = alt.Color('PdDistrict:N', legend = alt.Legend(title = "District")),
        tooltip = 'PdDistrict'
    ).project(
        type='albersUsa'
    ).properties(
        width=450,
        height=500
    )

    chart_2 = alt.Chart(df_t4).mark_bar().encode(
        x=alt.X('PdDistrict:N', axis=None, title="District"),
        y=alt.Y('count()', title="Count of reports"),
        color=alt.Color('PdDistrict:N', legend=alt.Legend(title="District")),
        tooltip=['PdDistrict', 'count()']
    ).properties(
        width=450,
        height=500
    )

    # A dropdown filter
    crimes_dropdown = alt.binding_select(options=crimes)
    crimes_select = alt.selection_single(fields=['Category'], bind=crimes_dropdown,
                                              name="Pick\ Crime")

    combine_chart = (chart_2 | chart_1)

    filter_crimes = combine_chart.add_selection(
        crimes_select
    ).transform_filter(
        crimes_select
    )

    return filter_crimes


app.layout = html.Div([
    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('San Francisco Crime Dashboard',  style={'backgroundColor':'#56D7DC'}),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='500',
        width='1200',
        style={'border-width': '5px'},
        srcDoc= make_plot().to_html()
        ),

    dcc.Dropdown(
        options=[
            {'label': 'Southern', 'value': df['PdDistrict'].unique()[0]},
            {'label': 'Bayview', 'value': df['PdDistrict'].unique()[1]},
            {'label': 'Tenderloin', 'value': df['PdDistrict'].unique()[2]},
            {'label': 'Mission', 'value': df['PdDistrict'].unique()[3]},
            {'label': 'Northern', 'value': df['PdDistrict'].unique()[4]},
            {'label': 'Taraval', 'value': df['PdDistrict'].unique()[5]},
            {'label': 'Ingleside', 'value': df['PdDistrict'].unique()[6]},
            {'label': 'Central', 'value': df['PdDistrict'].unique()[7]},
            {'label': 'Richmond', 'value': df['PdDistrict'].unique()[8]},
            {'label': 'Park', 'value': df['PdDistrict'].unique()[9]}


    ],
    style={'height': '15px',
           'width': '300px'},
    value=df['PdDistrict'].unique()[0],
    multi=True


    )

])




if __name__ == '__main__':
    app.run_server(debug=True)