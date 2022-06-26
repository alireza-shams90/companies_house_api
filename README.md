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
