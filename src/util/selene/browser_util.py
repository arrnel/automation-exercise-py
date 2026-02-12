import logging

from selene import browser


def close_browser_tab(tab_number: int, switch_tab_number: int = 0):

    logging.info(f"Closing browser tab: {tab_number}")
    child = browser.driver.window_handles[1]
    browser.driver.switch_to.window(child)
    browser.driver.close()

    logging.info(f"Switch to tab: {switch_tab_number}")
    current_tab = browser.driver.window_handles[switch_tab_number]
    browser.driver.switch_to.window(current_tab)
