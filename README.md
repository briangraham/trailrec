# Rec & Ride
## Mountain Bike Trail Recommendation System

## Background
According to a 2010 [report](https://www.imbacanada.com/sites/default/files/Mountain-Biking_Market-Profiles.pdf) the International Mountain Bike Association, there were over 7 million people annual riders between the US and Canada. Those numbers are almost certainly higher today. Mountain Bikers will travel often to ride.  In a [survey](https://www.singletracks.com/blog/mtb-trails/mountain-bike-tourism-by-the-numbers/) of 1500 riders by Singletracks, they found that riders take 2-4 trips per year to ride.  Interestingly, 62% of these mountain bike tourists were traveling in order to ride new trails, but only 2.6% wanted to experience new styles of riding.  That means that people want to stick to what they know when they travel: they want to ride similar trails to what they are used to in terms of style, but want the excitement new trails in different locations.

## A wealth of data
Websites like Trailforks.com provide detailed information for 140,000 trails across the globe, with about 75,000 trails located in the US and Canada. Riders can navigate Trailforks to research trails and decide where to ride. This trail information is provided by a mix of local trail organizations, park services, and volunteers who upload trail descriptions, update trail conditions, rate trails, and log their rides to provide gps information that can be used to calculate trail metrics such as distance, vertical, and average ride time.

## How to find the next trail to ride
Trailforks is an amazing resource, but it can be difficult to navigate the wealth of information it provides. Take this [map](https://www.trailforks.com/region/british-columbia/map/) of British Columbia, Canada from Trailforks.com.  BC is one of the most popular MTB destinations in the world.  The circles on the map represent the number of trail systems in that area.  Each system can have 10s to nearly 100 trails, depending on its size. If you flew to vancouver, you would have access to 100s of trail within a 2 hour drive of the city.  Sorting thorugh all of this information on Trailforks can be a tedious task: it requires navigating the map interface or scrolling though an [extensive list of trails](https://www.trailforks.com/region/british-columbia/trails/), then opening up tons of browser tabs as you read all of the available info of each trail.  With the amount of data available on trailforks and modern recommednation system technqiues, we surely could make some improvments to the trail search process.

## The Solution
Rec & Ride simplifies the search process for someone who is trying to plan their next trip.  If a user was planning a trip to a specific region, they could be served a personalized list of the top 10 trails for them to ride, with only minimal input from the user. There are two methods by which it can serve recommendations, by finding similar trails to a trail the user likes, or by crowdsourcing recommendations from other users.  For the purposes of protoyping this system, I scraped the Trailforks trail pages of all the trails in British Colmbia.

### Finding Similar Trails (Feature-Based Trail Recommendations)
The Rec & Ride app can take either a BC trail name or Trailforks trail page url input by the user and output the 10 most similar trails in the BC trail system.  A trail vector is created using a combination of features including numerical trail metrics (ex trail distance), categorical information (ex difficulty), and trail description text ("This trail has a tricky start with lots of rocks and roots..."). Trail description text was vectorized using [TF-IDF](https://en.wikipedia.org/wiki/Tf–idf).  The cosine similarity metric is used to compare the similarity of every combination of trail.
### User Behavior-Based Recommendations (Collaborative Filtering)

Users can enter the name of one of their favorite trails, and receive recommendations for similar trails to ride, which are based on the trail features. If they already are an active user of Trailforks.com who records their rides on the app, they can enter their username and receive recommendations that are crowdsources from the activity of other users.


#### Demo Link
www.recandride.xyz
