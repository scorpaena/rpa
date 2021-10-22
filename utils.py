import time
import os

from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from RPA.Excel.Files import Files

from SeleniumLibrary.errors import ElementNotFound

browser_lib = Selenium()
file_system = FileSystem()
xls_file = Files()

path = f'{os.getcwd()}/download'

def open_website(url):
    return browser_lib.open_available_browser(url)


def click_element(locator):
    browser_lib.wait_until_element_is_visible(locator, timeout=30)
    browser_lib.click_element_when_visible(locator)


def get_element_url_and_click_element(locator):
    browser_lib.wait_until_element_is_visible(locator, timeout=30)
    browser_lib.wait_until_page_contains_element(locator, timeout=30)
    href = browser_lib.get_element_attribute(locator, attribute='href')
    browser_lib.click_element_when_visible(locator)
    return href


def set_download_folder_in_current_directory(path=path):
    file_system.create_directory(path)
    browser_lib.set_download_directory(path)
    return path


def number_of_pagination_buttons(pagination_button_locator):
    browser_lib.wait_until_element_is_visible(pagination_button_locator, timeout=30)
    return browser_lib.get_element_count(pagination_button_locator)


def click_next_pagination_button(pagination_button_locator):
    click_element(pagination_button_locator)


def get_table_rows_columns_number(table_locator):
    browser_lib.wait_until_element_is_visible(table_locator, timeout=30)
    browser_lib.wait_until_page_contains_element(table_locator, timeout=30)
    rows_number = browser_lib.get_element_count(f'{table_locator}/tbody/tr')
    columns_number = browser_lib.get_element_count(f'{table_locator}/tbody/tr/td') // rows_number
    return (rows_number, columns_number)


def get_tile_elements_count(agencies_locator):
    browser_lib.wait_until_element_is_visible(agencies_locator, timeout=30)
    browser_lib.wait_until_page_contains_element(agencies_locator, timeout=30)
    blocks = browser_lib.get_element_count(f'{agencies_locator}/div/div')
    tiles = browser_lib.get_element_count(f'{agencies_locator}/div/div/div')
    tiles_in_block = browser_lib.get_element_count(f'{agencies_locator}/div/div[1]/div')
    return (blocks, tiles, tiles_in_block)


def save_agencies_data_to_xls(agencies_locator, path):
    xls_file.create_workbook(f'{path}/template.xls')
    xls_file.rename_worksheet('Sheet', 'Agencies')
    blocks, _ , tiles_in_block = get_tile_elements_count(agencies_locator)
    excel_row = 0
    try:
        for block in range(1, blocks + 1):
            for tile in range(1, tiles_in_block + 1):
                base = f'{agencies_locator}/div/div[{block}]/div[{tile}]/div/div/div/div[1]/a'
                name = browser_lib.get_text(f'{base}/span[1]')
                amount = browser_lib.get_text(f'{base}/span[2]')
                xls_file.set_cell_value(row=tile + excel_row, column=1, value=name)
                xls_file.set_cell_value(row=tile + excel_row, column=2, value=amount)
                xls_file.save_workbook()
            excel_row += 3
    except ElementNotFound:
        return


def number_of_locators_with_pdf(table_locator):
    browser_lib.wait_until_element_is_visible(table_locator, timeout=30)
    rows_number, _ = get_table_rows_columns_number(table_locator)
    number_of_locators = 0
    for row in range(1, rows_number + 1):
        file_locator = f'{table_locator}/tbody/tr[{row}]/td[1]/a'
        try:
            browser_lib.get_element_attribute(file_locator, attribute='href')
            number_of_locators += 1
        except ElementNotFound:
            continue
    return number_of_locators


def download_pdf_from_href_link(table_locator, page_url, path, link_locator='//*[@id="business-case-pdf"]/a'):
    number_of_locators = number_of_locators_with_pdf(table_locator)
    for row in range(1, number_of_locators + 1):
        browser_lib.wait_until_page_contains_element(table_locator, timeout=30)
        file_locator = f'{table_locator}/tbody/tr[{row}]/td[1]/a'
        file_href = browser_lib.get_element_attribute(file_locator, attribute='href')
        if file_href is not None:
            file_name = f'{file_href.split("/")[-1]}.pdf'
            browser_lib.click_link(file_locator)
            browser_lib.wait_until_page_contains_element(link_locator, timeout=30)
            browser_lib.click_link(link_locator)
            file_system.wait_until_created(f'{path}/{file_name}', timeout=30)
            browser_lib.close_browser()
            open_website(page_url)


def save_paginated_table_data_to_xls(table_locator, pagination_button_locator):
    xls_file.create_worksheet('Individual Investments')
    number_of_buttons = number_of_pagination_buttons(pagination_button_locator)
    paginated_rows_number = 0
    empty_row = 1
    for number in range(1, number_of_buttons + 1):
        click_next_pagination_button(f'{pagination_button_locator}[{number}]')
        time.sleep(10)
        rows_number, columns_number = get_table_rows_columns_number(table_locator)
        for row in range(1, rows_number + 1):
            for column in range(1, columns_number + 1):
                value = browser_lib.get_table_cell(f'{table_locator}', row + empty_row, column)
                xls_file.set_cell_value(row + paginated_rows_number, column, value)
        empty_row = 2
        paginated_rows_number += 10
    xls_file.save_workbook()
