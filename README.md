# House Sales - Insights Project

In this link it's presented a Dashboard with the results of this project: 
https://diegodinizf-house-roc-streamlit-reportstreamlit-dashbord-t2tc14.streamlitapp.com/

#

**Disclaimer**: this project was inspired by the "King County House Data" published on kaggle (https://www.kaggle.com/datasets/shivachandel/kc-house-data). It is a fictitious project but with all the steps of a real project.

## Business Scenario

House Rocket is a company that works reselling properties in King County (WA).

The company's CEO wants to know a strategy to generate profits for the next year, so he asked to create an analysis based on some questions that he brought.

**1. The CEO wants to know which properties the company should buy and their prices.**

**2. Once the property is purchased, when should the company sell it and for what price?**

**3. Should House Rocket do a home renovation to raise the sale price? What could be the renovation suggestions and how much would the price increase?**

## Project Assumptions

- The date referenced in data is the date the property will be available for buying.
- In case of duplicate properties ID, it was kept the most recent data.
- The sale price is expected if the property is sold in its respective season.
- The square feet price includes the costs with home construction

## Solution Planning

In the end of the project it will be delivered:
- .csv report containing ("csv reports" folder):
  - recommended properties for buying
  - sale price suggestion in the season
  - indicator of whether or not the property could be renovated to increase the sale price 
 
- Dashboard in Streamlit containing:
  - filter options: price, bedrooms, bathrooms, waterfront
  - overview map with price distribution
  - density portfolio Map with recommendations
  - download option of the 3 .csv reports mentioned above
  
 ### Tools
  
  In this project was used:
  - Python (pandas, numpy, matplotlib, seaborn, folium, plotly)
  - Visual Code Studio
  - Jupyter Notebook
  - Streamlit
  - Version Control with git and github
  
 ### Process and Methods
 
 10 hypotheses were stated and evaluated in order to help in the solving of the business problem:
 
 1. Waterfront properties  are 20% more expansive, on average.
 2. Properties with built year prior to 1955 are 50% cheaper, on average.
 3. Properties without a basement are 40% bigger than the properties with basement.
 4. The YoY (Year over Year) price is increasing in 10%.
 5. Properties with 3 bathrooms have a MoM (Month over Month) price increasing in 15%. 
 6. Properties sell 20% more in summer than in winter.
 7. In the winter, properties prices tend to be 20% lower than in summer.
 8. The number of bedrooms and bathrooms of a property has more effect on price than its total living area.
 9. Properties renovated after 2005 have their prices higher than the properties which were renovated before 2005 or than have never been renovated.
 10. Properties that have their total living area smaller than the 15 closest properties are cheaper, on average.

 1. **Import Data**
    - Pandas was used to extract data from .csv archive
 2. **Transform Data**
    - Getting to know the data: dataframe lenght, data types and statistical parameters
    - NA values were filled and duplicates were dropped
    - Creating some features that helps on the solving of the problem
 3. **Exploratory Data Analysis**
    - Checking whether or not the hypotheses are true
    - Using what was discovered with the hypotheses to solve the business problem
 4. **Results**
    - Short topic where some of the financial results were estimated with the solution that was presented

 The discussion of each hypothesis to validate or refute it is found in the notebook file. Below are the summary of the analysis of hypotheses 7, 8 and 9:

  ### 1. In the winter, properties prices tend to be 20% lower than in summer.
  
  **False**: By plotting the barchart of the prices by season is seen that prices in winter are the cheapest, but it is only 3.27% lower than the prices in summer.
  
  In the winter, the quantity of sales are also lower than in other seasons (see hypothesis 6 in the notebook file)
  
  ![image](https://user-images.githubusercontent.com/110054775/187316945-a467b517-dd97-40a1-a1ba-48e6c22dd548.png)
  
  ### 2. The number of bedrooms and bathrooms of a property has more effect on price than its total living area.
  
  **False**: By plotting the heatmap, it's possible to see what are the features with the biggest correlations with price. In view of that, the total living area of the property has more influence on its price than the number of rooms.

- The properties' living area ("sqft_living") have 70% of influence over the price.
- Number of bedrooms and bathrooms have 32% and 53% of influence over the properties prices, respectively.
- Number of bathrooms has more influence over the living area than the number of bedrooms.

![image](https://user-images.githubusercontent.com/110054775/187319450-689872f4-d299-4108-bcfc-4d2b14c9ef88.png)

### 3. Properties renovated after 2005 have their prices higher than the properties which were renovated before 2005 or than have never been renovated.

**True**: On average, the properties renovated recently have higher prices whatever year the house was built. This analysis shows that a renovation can raise the sale price. The next challenge is to discover what are the most propitious homes to be renovated and what should be the new sale price

![image](https://user-images.githubusercontent.com/110054775/187319535-c0455e6e-c86a-4ecd-a636-f968cee75322.png)

# Results

Below are the answers for each business problem brought by the House Rocket's CEO.

**1. The CEO wants to know which properties the company should buy and their prices.**

For this problem was suggested that properties which have their prices lower than the median price of the region and are in good conditions be bought.

This solution prevents the company from purchasing expensive properties which must need some renovation to be sold.

By plotting the count of the recommended properties, it can be seen that this solving of the problem results in **10502** properties that has a potential purchases

![image](https://user-images.githubusercontent.com/110054775/187498380-8330ea96-ec60-4b50-bf4c-e2ce02fe0c28.png)

**2. Once the property is purchased, when should the company sell it and for what price?**

In this case, the properties were grouped by region (zipcode) and the season extract from date. Properties that have their prices lower than the median price of the region at that season can be sold for 30% increase in their prices. The ones with prices higher than the median can be sold for a 10% increase.

This solution prevents prices from rising far above the region's range at that season. Thus, properties with higher prices don't deviate from median and the ones with lower prices can get more close to the market expectation.

Since these sale prices are expected for the current season extracted from the "date" column, it's also recommended that properties be sold until the end of their respectives seasons.

Below it's shown a chart of profit by season

![image](https://user-images.githubusercontent.com/110054775/187521576-0c3d3629-cde9-48fe-ae02-9904ba0a9574.png)

The solution adds the company a gain of more than **$ 400 million** in 1 year.

**3. Should House Rocket do a home renovation to raise the sale price? What could be the renovation suggestions and how much would the price increasing?**

It was considered that homes which were smaller than the 15 ones closest to them could have an increase in their living spaces through a renovation. This option was recommended, since total living area is the most influential variable for the price.

Further, the new space it's limited on 25% of the total available space in the home. This limit was maintained to prevent property prices from rising too much. 

This solution shows that it's possible to increase the sale prices by doing a renovation in **5612** properties (**53,4%** of the portfolio of purchase recommendations)

Below is presented a chart comparing the gaining House Rocket would have if they did a home renovation in some of the properties. The new results shows that profit increases in almost 2 times. A gain of more than **$ 800 million** in 1 year. 

![image](https://user-images.githubusercontent.com/110054775/187540653-7d67585e-d5e6-4744-9cc2-f89a610163f1.png)

## Conclusion

This project was able to present a strategy for the company to generate profit in a period of almost 1 year. It was presented purchase recommendations taking into account the conditions of the property. Also, it was possible to almost double the gains with a option of renovation in some homes that could have a bigger living space. In the end, everything that was proposed was delivered in a dynamic dashboard, using Streamlit, where the CEO may filter some attributes, and make his own visual and numeric anaylisis.

## Next Steps

Below are some suggestions for future steps in this project:

- It can be done a sales forecast using machine learn models in order to indentify minor behaviors over the seasons
- Since the number of bathrooms it's a influent factor over the price, it also can be done a study for new bathrooms constructions inside the property
- Finally, the properties also could be evaluated by it's area: if it's urban or rural by its square feet lot, for example.















  
  
  
   



