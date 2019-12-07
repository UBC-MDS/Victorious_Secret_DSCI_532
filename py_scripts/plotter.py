import pandas as pd
import numpy as np
import altair as alt
from py_scripts.theme import mds_special

# register the custom theme under a chosen name
alt.themes.register('mds_special', mds_special)

# enable the newly registered theme
alt.themes.enable('mds_special')  
alt.data_transformers.enable('default')
alt.data_transformers.disable_max_rows()

def make_plot_top(data):
    """
    Make the time plot for 
    San Fransisco crime data.
    
    parameters:
    -----------
    data : pandas.DataFrame
        data frame containing the crime data
    
    returns:
    --------
    alt.Chart
        altair plot

    """
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    # making the slider
    slider = alt.binding_range(min = 0, max = 23, step = 1)
    select_hour = alt.selection_single(name='select', fields = ['hour'],
                                    bind = slider, init={'hour': 19})
    
    chart = alt.Chart(data).mark_bar(size=30).encode(
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

def make_plot_bot(data):
    """
    Make the histogram and geoplots 
    for San Fransisco crime data.
    
    parameters:
    -----------
    data : pandas.DataFrame
        data frame containing the crime data
    
    returns:
    --------
    alt.Chart
        altair plot

    """
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