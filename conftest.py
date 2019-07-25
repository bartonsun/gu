from selenium import webdriver
import pytest
import os


@pytest.yield_fixture(scope='session')
def driver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', os.getcwd() + '/tmp')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/rtf')
    driver = webdriver.Firefox(
        executable_path='driver/geckodriver',
        firefox_profile=profile,
    )
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()
