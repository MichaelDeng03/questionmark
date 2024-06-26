## Presentation Link
[link](https://www.canva.com/design/DAFbqI0E768/EHMsXmpTsuqUyfFRP5JlGw/view?utm_content=DAFbqI0E768&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
## Inspiration
In some rural areas in the United States, people have to drive up to 30 minutes to get to the nearest hospital. The pandemic made access to hospitals even more difficult because of how overwhelmed they were with COVID-19 patients. 
## What it does
Our program takes a state and the number of hospitals to be built, then determines the most efficient locations so that they can reach the most people.
## How we built it
We joined data from the Center of Medicaid and Medicare Services and the Department of Homeland Security to get a list of Medicare hospitals, their addresses, and the number of people they can reach. We used this in conjunction with US Census Data containing city populations. With this data, we used a weighted k-means algorithm to identify the clusters of populations in need of a hospital.
## Challenges we ran into
We struggled with debugging the customized k-means, setting the weights for every city node, and dealing with sometimes inconsistent data (especially when joining tables).
## Accomplishments that we're proud of
We're proud of the weighted k-means algorithm, integrating with the Google Maps API, and having an interactive front end.
## What we learned
It's important to get the simple things working before adding new features, especially when you have a time constraint.
## What's next for Hospital Locator
In the future, we'd love to add more visualization features for the clustering and allow users to be able to input counties that they'd like to live in. 
