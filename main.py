from locator import *
from utils import (
    set_download_folder,
    open_website,
    click_element,
    get_element_url_and_click_element,
    save_agencies_data_to_xls,
    save_paginated_table_data_to_xls,
    download_pdf_from_href_link,
)


def main():
    path = set_download_folder(path=PATH)
    open_website(url=URL)
    click_element(locator=DIVE_IN_BUTTON)
    save_agencies_data_to_xls(
        agencies_locator=AGENCIES_TILES,
        path=path
    )
    page_url = get_element_url_and_click_element(locator=AGENCY_BUTTON)
    download_pdf_from_href_link(
        table_locator=INVESTMENTS_TABLE,
        page_url=page_url,
        path=path
    )
    save_paginated_table_data_to_xls(
        table_locator=INVESTMENTS_TABLE,
        pagination_button_locator=TABLE_PAGINATION_BUTTON
    )


if __name__ == "__main__":
    main()
