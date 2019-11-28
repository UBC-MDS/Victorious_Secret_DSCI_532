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
df = pd.read_csv("https://raw.github.ubc.ca/MDS-2019-20/DSCI_531_lab4_anas017/master/data/Police_Department_Incidents_-_Previous_Year__2016_.csv?token=AAAHQ0dLxUd74i7Zhzh1SJ_UuOaFVI3_ks5d5dT3wA%3D%3D")


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

def make_plot(data=df_t4):
    chart_1 = alt.Chart(data).mark_circle(size=3, opacity = 0.8).encode(
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

    chart_2 = alt.Chart(data).mark_bar().encode(
        x=alt.X('PdDistrict:N', axis=None, title="District"),
        y=alt.Y('count()', title="Count of reports"),
        color=alt.Color('PdDistrict:N', legend=alt.Legend(title="District")),
        tooltip=['PdDistrict', 'count()']
    ).properties(
        width=450,
        height=500
    )

    # A dropdown filter
    crimes_dropdown = alt.binding_select(options=list(df_t4['Category'].unique()))
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
        id = 'drop_selection_crime',
        options=[{'label': i, 'value': i} for i in df_t4['Category'].unique()
        ],
    style={'height': '15px',
           'width': '300px'},
    value=df_t4['Category'].unique(),
    multi=True
    ),

])

@app.callback(
    Output('plot', 'srcDoc'),
    [Input('drop_selection_crime', 'value')])
def update_plot(value_smtn):

    updated_plot = make_plot(df_t4[df_t4['Category'].isin(value_smtn)]).to_html()
    return updated_plot    

if __name__ == '__main__':
    app.run_server(debug=True)