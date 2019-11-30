
## Reflection (10%)
rubric={raw:10}

In this section, you should (as a group) critique your dashboard and point out what it does well, what its limitations are, and what are good future improvements and additions. 
In this section, you should also **clearly document** how you addressed the feedback (GitHub issues) you received from your peers and the TAs.
Point form is fine, but they need to be full sentences.
This section should not be more than 500 words.



One of the main issues of this dashboard lies in the data we use for plotting; it lacks the population of a district. Hence, this fact leaves us with no ability to normalize the number of crime occurrences per population of a district as it would have been more insightful to show crimes per capita.
Another issue we'd encountered during the building of this app is its speed. The problem is primarily caused by the map plot. The way it works with our dataset is that every crime has location coordinates attached to it, Altair plots every data point individually and it appears as a map. Our dashboard wrangles data based on the user's selection and plots the Altair plot once again from scratch. The whole process takes time and it causes delays in between user's input and actual replotting the data.
Due to the lack of designers in our team, users can observe that overall showcasing of the app could have been better. The fonts and coloring needs significant improvement but in order to prevent this app from looking like an eyesore, we played it safe and left the design for future modifications.
