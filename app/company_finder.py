import requests
from app.logger import Logger
from utils.find_digits_in_string import digits_of_string
from dotenv import load_dotenv
import os
import time


def _api_get_requester(base_url, api_key, payload):
    """
    :param base_url: string - which specifies the url need to send get request to
    :param api_key: string - this is the api key specific to this application which is from companies house.
    :param payload: dict - this is the dictionary with payload variables search_term, items_per_page=100, start_index
                   and restrictions.
    :return: api call response json
    """
    logger = Logger('api_get_requester').set_logger()
    try:
        response = requests.get(base_url, auth=(api_key, ''), params=payload)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error("Timeout error! Will sleep for a minute and retry")
        time.sleep(60)
        try:
            response = requests.get(base_url, auth=(api_key, ''), params=payload)
        except requests.exceptions.Timeout:
            logger.error("Another timeout error!")
            raise SystemExit("Seems like something wrong with the server. You need to retry later")
    except requests.exceptions.TooManyRedirects:
        logger.error("The URL is not working!")
        raise SystemExit("Please try another BASE_URL")
    except requests.exceptions.HTTPError as err:
        logger.error("URL not found!")
        raise SystemExit(err)
    except requests.exceptions.RequestException as err:
        logger.error("Something is very wrong!")
        raise SystemExit(err)
    return response.json()


def search_companies(search_term, items_per_page=100, start_index=0, restrictions=None):
    """
    :param search_term: string - The term being searched for
    :param items_per_page: integer - The number of search results to return per page.
    :param start_index: integer - The index of the first result item to return.
    :param restrictions: string - Enumerable options to restrict search results. Space separate multiple restriction
           options to combine functionality.
    :return: List of dictionaries - all matched companies with search term and their details:
    https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/resources/companysearch?v=latest
    """
    base_url = os.environ.get('BASE_URL')
    logger = Logger('search_companies').set_logger()
    payload = {'q': search_term, 'items_per_page': items_per_page, 'start_index': start_index
               , 'restrictions': restrictions}
    logger.info(f"Variables are set as - search term: '{search_term}', items per page: {items_per_page},start index: "
                f"{start_index} and restrictions : '{restrictions}'.")
    load_dotenv()
    api_key = os.getenv('api_key')
    logger.info(f"Calling url: {base_url}")
    companies_batch_results = _api_get_requester(base_url=base_url, api_key=api_key, payload=payload)
    num_total_results = companies_batch_results['total_results']
    logger.info(f"API call returned {num_total_results} companies.")
    list_of_companies_details = companies_batch_results['items']
    start_index += items_per_page
    number_of_api_calls = 1
    while num_total_results > start_index:
        payload['start_index'] = start_index
        logger.info(f"Start index changed to: {start_index} and sending another get request")
        companies_batch_results = _api_get_requester(base_url=base_url, api_key=api_key, payload=payload)
        list_of_companies_details.extend(companies_batch_results['items'])
        start_index += items_per_page
        number_of_api_calls += 1
        if number_of_api_calls > 599:
            logger.info(f"Already sent {number_of_api_calls} requests! I'm tired! Need to sleep for 5 minutes -:")
            time.sleep(300)
    list_of_companies_details = [(i.get('company_number'), i.get('title'), i.get('company_type'),
                                  i.get('date_of_creation'), i.get('date_of_cessation'),
                                  i['address'].get('address_line_1'), i['address'].get('premises'),
                                  i['address'].get('locality'), i['address'].get('country'),
                                  i['address'].get('postal_code'), i.get('company_status'),
                                  i.get('description_identifier')[0], digits_of_string(i['address'].get('premises')),
                                  ) for i in list_of_companies_details]
    return list_of_companies_details


