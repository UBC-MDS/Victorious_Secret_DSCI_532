# Victorious_Secret_DSCI_532
A San Francisco Crime Rate Dashboard: Criminals Beware. We know all the answers!! 


Group Members:

- Lesley Miller
- Anas Muhammad
- Polina Romanchenko
- Xinwen Wang

# App Description 

The app contains two panels. The top panel displays the overall distribution of crime frequency in San Francisco at certain time points. There are two drop down bars to specify crime information: one for choosing the crime type, another for choosing the neighborhood. Users can adjust the Time of Day with a slider to view frequency of crimes over time. The bottom panel contains two graphs to display specific crime information that users want to focus on. The left graph is a bar chart for the crime frequency at a specific time point in neighborhoods specified by the user. The right graph displays a point for an incidence of a crime at a specific location, color coded by neighborhood. The density of the points results in map of San Francisco. Filtering by neighborhood, the user can highlight the points of their choice, leaving the rest of the points greyed out.




![Dashboard Sketch](https://github.com/UBC-MDS/Victorious_Secret_DSCI_532/blob/master/img/victorious_secret_dashboard.png?raw=true)

# Functionality Description 

The app contains a main drop-down feature, allowing the user to filter for type of crime. This feature affects the types of crimes shown in the time series panel in the upper right and also affects the crimes available to view in the bottom panel. The slider allows the user to view crime counts at a specified hour of the day starting at Hour 0 or midnight. The bottom panel contains a drop-down menu that allows a user to select a single crime and view its crime count distribution across San Francisco neighborhoods. Hovering over data points in any of the plots brings up a tooltip that provides more information about that specific data point. 
