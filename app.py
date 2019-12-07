import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import altair as alt
from py_scripts.plotter import make_plot_top, make_plot_bot
from py_scripts.wrangle_data import prep_data

alt.data_transformers.enable('default')
alt.data_transformers.disable_max_rows()

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})  # noqa: E501

server = app.server
app.title = 'Victorious Secret Crime Analyzer'

# get the top 4 crimes df
df_t4 = prep_data()

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
                                    srcDoc = make_plot_top(df_t4).to_html()
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
                srcDoc= make_plot_bot(df_t4).to_html()
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