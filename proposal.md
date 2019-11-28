
# 1\. Motivation and Purpose

When looking for a place to live or visit, one important factor that people will consider
is the safety of the neighborhood. Searching that information district
by district could be time consuming and exhausting. It is even more difficult to
compare specific crime statistics across districts such as the crime rate
at a certain time of day. It would be useful if people can look up crime
related information across district on one application. Our app
aims to help people make decisions when considering their next trip or move to San Francisco, California
via visually exploring a dataset of crime statistics. The app provides an overview of the crime rate across
neighborhoods and allows users to focus on more specific information through
filtering of geological location, crime rate, crime type or time of the
crime.


# 2\. Data Description 
We will be visualizing approximately 150,500 observations about crime rates in the city of San Francisco for the year of 2016 provided by [Coursera](https://www.coursera.org/) and [IBM]( https://www.ibm.com/). This dataset is available for free on [Kaggle]( https://www.kaggle.com/roshansharma/sanfranciso-crime-dataset), under the Open Database License. Each crime observation is described by 15 attributes; however, we will be focusing on 5 of them for our app. 

-	`IncidntNum` is our primary key, which we will be using to count unique occurrences of a crime. 
-	`Category` defines the crime type, e.g. larceny, theft, assault, etc. Additionally, we will allow our users to modify visualizations based on crime type.
-	`Time` is the time of day when the crime took place. We will be transforming this into hour ranges to view crimes between 6am and 7am, for example.
-	`PdDistrict` refers to the different police districts in the city of San Francisco which roughly maps onto different neighborhoods. We will be giving the user the ability to drill down on rate of crimes in different San Francisco neighborhoods.
-	`X` and `Y` are respectively the latitudes and longitudes of the crime incidents, and we will be using these to form a crime density map so that the user can view neighborhoods of high crime density in the city of San Francisco.

# 3\. Research Questions and Usage Scenarios 
## Visiting San Francisco
  Imagine Anny, she’s a frequent traveler and knows that no matter which city or country she’s going to visit, safety comes first. She decided to plan a trip to San Francisco, but she’s never been there and doesn’t know much about the neighborhoods. She wants to make sure that her trip will be as safe as possible so she can take home only good memories. As a part of her planning process, she wants to get deeper insight about the current crime rate situation in San Francisco. Anny wants to explore the data set and identify the most appealing neighborhood for her short stay. Anny also owns and travels in her own car, so her biggest concern is vehicle theft. Because who wants to find themselves in an unfamiliar city without their primary method of transportation, right? Therefore, she wants to be able to only [choose parameters of interest] during her planning process. When Anny logs into the Victorious Secret dashboard she will see an overview of all the available crimes (different types of criminal offenses) in her dataset, according to the neighborhood where the crime was committed. She can filter out crime types that are not relevant to her situation and find the most appropriate neighborhood for her stay.

## Moving to San Francisco
  Let’s also look at David. Since he recently moved to San Francisco for work, he is now in the middle of an apartment hunt. He approximately knows in what neighborhoods he can afford accommodation, but how to choose between them? With logging into the Victorious Secret dashboard, he’s now able to choose all the neighborhoods he’s interested in and see which one is the safest overall, or has smallest frequency of vandalism and theft. In an additional graph in the dashboard, where he can see a per hour rate of crimes, he noticed that the peak hour for theft is around the 6pm mark. David started to think that this must be a concern for his safety, as he’s usually just getting back home from work at that time and decided to invest more in house alarms.

## Journalism Crime Reporting 
  And finally, Angela is an investigative journalist who wants to dive deep into the criminal records of San Francisco and find content for her article. The most important questions that she raises are: what was the most notorious crimes for a specified hour and how do these crimes vary across different districts. What was the district with highest incidence reports for each of the top 4 crimes? She logs into the dashboard and goes through hours and locations. Angela sees that Southern district is the most notorious for assault, larceny/theft, and vandalism crimes, with more density towards the border between Mission and Northern districts. And the number of top four criminal offenses reported rises from 5 am onwards and peaks at 6 pm. Moreover, this count drops after 6 pm and is at its lowest at 5 am. That made her think that she needs to conduct a follow-on study about the working hours of people in those districts.
