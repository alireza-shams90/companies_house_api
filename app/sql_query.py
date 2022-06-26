
drop_table_query = "DROP TABLE IF EXISTS {{table_name}}"

create_table_query = " CREATE TABLE {{table_name}} (" \
             "  company_id  TEXT PRIMARY KEY" \
             ", company_name TEXT" \
             ", company_type TEXT" \
             ", date_of_creation TEXT" \
             ", date_of_cessation TEXT" \
             ", address_line_1 TEXT" \
             ", premises TEXT" \
             ", locality TEXT" \
             ", country TEXT" \
             ", postal_code TEXT" \
             ", company_status TEXT" \
             ", description_identifier TEXT" \
             ", premise_digits TEXT)"

insert_query = "insert into {{table_name}}" \
              "(company_id, company_name, company_type, date_of_creation, date_of_cessation, address_line_1, premises" \
              ", locality, country, postal_code, company_status, description_identifier, premise_digits)" \
              "values(?,?,?,?,?,?,?,?,?,?,?,?,?);"

total_num_companies = "select count(*) " \
                      "  from {{table_name}} " \
                      " where lower(company_name) like lower('%{{search_term}}%')"

active_companies = "select count(*) " \
                   "  from {{table_name}}" \
                   " where lower(company_name) like lower('%{{search_term}}%')" \
                   "   and lower(company_status) = 'active'"

avg_life_dissolved_companies = "select round(sum(julianday(date_of_cessation) - julianday(date_of_creation))/count(*)) " \
                               "  from {{table_name}}" \
                               " where lower(company_status) = 'dissolved'" \
                               "   and lower(company_name) like lower('%{{search_term}}%')"

first_lim_partnership_created = "select min(date_of_creation)" \
                              "  from {{table_name}}" \
                              " where lower(company_type) = 'limited-partnership'" \
                              "   and lower(company_name) like lower('%{{search_term}}%')"

companies_with_vate_in_name = "select company_name" \
                              "  from {{table_name}}" \
                              " where lower(company_name) like lower('%{{search_term}}%')" \
                              "   and lower(company_name) like '%vate%'"

sum_of_premises_digits_per_company_type = "select company_type" \
                                          "     , sum(cast(coalesce(premise_digits,'0') as decimal)) as sum_of_premises_digits" \
                                          "  from {{table_name}} " \
                                          " where lower(company_name) like lower('%{{search_term}}%') " \
                                          " group by company_type"


