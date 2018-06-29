# When is the Best Time to Vacation in Hawaii?
This project utilizes historical weather observations from different stations in Hawaii, to show a potential vacationer what the
weather could be like based on the previous year's weather.

## Tools Used:
* Database: SQLite, PythonSQL Alchemy to create and query
* Data Visualization: Python Matplotlib and Seaborn libraries
* Server: Python Flask App

## Process
1. #### [Data Engineering](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/data_engineering.ipynb)
This step reads two csv files, performs clean up and writes cleaned files to a new location. 

2. #### [Database Engineering](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/database_engineering.ipynb)

* Read Cleaned files into Pandas dataframes
* Use the SQLAlchemy engine and connection to create a database
* Use SQLAlchemy declarative_base and create classes for each table
![Create Classes](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/databaseclasses.PNG)

* Create the tables and populate the database using the data in the Pandas dataframes
![Create Tables](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/databasecreatetable.PNG)

3. #### [Analyze Data](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/climate_analysis.ipynb)
The analysis shows the vacationer the following information to evaluate the timing of their trip: 
* Rainfall Observations shown over time and in histogram form

![Hawaii Precipitation Over 12 months](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/Precipitation_Over_12Months.png)

![Rainfall Histogram](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/Rainfaill_Histogram.png)
* Average Temperature for the Vacation Dates Entered
![Trip_Avg_Temp](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/Trip_Avg_Temp.png)

* Historical Daily Normals (Max, Min and Average Temperatures)
![Historical Daily Normals](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/Historical_Daily_Normals.png)

4. Deploy Database Queries to Flask App to make data available
This is one of the app routes available:
![Flask App Route](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/exampleapproute.PNG)

