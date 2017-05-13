
# Evaluating Airbnb in Boston Area

Author: [Bohan Li](https://github.com/bohanli0403), [Ningyi Xue](https://github.com/Ginnyxue), [Han Xiao](https://github.com/HanXiaocs), [Yiran Pan](https://github.com/yiran123)

## Introduction
As one of the most famous online marketplaces and hospitality service websites, Airbnb becomes more and more popular among travelers all around the world. However, do travelers really know the Airbnb housing they choose to stay? Unlike looking for a traditional hotel on travel agency websites, customers usually need to spend more time on finding a safe and convenient house that matches their expectation because Airbnb let hosts provide all the information, which could lead to the lack of credibility. In addition, according to our own experience, we find that people tends to give high ratings to hotels/Airbnbs due to many reasons(ex. give random score; hosts are really nice so they don't want to give low score; don't want to receive low score from the hosts; not familiar with the neighbors). Under the influences of many factors, the original airbnb review may be biased. In our project, we decide to let the data talks. Besides the original Airbnb reviews given by customers, we also evaluate other factors that could affect the qualities of Airbnb housings in Boston Area. The goal of our project is to help potential Airbnb customers to choose the best Airbnb of they needs.

## Tools and Dataset

### Programming Languages
1. Python
2. MongoDB
3. D3.js
4. Leaflet js

### Datasets
1. City of Boston crime incident July 2012 - August 2015
   
   https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-July-2012-August-2015-Sourc/7cdf-6fgx
2. Active Food Establishment Licenses
   
   https://data.cityofboston.gov/Permitting/Active-Food-Establishment-Licenses/gb6y-34cq
3. Food Establishment Inspections
   
   https://data.cityofboston.gov/Health/Food-Establishment-Inspections/qndu-wx8w
4. Entertainment Licenses
   
   https://data.cityofboston.gov/Permitting/Entertainment-Licenses/qq8y-k3gp
5. Airbnb Boston
   
   http://insideairbnb.com/get-the-data.html
   
6. MBTA Bus Sthttp://insideairbnb.com/get-the-data.htmlops
   
   http://datamechanics.io/data/wuhaoyu_yiran123/MBTA_Bus_Stops.geojson

### Data Retrieval
In our project, we mainly use coordinates to locate places and employ geopy/vincenty to calculate the distances between places in different datasets in order to obtain a statistic.

| Transformations | Original Dataset                 | New combination|
| -------------   |:---------------:                 | --------------:|
| 1               | Active food establishment license, Crime Boston | Crime number around each food establishment(within 1 mile)|
| 2               | MBTA Bus Stop, Airbnb Rating(Original), Entertainment License|Entertainment & bus stop number around each Airbnb|
| 3               | Active food establishment license, Food Establishment Inspection |Cleanliness level of food establishments(Passrate of inspections)|
| 4               |Cleanliness level of food establishments, Crime number around each food establishment(within 1 mile),Entertainment & bustop number around each Airbnb|Correlation coefficient|
| 5               |correlation coefficient|Food establishment score system|
| 6               |Food establishment score system, Airbnb Rating| Airbnb surrounding food establishment score (Average)|
| 7               |Airbnb Rating, Crime Boston | Crime number around each Airbnb(within 1 mile)|
| 8               |Airbnb Rating, Entertainment & bus stop number around each Airbnb, Airbnb surrounding food establishment score (Average), Crime number around each Airbnb(within 1 mile)|Airbnb Score System|
| 9               |Airbnb Score System|Score distribution(for visualization)|

# Algorithm

## Score system 

In this project, the original Airbnb reviews by customers only serve as a part of the evaluation. For each Airbnb housing, we also count and calculate safety level, surrounding dining options (safety and cleanliness), recreations, entertainments, transportations (bus stops). Then we normalize and weight all scores evenly to get the final rating of Airbnb housings under our standard. 

Normalization:

![equation](http://latex.codecogs.com/gif.latex?x_%7Bnew%7D%20%3D%20%5Cfrac%7Bx-%20x_%7Bmin%7D%7D%7Bx_%7Bmax%7D%20-%20x_%7Bmin%7D%7D)

finalScore = (reviews + safety + transportation + recreationAndDinning)/4

Here's the weighted score frequency bar graph:

![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/bar.png)

## Correlation Coefficient
The definition of correlation coefficient:

![equation](http://latex.codecogs.com/gif.latex?corr%28x%2Cy%29%3D%20%5Cfrac%7Bcov%28x%2Cy%29%7D%7Bstd%28x%29%20%5Ccdot%20std%28y%29%7D)

We calculate correlation coefficients between the most concerned factors (original Airbnb ratings, weighted Airbnb scores, safety level, transportation) and generate three plot graphs to show the relationships.
Here is the distribution (Our first visualization) as well as the corresponding analysis.

### Original Airbnb Ratings(y-axis) vs. Weighted Airbnb Scores(x-axis)

![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/oldnew.png)

Correlation coefficient: 0.66

Overall, the original Airbnb ratings is higher than the Weighted Airbnb scores, but they are strong positive related. The reviews from customers are relatively reliable. Also, for Airbnb housings that haven’t been booked by any customer (dots on x-axis), there are still a few of them worth a try for they have relatively high weighted scores.

### Original and Weighted Airbnb Scores(x-axis)  vs  Safety Level (y-axis) 

![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/Screen%20Shot%202017-04-26%20at%204.01.54%20AM.png)
![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/Screen%20Shot%202017-04-26%20at%203.59.33%20AM.png)

Correlation coefficient: 0.01 and -0.61

Above graph No.1 shows the weak positive relationship between original Airbnb scores and number of crimes happened 1km within of each Airbnb. Although the original ratings do not strongly connect to the number of crimes, we can observe that high rating Airbnb housings are mostly located in safe areas. Thus we think it is reasonable to take safety as one factor that may affect the evaluations. 
Graph No.2 shows the strong negative relationship between weighted scores and number of crimes. 

### Original Airbnb Scores vs. Transportation Convenience

![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/Screen%20Shot%202017-05-08%20at%209.28.55%20PM.png)

Correlation coefficient: -0.01

The relationship between Original Airbnb scores and transportation convenience is almost not related. We cannot summarize that Airbnb housings in which neighbors tend to be more convenient in respect to transportation. Therefore, it is important to add this factor to the total rating, because each Airbnb is unique.

# Visualizations

Files can be found in the folder Visualization.

## First Visualization: Plotting (Must open in Firefox)

The above graphs of the correlation coefficients are the first visualization. Our code is based on a plotting template we found on d3js.org. The script reads data from tsv file and plot on a html page. Users can click each dot on the graph to see the exact value of the dot.(i.e different scores)

About the data: The original template required tsv file as input. Since we're using mongodb, the data file must be exported as json or csv first then use convertor to create a tsv file.

## Second Visualization: An interactive map

We employ another js map library called leaflet and create an interactive map to help Airbnb customers to choose their ideal Airbnb.

Here is a screenshot of the map:
![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/map1.png)
![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/map2.png)

This is a satellite map of Boston with neighbor names and roads. Each dot on the map represent one Airbnb housing. While a user clicks a dot, an info box will pop out. So far we include the name, weighted score and an Airbnb link to the house. More fields can be added to the box (just need a little change on the source code, the data file we use basically includes all raw scores and calculated scores).
The map can be zoomed in/out. 

For each plot of houses on the map, overall score > 0.8 is orange, 0.5 < score < 0.8 is blue, and those below 0.5 are set to yellow. 

# Conclusion

This is an open-ended project with no certain conclusion. Our ultimate goal is to write a semi-application that can be extended and adjusted to a real product that can be used to help potential Airbnb customers. The interactive map is a model that cound be used in the future.

Also, the data itself actually reveals a lot of information. Generally, the original score and the weighted score are related, which implies that most customers' reviews are reliable. However, the overall weighted scores are lower than the original scores. This means the factors that we consider to be important actually drag down the whole scale. Therefore, a house that have a big gap between the original scores and the weighted scores may not be a good choice to stay. For example, while we calculate the crime number around Airbnb houses, the number is actually greater than what we thought it would be. This could be an effective factor on those low rating houses. Also, many of our favorite restaurants actually failed a lot of inspections. Cooking at home seems to be a necessary skill :)

# Further Extension and Limitation

Due to the limitation of the datasets we can deploy, we only cover a small part of factors that may affect Airbnb ratings. Prices and evaluation of hosts should also be considered. Some of the data we use is rather old. Also, the Airbnb dataset is not the live data of the website. Some information may be changed. While we test the maps, we found some URLs were already expired.

In addition, because we define the scoring system and algorithm by our own understandings, the scores may be biased. 

This project still has some space to extend in the future. We also planned a search engine that allows users to directly search their ideal or potential Airbnb housings for their trips. We could also allow searching by filters to satisfy various needs (ex. Highest rating, neighbors with most entertainments, safest neighbor).  In fact, if we have enough information, we may be able to write an application that can be used in reality. 


# Reference 
1. https://bl.ocks.org/mbostock/3887118
2. http://leafletjs.com/




