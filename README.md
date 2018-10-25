# Rec & Ride
## Mountain Bike Trail Recommendation System

## Background
According to a 2010 [report](https://www.imbacanada.com/sites/default/files/Mountain-Biking_Market-Profiles.pdf) the International Mountain Bike Association, there were over 7 million annual mountain bike riders between the US and Canada. Those numbers are almost certainly higher today. These Mountain Bikers will travel often to ride.  In a [survey](https://www.singletracks.com/blog/mtb-trails/mountain-bike-tourism-by-the-numbers/) of 1500 riders by Singletracks, it was found that riders take 2-4 trips per year to ride.  Interestingly, 62% of these mountain bike tourists were traveling in order to ride new trails, but only 2.6% wanted to experience new styles of riding.  This means that people want to stick to what they know when they travel: they want to ride similar trails to what they are used to in terms of style, but want the excitement new trails in different locations.

## A wealth of data
Websites like Trailforks.com provide detailed information for 140,000 trails across the globe, with about 75,000 trails located in the US and Canada. Riders can navigate Trailforks to research trails and decide where to ride. This trail information is provided by a mix of local trail organizations, park services, and riders who upload trail descriptions, update trail conditions, rate trails, and log their rides to provide gps information that can be used to calculate trail metrics such as distance, vertical, and average ride time.

## How to find the next trail to ride
Trailforks is an amazing resource, but it can be difficult to navigate the wealth of information it provides. Take this [map](https://www.trailforks.com/region/british-columbia/map/) of British Columbia, Canada from Trailforks.com.  BC is one of the most popular MTB destinations in the world.  The circles on the map represent the number of trail systems in that area.  Each system can have tens to nearly a hundred trails, depending on its size. If you flew to vancouver, you would have access to hundreds of trails within a 2 hour drive of the city.  Sorting thorugh all of this information on Trailforks can be a tedious task: it requires navigating the map interface or scrolling through an [extensive list of trails](https://www.trailforks.com/region/british-columbia/trails/), then opening up tons of browser tabs as you read all of the available info of each trail.  With the amount of data available on trailforks and modern recommednation system techniques, we surely could make some improvments to the trail search process.

## The Solution
The goal of Rec & Ride is to simplify the search process for someone who is trying to plan their rides on their next trip.  If a user was planning a trip to a specific region, they could be served a personalized list of the top 10 trails for them to ride, with minimal effort by the user. There are two methods by which it can serve recommendations, by finding similar trails to a trail the user likes, or by crowdsourcing recommendations from other users.  For the purposes of protoyping this system, I scraped the Trailforks trail pages of all the trails in British Colmbia.

### Finding Similar Trails (Feature-Based Trail Recommendations)
The Rec & Ride app can take either a BC trail name or Trailforks trail page url input by the user and output the 10 most similar trails in the BC trail system.  A trail vector is created using a combination of features including numerical trail metrics (ex: trail distance), categorical information (ex: difficulty), and trail description text (ex: "This trail has a tricky start with lots of rocks and roots..."). Trail description text was vectorized using TF-IDF.  The cosine similarity metric is used to compute the similarity between every trail combination.  When a user inputs a trail, the top 10 most similar trails are returned to them.

### User Behavior-Based Recommendations (Collaborative Filtering)
A user can also enter their Trailforks username if they have an account and log their rides on the Trailforks app. The collaborative filtering algorithm uses 1.5 million trail ride logs from 10,000 users in the BC trail system.  First, a proxy rating is calculated for how much a user likes a trail, based on the number of times they have ridden that trail out of their total number of rides. The proxy rating is scaled from 1 to 5.  A spares matrix is created with rows representing users and columns representing trails: the values of the matrix are the proxy ratings. An [SVD matrix factorization algorithm](https://surprise.readthedocs.io/en/stable/matrix_factorization.html) is used to learn the embeddings that map users to trails, which can then be used to predict the missing values in the proxy ratings matrix. When a user enters their Trailforks username into the app, they will be served their top 10 highest rated trails which they haven't ridden yet.

#### Demo
A proof of concept version of the app is up and running here: www.recandride.xyz.  Since I only had 3 weeks to work on this project during my Insight Data Science Fellowship and did not have access to the trailforks database, I only had the BC trail dataset I scraped, and ended up limiting myself to a subset of the trails that had trail descriptions.  If you do not enter one of these trails, the app will not work.  Also, if a user had not ridden one of these trails prior to Sepember 22nd, their username will not be in my database.  Ridelog pages for a trail can be accessed by clicking on the Ridelog tab on a trail's page.  You can then go back a couple pages until you reach early September ride logs and pull usernames from the list if you want to give that part of the app a try.
