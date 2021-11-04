import os

from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from RPA.Excel.Files import Files

from SeleniumLibrary.errors import ElementNotFound

browser_lib = Selenium()
file_system = FileSystem()
xls_file = Files()

SELECTED_AGENCY = os.environ.get('agency', default='National_Science_Foundation')


class FileProcessor:

    path = f'{os.getcwd()}\\output'

    def set_download_folder_in_current_directory(self):
        file_system.create_directory(self.path)
        browser_lib.set_download_directory(self.path)

    def save_agencies_data_to_xls(self, data_generator):
        xls_file.create_workbook(f'{self.path}/{SELECTED_AGENCY}.xlsx')
        xls_file.rename_worksheet('Sheet', 'Agencies')
        row = 0
        for data in data_generator:
            row += 1
            for column in range(len(data)):
                xls_file.set_cell_value(row=row, column=column + 1, value=data[column])
        xls_file.save_workbook()

    def save_investments_table_data_to_xls(self, data_generator):
        xls_file.create_worksheet('Individual Investments')
        for data in data_generator:
            xls_file.set_cell_value(row=data['row'], column=data['column'], value=data['value'])
        xls_file.set_active_worksheet(xls_file.list_worksheets()[0])
        xls_file.save_workbook()
        xls_file.close_workbook()


class ITDashBoardWebDataScraper:

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
    AGENCY_LOCATOR = ALL_AGENCIES[f'{SELECTED_AGENCY}']
    AGENCY_BUTTON = f'{AGENCIES_TILES}{AGENCY_LOCATOR}'

    INVESTMENTS_TABLE = '//*[@id="investments-table-object"]'
    INVESTMENTS_TABLE_INFO = '//*[@id="investments-table-object_info"]'

    PDF_FILE_LINK = '//*[@id="business-case-pdf"]/a'

    TABLE_SHOW_50_ENTRIES_BUTTON = '//*[@id="investments-table-object_length"]/label/select/option[3]'

    TABLE_NEXT_BUTTON = '//*[@id="investments-table-object_next"]'

    TABLE_FIRST_BUTTON = '//*[@id="investments-table-object_first"]'

    INVESTMENTS_TABLE_ROWS_SHOWN = 50

    file_processor = FileProcessor

    def _click_element(self, locator):
        browser_lib.wait_until_element_is_visible(locator, timeout=30)
        browser_lib.click_element_when_visible(locator)

    def _wait_until_element_is_ready(self, locator):
        browser_lib.wait_until_element_is_visible(locator, timeout=30)
        browser_lib.wait_until_page_contains_element(locator, timeout=30)

    def _click_next_table_pagination_button(self):
        self._click_element(f'{self.TABLE_NEXT_BUTTON}')

    def _click_first_table_pagination_button(self):
        self._click_element(f'{self.TABLE_FIRST_BUTTON}')

    def _get_investments_table_info(self):
        browser_lib.wait_until_page_contains_element(self.INVESTMENTS_TABLE, timeout=30)
        return browser_lib.get_text(self.INVESTMENTS_TABLE_INFO)

    def _is_last_page_of_investments_table(self):
        table_info = self._get_investments_table_info()
        entries_start = table_info.split()[3]
        entries_end = table_info.split()[5]
        return entries_start == entries_end

    def _get_investments_table_total_entries(self):
        table_info = self._get_investments_table_info()
        text = table_info.split()[-2]
        value = int(text.replace(',', ''))
        return (text, value)

    def _get_investments_table_entries(self):
        table_info = self._get_investments_table_info()
        start = int(table_info.split()[1].replace(',', ''))
        stop = int(table_info.split()[3].replace(',', ''))
        rows = stop - start + 1
        return rows

    def _click_show_50_entries_button(self):
        self._click_element(self.TABLE_SHOW_50_ENTRIES_BUTTON)
        total_entries = self._get_investments_table_total_entries()
        table_info = f'Showing 1 to {self.INVESTMENTS_TABLE_ROWS_SHOWN} of {total_entries[0]} entries'
        if total_entries[1] < self.INVESTMENTS_TABLE_ROWS_SHOWN:
            table_info = f'Showing 1 to {total_entries[0]} of {total_entries[0]} entries'
        browser_lib.wait_until_element_contains(self.INVESTMENTS_TABLE_INFO, text=table_info, timeout=30)

    def _get_investments_table_dimensions(self):
        table_locator = self.INVESTMENTS_TABLE
        self._wait_until_element_is_ready(table_locator)
        rows_number = browser_lib.get_element_count(f'{table_locator}/tbody/tr')
        columns_number = browser_lib.get_element_count(f'{table_locator}/tbody/tr/td') // rows_number
        return (rows_number, columns_number)

    def _get_tile_elements_count(self):
        agencies_locator = self.AGENCIES_TILES
        self._wait_until_element_is_ready(agencies_locator)
        blocks = browser_lib.get_element_count(f'{agencies_locator}/div/div')
        tiles_in_block = browser_lib.get_element_count(f'{agencies_locator}/div/div[1]/div')
        return (blocks, tiles_in_block)

    def _pdf_file_link_generator(self):
        browser_lib.switch_browser('main')
        self._click_first_table_pagination_button()
        while True:
            table_entries = self._get_investments_table_entries()
            for row in range(1, table_entries + 1):
                browser_lib.switch_browser('main')
                file_locator = f'{self.INVESTMENTS_TABLE}/tbody/tr[{row}]/td[1]/a'
                try:
                    yield browser_lib.get_element_attribute(file_locator, attribute='href')
                except ElementNotFound:
                    continue
            if self._is_last_page_of_investments_table():
                break
            self._click_next_table_pagination_button()

    def _download_pdf_file(self, link):
        file_name = f'{link.split("/")[-1]}.pdf'
        browser_lib.switch_browser('download_pdf')
        browser_lib.go_to(link)
        browser_lib.wait_until_page_contains_element(self.PDF_FILE_LINK, timeout=30)
        browser_lib.click_link(self.PDF_FILE_LINK)
        file_system.wait_until_created(f'{self.file_processor.path}/{file_name}', timeout=30)

    def open_website(self):
        browser_lib.open_available_browser(self.URL, alias='main')

    def click_dive_in_button(self):
        self._click_element(self.DIVE_IN_BUTTON)

    def click_agency_button(self):
        self._click_element(self.AGENCY_BUTTON)

    def agencies_data_generator(self):
        blocks, tiles_in_block = self._get_tile_elements_count()
        for block in range(1, blocks + 1):
            for tile in range(1, tiles_in_block + 1):
                try:
                    base = f'{self.AGENCIES_TILES}/div/div[{block}]/div[{tile}]/div/div/div/div[1]/a'
                    name = browser_lib.get_text(f'{base}/span[1]')
                    amount = browser_lib.get_text(f'{base}/span[2]')
                    yield (name, amount)
                except ElementNotFound:
                    break

    def download_pdf_from_investments_table(self):
        browser_lib.open_available_browser(alias='download_pdf')
        for link in self._pdf_file_link_generator():
            self._download_pdf_file(link)
        browser_lib.switch_browser('main')

    def investments_table_data_generator(self):
        self._click_show_50_entries_button()
        data = {}
        empty_rows_amount = 2
        excel_rows_offset = 0
        while True:
            rows_number, columns_number = self._get_investments_table_dimensions()
            for row in range(1, rows_number + 1):
                for column in range(1, columns_number + 1):
                    value = browser_lib.get_table_cell(self.INVESTMENTS_TABLE, row + empty_rows_amount, column)
                    data['row'] = row + excel_rows_offset
                    data['column'] = column
                    data['value'] = value
                    yield data
            if self._is_last_page_of_investments_table():
                break
            excel_rows_offset += self.INVESTMENTS_TABLE_ROWS_SHOWN
            self._click_next_table_pagination_button()

    def close_all_browsers(self):
        browser_lib.close_all_browsers()
