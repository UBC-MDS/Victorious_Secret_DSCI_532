import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
import vega_datasets
alt.data_transformers.enable('default')
alt.data_transformers.disable_max_rows()
app = dash.Dash(__name__, assets_folder='assets')
server = app.server
app.title = 'Dash app with pure Altair HTML'
df = pd.read_csv("https://raw.github.ubc.ca/MDS-2019-20/DSCI_531_lab4_anas017/master/data/Police_Department_Incidents_-_Previous_Year__2016_.csv?token=AAAHQ0dLxUd74i7Zhzh1SJ_UuOaFVI3_ks5d5dT3wA%3D%3D")
df['datetime'] = pd.to_datetime(df[["Date","Time"]].apply(lambda x: x[0].split()[0] +" "+x[1], axis=1), format="%m/%d/%Y %H:%M")
df['hour'] = df['datetime'].dt.hour
df.dropna(inplace=True)
top_4_crimes = df['Category'].value_counts()[:6].index.to_list()
top_4_crimes
top_4_crimes.remove("NON-CRIMINAL")
top_4_crimes.remove("OTHER OFFENSES")
# top 4 crimes df subset
df_t4 = df[df["Category"].isin(top_4_crimes)].copy()

def make_plot(df_new=df_t4):
    
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # making the slider
    slider = alt.binding_range(min = 0, max = 23, step = 1)
    select_hour = alt.selection_single(name='hour', fields = ['hour'],
                                    bind = slider, init={'hour': 0})

    #begin of my code
    typeDict = {'ASSAULT':'quantitative',
                'VANDALISM':'quantitative',
                'LARCENY/THEFT':'quantitative',
                'VEHICLE THEFT':'quantitative'
    }
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

    

app.layout = html.Div([
    ### ADD CONTENT HERE like: html.H1('text'),
    html.Iframe(
        sandbox = "allow-scripts",
        id = "plot",
        height = "500",
        width = "700",
        style = {"border-width": "5px"},
        srcDoc = make_plot().to_html()
        ),
    #my
    dcc.Dropdown(
        id='dd-chart',
        options=[
            {'label': i, 'value': i} for i in ['ASSAULT','VANDALISM','LARCENY/THEFT','VEHICLE THEFT']
        ],
        value='ASSAULT',
        multi=True,
        style=dict(width='45%',
              verticalAlign="middle"
              )
        ),
])
#my
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value')]
    )

#def update_plot(xaxis_column_name):

    #updated_plot = make_plot(xaxis_column_name).to_html()
#    updated_plot = make_plot(xaxis_column_name).to_html()

#    return updated_plot

def update_df(chosen):
    new_df = df_t4[(df_t4["Category"].isin(chosen))]
    updated_plot = make_plot(new_df).to_html()

    return updated_plot
    
#end
if __name__ == '__main__':
    app.run_server(debug=True)
