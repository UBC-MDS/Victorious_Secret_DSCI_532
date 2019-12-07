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
app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.BOOTSTRAP])
# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501
server = app.server
app.title = 'Victorious Secret Crime Analyzer'

#df = pd.read_csv('data/Police_Department_Incidents_-_Previous_Year__2016_.csv')

df = pd.read_csv("data/Police_Department_Incidents_-_Previous_Year__2016_.csv")
df['datetime'] = pd.to_datetime(df[["Date","Time"]].apply(lambda x: x[0].split()[0] +" "+x[1], axis=1), format="%m/%d/%Y %H:%M")
df['hour'] = df['datetime'].dt.hour     
df.dropna(inplace=True)
top_4_crimes = df['Category'].value_counts()[:6].index.to_list()
top_4_crimes
top_4_crimes.remove("NON-CRIMINAL")
top_4_crimes.remove("OTHER OFFENSES")
# top 4 crimes df subset
df_t4 = df[df["Category"].isin(top_4_crimes)].copy()
def mds_special():
    font = "Arial"
    axisColor = "#000000"
    gridColor = "#DEDDDD"
    return {
        "config": {
            "title": {
                "fontSize": 24,
                "font": font,
                "anchor": "start", # equivalent of left-aligned.
                "fontColor": "#000000"
            },
            'view': {
                "height": 300, 
                "width": 400
            },
            "axisX": {
                "domain": True,
                #"domainColor": axisColor,
                "gridColor": gridColor,
                "domainWidth": 1,
                "grid": False,
                "labelFont": font,
                "labelFontSize": 12,
                "labelAngle": 0, 
                "tickColor": axisColor,
                "tickSize": 5, # default, including it just to show you can change it
                "titleFont": font,
                "titleFontSize": 16,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "X Axis Title (units)", 
            },
            "axisY": {
                "domain": False,
                "grid": True,
                "gridColor": gridColor,
                "gridWidth": 1,
                "labelFont": font,
                "labelFontSize": 14,
                "labelAngle": 0, 
                #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                "titleFont": font,
                "titleFontSize": 16,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "Y Axis Title (units)", 
                # titles are by default vertical left of axis so we need to hack this 
                #"titleAngle": 0, # horizontal
                #"titleY": -10, # move it up
                #"titleX": 18, # move it to the right so it aligns with the labels 
            },
        }
            }

# register the custom theme under a chosen name
alt.themes.register('mds_special', mds_special)

# enable the newly registered theme
alt.themes.enable('mds_special')
def make_plot_top(df_new=df_t4):
    
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # making the slider
    slider = alt.binding_range(min = 0, max = 23, step = 1)
    select_hour = alt.selection_single(name='select', fields = ['hour'],
                                    bind = slider, init={'hour': 19})
    
    chart = alt.Chart(df_new).mark_bar(size=30).encode(
        x=alt.X('Category',type='nominal', title='Category'),
        y=alt.Y('count()', title = "Count" , scale = alt.Scale(domain = (0,3300))),
        tooltip='count()'
    ).properties(
        title = "Hourly crime occurrences for selected crimes",
        width=500,
        height = 250
    ).add_selection(
        select_hour
    ).transform_filter(
        select_hour
    )
    chart.configure_title(fontSize=12)
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
        height=360,
        title= 'Crime Density Across Neighborhoods'
    )

    chart_2 = alt.Chart(data).mark_bar().encode(
        x=alt.X('PdDistrict:N',
                axis=None,
                title="Neighborhood District",
                sort=alt.EncodingSortField(field='PdDistrict', op='count', order='descending')),
        y=alt.Y('count()',
                title="Count of Reports"),
        color=alt.Color('PdDistrict:N', legend=alt.Legend(title="District")),
        tooltip=['PdDistrict', 'count()']
    ).properties(
        width=450,
        height=350,
        title='Distribution of Crime Reports Across Neighborhoods'
    )

    # A dropdown filter
    if data['Category'].unique().tolist():
        crimes_dropdown = alt.binding_select(options=list(data['Category'].unique()))
        crimes_select = alt.selection_single(fields=['Category'], bind=crimes_dropdown,
                                                name="Pick_Crime", 
                                                init = {'Category': data['Category'].unique()[0]})
    else:
        crimes_dropdown = alt.binding_select(options=list(data['Category'].unique()))
        crimes_select = alt.selection_single(fields=['Category'], bind=crimes_dropdown,
                                                name="Pick_Crime")
    chart_1.configure_title(fontSize=14)
    chart_2.configure_title(fontSize=14)
    combine_chart = (chart_2 | chart_1)

    filter_crimes = combine_chart.add_selection(
        crimes_select
    ).transform_filter(
        crimes_select
    ).configure_legend(
    orient='bottom'
    )

    return filter_crimes  

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("San Francisco Top 4 Crimes"),
                        html.P(
                            """\
                            When looking for a place to live or visit, one important factor that people will consider
                            is the safety of the neighborhood. This app aims to help people make decisions when considering their next trip or move to San Francisco, California
                            via visually exploring a dataset of crime statistics. The app provides an overview of the crime rate across
                            neighborhoods and allows users to focus on more specific information through
                            filtering crime type or time of the crime.
                            """
                        ),
                        html.H5("Use the box below to choose crimes of interest:"),
                        dcc.Dropdown(
                                    id = 'drop_selection_crime',
                                    options=[{'label': i, 'value': i} for i in df_t4['Category'].unique()
                                    ],
                                    style={'height': '20px',
                                        'width': '400px'},
                                    value=df_t4['Category'].unique(),
                                    multi=True)
                    ],
                    md=5,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.Iframe(
                                    sandbox = "allow-scripts",
                                    id = "plot_top",
                                    height = "400",
                                    width = "650",
                                    style = {"border-width": "0px"},
                                    srcDoc = make_plot_top().to_html()
                                    )
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            html.Iframe(
                sandbox='allow-scripts',
                id='plot_bot',
                height='500',
                width='1200',
                style={'border-width': '0px'},
                srcDoc= make_plot_bot().to_html()
                )
        )
    ],
    className="mt-4",
)

app.layout = html.Div(body)

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
    app.run_server(debug=False)