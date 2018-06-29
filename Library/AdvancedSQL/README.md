# Advanced SQL using Python
This project takes weather observation readings at different stations in Hawaii, created a SQLite database and then utilizes database 
queries to achieve visualizations of the data. 

## Process
* #### [Data Engineering](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/data_engineering.ipynb)
This step reads two csv files, performs clean up and writes cleaned files to a new location.
* #### [Database Engineering](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/database_engineering.ipynb)
1. Read Cleaned files into Pandas dataframes
2. Use the SQLAlchemy engine and connection to create a database
3. Use SQLAlchemy declarative_base and create classes for each table
![Create Classes](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/databaseclasses.PNG)

4. Create the tables and populate the database using the data in the Pandas dataframes
![Create Tables](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/databasecreatetable.PNG)

* #### [Analyze Data](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/climate_analysis.ipynb)
![Hawaii Precipitation Data 12 months](https://github.com/cammster/FullStackSkillsLibrary/blob/master/Library/AdvancedSQL/Images/Precipitation_Over_12Months.png)

