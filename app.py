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

def make_plot_top(df_new=df_t4):
    
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # making the slider
    slider = alt.binding_range(min = 0, max = 23, step = 1)
    select_hour = alt.selection_single(name='select', fields = ['hour'],
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
        title = "Per hour crime occurrences for your selection of the top 4 crimes",
        width=500,
        height = 315
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
        height=350
    )

    chart_2 = alt.Chart(data).mark_bar().encode(
        x=alt.X('PdDistrict:N', axis=None, title="District"),
        y=alt.Y('count()', title="Count of reports"),
        color=alt.Color('PdDistrict:N', legend=alt.Legend(title="District")),
        tooltip=['PdDistrict', 'count()']
    ).properties(
        width=450,
        height=350
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

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("San Francisco Crime"),
                        html.P(
                            """\
                            When looking for a place to live or visit, one important factor that people will consider
                            is the safety of the neighborhood. Searching that information district
                            by district could be time consuming and exhausting. It is even more difficult to
                            compare specific crime statistics across districts such as the crime rate
                            at a certain time of day. It would be useful if people can look up crime
                            related information across district on one application. Our app
                            aims to help people make decisions when considering their next trip or move to San Francisco, California
                            via visually exploring a dataset of crime statistics. The app provides an overview of the crime rate across
                            neighborhoods and allows users to focus on more specific information through
                            filtering crime type or time of the crime.

                            Use the box below to choose crimes of interest.
                            """
                        ),
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
                                    height = "500",
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