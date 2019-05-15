# -*- coding: utf-8 -*-
#
# Helper Functions
#
# ------------------------------------------------

# imports
# -------
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ElementNotFound(Exception):

    __version_error_parser__ = 1.0
    __allow_update__ = False

    """

    Raise an Element not found error

    """
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

def get_proxies():

    """

    Returns a list of proxies from free-proxy list that are readily available for the scraper

    Borrowed from ScrapeStorm

    """
    from lxml.html import fromstring
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

# @get_proxies Handle the get proxies for log in info and requests down stream.
def login_glassdoor(driver, username, password):

    """

    The purpose of this function is to log into the site we are trying to access.

    Arguments:
        driver (Object): the Chrome driver object, for now I am just using chrome but we can extend this an option
        username (String): the username of the account we are logging into. TODO: CHANGE THIS IMMEDIATELY TO NOT BE HARDCODED
        password (String): the password of the account we are logging into. TODO: CHANGE THIS IMMEDIATELY TO NOT BE HARDCODED

    Exceptions:
        TimeoutException: if the login and password failed.

    """

    import time
    driver.get("http://www.glassdoor.com/profile/login_input.htm")
    try:
        user_field = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "userEmail")))
        pw_field = driver.find_element_by_id("userPassword")
        login_button = driver.find_element_by_class_name("gd-ui-button")
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        time.sleep(1)
        pw_field.send_keys(password)
        time.sleep(1)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")

def start_browser(url, chromedriver_path):

    """

    Initialize the browser with chrome, we can extend this down the road to other browsers

    Arguments:
         url (String): the url for the host website to scrape data from.
         chromedriver_path (String): chrome driver executable path.

    Returns:
        driver (object): the chrome driver object we are initiating.

    """

    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins-discovery')

    # Tackle this in a later commit, but need to jump through a loop of proxies to route through.
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = "ip_addr:port"
    # prox.socks_proxy = "ip_addr:port"
    # prox.ssl_proxy = "ip_addr:port"
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(executable_path=chromedriver_path)
    # desired_capabilities=capabilities)
    driver.wait = WebDriverWait(driver, 10)
    login_glassdoor(driver, "swifter_scraper@outlook.com", "swifter1")

    return driver
