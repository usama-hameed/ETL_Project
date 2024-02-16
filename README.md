### Run Project
Follow the following steps to start the project
1. Clone in you local machine
```
   git clone https://github.com/usama-hameed/ETL_Project.git
```
2. Run Follwoing command in the root directory
```
   docker-compose up
```
This Commnad will install all the required packages and start the following service:
1. etl
2. postgres

'etl' container has all the code related to scraping, cleaning and loading in database.
In 'etl' container logs if you see following messages
```
Scraping Started
Scraping Done
Saving Data in Database
Data Saved in Database
```
This mean that the project has succeesfully scraped data and stored in postgresql. You can use pgadmin to view the data.

### Project Structure
Project has 3 packages.

#### src
This package has following 3 files:
- **main.py**- This serves as the starting point of the project. Functions for scraping data and saving it into PostgreSQL are invoked from this file.
- **crawler.py** - This file contains complete scraping code.
- **cleaning_text.py**- Here, you'll find functions essential for cleaning and transforming text before it's loaded into the database.
  
#### db
This package comprises the following two files:
- **connection.py** -  This file facilitates the establishment of a connection with the database. It contains the connection string, allowing for adjustments to the host or database name if necessary.
- **models.py** - Here, you'll find the schema for the database, defining the structure of the tables and their relationships.

#### tests
This is a testing module, here you will find test cases for all the modules.
- **crawler_tests.py** - Contain tests for crawler
- **db_tests.py** - Conntain tests for data insertion



  
