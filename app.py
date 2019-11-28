import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
import vega_datasets
import os

wd = os.getcwd()

alt.data_transformers.enable('default')
alt.data_transformers.disable_max_rows()
app = dash.Dash(__name__, assets_folder='assets')
server = app.server
app.title = 'Dash app with pure Altair HTML'

df = pd.read_csv('data/Police_Department_Incidents_-_Previous_Year__2016_.csv')

# df = pd.read_csv("https://raw.github.ubc.ca/MDS-2019-20/DSCI_531_lab4_anas017/master/data/Police_Department_Incidents_-_Previous_Year__2016_.csv?token=AAAHQ0dLxUd74i7Zhzh1SJ_UuOaFVI3_ks5d5dT3wA%3D%3D")
df['datetime'] = pd.to_datetime(df[["Date","Time"]].apply(lambda x: x[0].split()[0] +" "+x[1], axis=1), format="%m/%d/%Y %H:%M")
df['hour'] = df['datetime'].dt.hour
df.dropna(inplace=True)
top_4_crimes = df['Category'].value_counts()[:6].index.to_list()
top_4_crimes
top_4_crimes.remove("NON-CRIMINAL")
top_4_crimes.remove("OTHER OFFENSES")
# top 4 crimes df subset
df_t4 = df[df["Category"].isin(top_4_crimes)].copy()

def make_plot_top(df_new=df_t4):
    
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # making the slider
    slider = alt.binding_range(min = 0, max = 23, step = 1)
    select_hour = alt.selection_single(name='hour', fields = ['hour'],
                                    bind = slider, init={'hour': 0})

    #begin of my code
    # typeDict = {'ASSAULT':'quantitative',
    #             'VANDALISM':'quantitative',
    #             'LARCENY/THEFT':'quantitative',
    #             'VEHICLE THEFT':'quantitative'
    # }
    # end
    
    chart = alt.Chart(df_new).mark_bar(size=30).encode(
        x=alt.X('Category',type='nominal', title='Category'),
        y=alt.Y('count()', title = "Count" , scale = alt.Scale(domain = (0,3300))),
        tooltip='count()'
    ).properties(
        title = "Per hour crime occurrences for the top 4 crimes",
        width=600,
        height = 400
    ).add_selection(
        select_hour
    ).transform_filter(
        select_hour
    )
    return chart

def make_plot_bot(data=df_t4):
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
    crimes_dropdown = alt.binding_select(options=list(data['Category'].unique()))
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
    dcc.Dropdown(
        id = 'drop_selection_crime',
        options=[{'label': i, 'value': i} for i in df_t4['Category'].unique()
        ],
        style={'height': '15px',
               'width': '300px'},
        value=df_t4['Category'].unique(),
        multi=True
        ),
    
    html.Iframe(
        sandbox = "allow-scripts",
        id = "plot_top",
        height = "500",
        width = "700",
        style = {"border-width": "5px"},
        srcDoc = make_plot_top().to_html()
        ),
    
    html.Iframe(
        sandbox='allow-scripts',
        id='plot_bot',
        height='500',
        width='1200',
        style={'border-width': '5px'},
        srcDoc= make_plot_bot().to_html()
        ),


])
#my
@app.callback([dash.dependencies.Output('plot_top', 'srcDoc'),
    dash.dependencies.Output('plot_bot', 'srcDoc')],
    [dash.dependencies.Input('drop_selection_crime', 'value')]
    )
def update_df(chosen):
    new_df = df_t4[(df_t4["Category"].isin(chosen))]
    updated_plot_top = make_plot_top(new_df).to_html()
    updated_plot_bottom = make_plot_bot(new_df).to_html()

    return updated_plot_top, updated_plot_bottom

if __name__ == '__main__':
    app.run_server(debug=True)
