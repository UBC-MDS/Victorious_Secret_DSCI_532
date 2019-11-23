
# 1\. Motivation and purpose

When looking for houses, one important factor that people will consider
is the safety of the neighborhood. Searching that information district
by district could be time consuming and exhausting. It is even harder to
compare specific crime statistics across districts like the crime rate
at a certain time point which some people might care about if their work
ends really late. It would be useful if people can just look up crime
related information across district on one mobile application. Our app
aims to help people make decisions when considering potential dwellings
via visually explore a dataset of crime statistics in San Francisco,
United State. The app provides an overview of the crime rate across
districts and allows users to focus on more specific information through
filtering via geological location,crime rate, crime type or time of the
crime.

# 2.\. Description of the data.
We will be visualizing approximately 150,500 observations about crime rates in the city of San Francisco for the year of 2016 provided by [Coursera](https://www.coursera.org/) and [IBM]( https://www.ibm.com/). This dataset is available for free on [Kaggle]( https://www.kaggle.com/roshansharma/sanfranciso-crime-dataset), under the Open Database License. Each crime observation is described by 15 attributes; however, we will be focusing on 5 of them for our app. 
•	`IncidntNum` is our primary key, which we will be using to count unique occurrences of a crime. 
•	`Category` feature defines the crime type, e.g. Larceny, theft, assault, etc. Additionally, we will allow our user to modify visualizations based on crime type.
•	`Time` the time of day when the crime took place, we will be transforming this into hour ranges to view crimes between 6am and 7am for example.
•	`PdDistrict` refers to the different districts in the city of San Francisco, we will be giving the user the ability to drill down on rate of crimes at different districts.
•	`X` and `Y` are respectively the latitudes and longitudes of the crime incidents, and we will be using these to form a choropleth map so that the user can view areas of high crime density in the city of San Francisco.
