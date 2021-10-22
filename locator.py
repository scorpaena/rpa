ALL_AGENCIES = {
    'Department_of_Agriculture': '/div/div[1]/div[1]/div/div/div/a',
    'Department_of_Commerce': '/div/div[1]/div[2]/div/div/div/a',
    'Department_of_Defense': '/div/div[1]/div[3]/div/div/div/a',
    'Department_of_Health_and_Human_Services': '/div/div[2]/div[1]/div/div/div/a',
    'Department_of_the_Interior': '/div/div[2]/div[2]/div/div/div/a',
    'Department_of_Justice': '/div/div[2]/div[3]/div/div/div/a',
    'Department_of_Labor': '/div/div[3]/div[1]/div/div/div/a',
    'Department_of_State': '/div/div[3]/div[2]/div/div/div/a',
    'Department_of_the_Treasury': '/div/div[3]/div[3]/div/div/div/a',
    'Social_Security_Administration': '/div/div[4]/div[1]/div/div/div/a',
    'Department_of_Education': '/div/div[4]/div[2]/div/div/div/a',
    'Department_of_Energy': '/div/div[4]/div[3]/div/div/div/a',
    'Environmental_Protection_Agency': '/div/div[5]/div[1]/div/div/div/a',
    'Department_of_Transportation': '/div/div[5]/div[2]/div/div/div/a',
    'General_Services_Administration': '/div/div[5]/div[3]/div/div/div/a',
    'Department_of_Homeland_Security': '/div/div[6]/div[1]/div/div/div/a',
    'Department_of_Housing_and_Urban_Development': '/div/div[6]/div[2]/div/div/div/a',
    'National_Aeronautics_and_Space_Administration': '/div/div[6]/div[3]/div/div/div/a',
    'Office_of_Personnel_Management': '/div/div[7]/div[1]/div/div/div/a',
    'Small_Business_Administration': '/div/div[7]/div[2]/div/div/div/a',
    'Department_of_Veterans_Affairs': '/div/div[7]/div[3]/div/div/div/a',
    'US_Agency_for_International_Development': '/div/div[8]/div[1]/div/div/div/a',
    'US_Army_Corps_of_Engineers': '/div/div[8]/div[2]/div/div/div/a',
    'National_Archives_and_Records_Administration': '/div/div[8]/div[3]/div/div/div/a',
    'National_Science_Foundation': '/div/div[9]/div[1]/div/div/div/a',
    'Nuclear_Regulatory_Commission': '/div/div[9]/div[2]/div/div/div/a'
}


URL = "https://itdashboard.gov"

DIVE_IN_BUTTON = '//*[@id="node-23"]/div/div/div/div/div/div/div/a'

AGENCIES_TILES = '//*[@id="agency-tiles-widget"]'

AGENCY_BUTTON = f'{AGENCIES_TILES}{ALL_AGENCIES["National_Science_Foundation"]}'

INVESTMENTS_TABLE = '//*[@id="investments-table-object"]'

TABLE_PAGINATION_BUTTON = '//*[@id="investments-table-object_paginate"]/span/a'

PDF_FILE_LINK = '//*[@id="business-case-pdf"]/a'