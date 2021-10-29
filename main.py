from utils import ITDashBoardWebDataScraper, FileProcessor

scraper = ITDashBoardWebDataScraper()
file_processor = FileProcessor()

file_processor.set_download_folder_in_current_directory()
scraper.open_website()
scraper.click_dive_in_button()
data_generator = scraper.agencies_data_generator()
file_processor.save_agencies_data_to_xls(data_generator)
scraper.click_agency_button()
data_generator = scraper.investments_table_data_generator()
file_processor.save_investments_table_data_to_xls(data_generator)
scraper.download_pdf_from_investments_table()
scraper.close_all_browsers()