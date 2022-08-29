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

  ### 1. In the winter, properties prices tend to be 20% lower than in summer
  
  **False**: By plotting the barchart of the prices by season is seen that prices in winter are the cheapest, but it is only 3.27% lower than the prices in summer. 
  
  ![image](https://user-images.githubusercontent.com/110054775/187315278-292ef03f-1272-4130-b042-a285f1ae62ee.png)


  
  
  
   



