# companies_house_api_call

## Summary
An API caller to companies house API with the ability of storing results into database.

### Companies house API
* `main.py`
   * The main.py module contains the main entry point(search for a term in companie's name).
 
 ### app
* `company_finder.py`
   * Sending requests to companie's house API and searching for a specific term in the companie's name. Returning the results of this search.
* `database.py`
   * DB to store the results of API calls. 
* `logger.py`
   * The class for setting of a logger using a common format.
* `sql_query.py`
   * Place to hold the sql scripts. 

 ### utils
 * `find_digits_in_string.py`
   * A utility function to find digits inside a string.

## Running the application
This application can be ran via Docker. All the variables are passed through docker-compose.yml file:
* `SEARCH_TERM`: This is the term that application looking for e.g. sono
* `BASE_URL`: The base URL of companies house REST API e.g. https://api.company-information.service.gov.uk/search/companies
* `ITEMS_PER_PAGE`: The number of search results to return per page.
* `START_INDEX`: The index of the first result item to return.
* `TABLE_NAME`: Name of the table to store the search results e.g. companies - name and address 
* `DATABASE_NAME`: Name of the database to store the data e.g. sonovate. As sqlite being used, this will be the database file name as well e.g. sonovate.db

After setting environment variables run :
```
docker-compose up --build
```
The output is saved to a db sqlite file called DATABASE_NAME.db which can be queried by selecting from the table TABLE_NAME.
