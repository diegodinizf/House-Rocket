# House Rocket - Insights Project

**Disclaimer**: this project was inspired by the "King County House Data" published on kaggle (https://www.kaggle.com/datasets/shivachandel/kc-house-data). It is a fictitious project but with all the steps of a real project.

## Business Scenario

House Rocket is a company that works reselling properties in King County (WA).

The company's CEO wants to know a strategy to generate profits for the next year, so they asked to create a analysis based on some questions that he brought.

**1. The CEO wants to know which properties the company should buy and their prices.**

**2. Once the property is purchased, when the company should sell it and for what price?**

**3. Should House Rocket do a home renovation to raise the sale price? What could be the renovation suggestions and how much would the price increasing?**

## Project Assumptions

- The date referenced in data is the date the property will be available for buying.
- In case of duplicate properties ID, it was kept the most recent data.
- The sale price is expected if the property is sold in its respective season.

## Solution Planning

In the end of the project it will be delivered:
- .csv report containing:
  - recommended properties for buying
  - sale price suggestion in the season
  - indicator of whether or not the property could be renovated to increase the sale price 
- Dashboard in Streamlit
  
 ### Tools
  
  In this project was used:
  - Python
  - Jupyter Notebook
  - Streamlit
  
 ### Process and Methods
  
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
    - Short topic where some of the finnancial results were estimated with the solution that was presented
   
 In this project were evaluated 10 hypotheses:
 
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

 The discussion of each hypothesis to validate or refute it is found in the notebook file. Below are the summary of the analysis of hypotheses 7, 8 and 9:

  ### 1. In the winter, properties prices tend to be 20% lower than in summer.
  
  **False**: By plotting the barchart of the prices by season is seen that prices in winter are the cheapest, but it is only 3.27% lower than the prices in summer. 
  
  ![image](https://user-images.githubusercontent.com/110054775/187316945-a467b517-dd97-40a1-a1ba-48e6c22dd548.png)
  
  ### 2. The number of bedrooms and bathrooms of a property has more effect on price than its total living area.
  
  **False**: By plotting the heatmap, it's possible to see what are the features with the biggest weight in data. In view of that, the total living area of the property has more influence on its price than the number of rooms.

- The properties living area have of 70% of influence over the price.
- Number of bedrooms and bathrooms have 32% and 53% of influence over the properties prices, respectively.
- Number of bathrooms has more influence over the living area than the number of bedrooms.

![image](https://user-images.githubusercontent.com/110054775/187319450-689872f4-d299-4108-bcfc-4d2b14c9ef88.png)

### 3. Properties renovated after 2005 have their prices higher than the properties which were renovated before 2005 or than have never been renovated.

**True**: On average, the properties renovated recently have higher prices whatever year the house was built. This analysis shows that a renovation can raise the sale price. The next challenge is to discover what are the most propitious homes to be renovated and what should be the new sale price

![image](https://user-images.githubusercontent.com/110054775/187319535-c0455e6e-c86a-4ecd-a636-f968cee75322.png)

# Results

Below are the presentations for each business problem brought by the House Rocket's CEO.

**1. The CEO wants to know which properties the company should buy and their prices.**

For this problem was suggested that properties which have their prices lower than the median price of the region and are in good conditions be bought.

This solution prevents the company from purchasing expansive properties which must need some renovation to be sold.

By plotting the count of the recommended properties, it can be seen that this solving of the problem results in **10502** properties that has a potential purchases

![image](https://user-images.githubusercontent.com/110054775/187498380-8330ea96-ec60-4b50-bf4c-e2ce02fe0c28.png)









  
  
  
   



