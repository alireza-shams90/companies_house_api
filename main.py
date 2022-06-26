from app.company_finder import search_companies
from app.logger import Logger
from os import environ
from jinja2 import Template
import app.sql_query as s
from app.database import Sqlite


def replace_variables_text(text, **params):
    """
    Use Jinja to replace the variables
    :param text: statement that needs to be run
    :param params: dictionary of params to sub in the text
    :return: a converted Text
    """
    templated_string = ''
    if text:
        jinja_template = Template(text)
        templated_string = jinja_template.render(params)
    return templated_string


if __name__ == "__main__":
    logger = Logger('main_app').set_logger()
    logger.info("---------Process started------------")
    search_term = environ.get('SEARCH_TERM')
    items_per_page = int(environ.get('ITEMS_PER_PAGE'))
    start_index = int(environ.get('START_INDEX'))
    companies = search_companies(search_term=search_term, items_per_page=items_per_page, start_index=start_index)
    parms_dict = {'table_name': environ.get('TABLE_NAME')
                  , 'search_term': environ.get('SEARCH_TERM'),
                  }
    drop_table_query = replace_variables_text(s.drop_table_query, **parms_dict)
    create_table_query = replace_variables_text(s.create_table_query, **parms_dict)
    insert_query = replace_variables_text(s.insert_query, **parms_dict)
    db = Sqlite('workflow/' + environ.get('DATABASE_NAME') + '.db')
    db_output = db.execute(drop_table_query)
    db_output = db.execute(create_table_query)
    db.insert(insert_query, companies)
    total_num_companies = replace_variables_text(s.total_num_companies, **parms_dict)
    db_output = db.execute(total_num_companies)
    logger.info(f"Total number of companies with term '{search_term}': {db_output[0][0]}")
    db.close_connection()
    logger.info("---------Process completed------------")

