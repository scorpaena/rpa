from utils import ITDashBoardScraper

scraper = ITDashBoardScraper()

scraper.set_download_folder_in_current_directory()
scraper.open_website()
scraper.click_dive_in_button()
data_generator = scraper.agencies_data_generator()
scraper.save_agencies_data_to_xls(data_generator)
agency_page_url = scraper.click_agency_button_and_get_its_url()
scraper.download_pdf_from_href_link(agency_page_url)
data_generator = scraper.paginated_table_data_generator()
scraper.save_paginated_table_data_to_xls(data_generator)
