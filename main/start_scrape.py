# -*- coding: utf-8 -*-
#
# Start scraping data.
#
# ------------------------------------------------

# imports
# -------
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType

from time import sleep


# Declare Constants
# -----------------
JOBS_LIST = []
NUM_JOBS = []


class ElementNotFound(Exception):

    __version_error_parser__ = 1.0
    __allow_update__ = False

    """

    Raise an Element not found error

    """
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

class JobNotFound(Exception):

    __version_error_parser__ = 1.0
    __allow_update__ = False

    """

    Raise a Job Not found error

    """
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


def get_proxies():

    """

    :return:
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

def start_browser(url):

    """

    Initialize the browser with chrome, we can extend this down the road to other browsers

    Arguments:
         url (String): the url for the host website to scrape data from.

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

    # TODO: add this as an argument parser for other folks and their chrome driver executable.
    driver = webdriver.Chrome(executable_path = "/Users/sulimansharif/Downloads/chromedriver_74")
                              # desired_capabilities=capabilities)
    driver.wait = WebDriverWait(driver, 10)
    login(driver, "swifter_scraper@outlook.com", "swifter1")

    return driver


def login(driver, username, password):

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

# Start search at home page then filter job listings
def start_search(browser, job, location):

        """

        Initializes the search and parses the html of the search results into the parse_html function.

        Arguments:
            browser (Object): the initialize chrome browser with the previous set driver.
            job (String): the job title we would like to search for.
            location (String): where in the world would we want to search the job data for.

        Returns:
            jobs (Array): the list of jobs for that page number to be parsed.

        Exceptions:
            Element Not Found if the element isn't found from the selenium driver for whatever reason


        """
        try:
            # to make it think we are human we need sleep statements.
            sleep(3)
            keyword_elem = browser.find_element_by_class_name("keyword")
            sleep(3)
            keyword_elem.send_keys(job)
            sleep(3)
            # There is some spacing between the two search boxes in Glassdoor but this isn't necessary.
            keyword_elem.send_keys(Keys.TAB)
            keyword_elem.send_keys(Keys.TAB)
            location_elem = browser.find_element(by=By.ID, value='sc.location')
            location_elem.clear()

            if not location_elem.is_displayed():
                try:
                    location_elem = browser.find_elements(By.CLASS_NAME, 'loc')
                    location_elem.clear()
                except ElementNotFound:
                    print('Element Not Found')

            sleep(3)
            location_elem.send_keys(location)
            search_elem = browser.find_element_by_class_name("gd-btn-mkt")
            search_elem.click()

            for page_num in range(30):
                job_num = len(NUM_JOBS)
                jobs = parse_html(browser.page_source, job_num)
                page_num = browser.find_element(By.CLASS_NAME, 'next')
                page_num.click()
                sleep(3)

        except ElementNotFound:
            print('Element not found')

        return jobs


# TODO: turn this into a file writer class that can support more than CSV, for now we need the data in any format.
def write_to_file(JOBS_LIST, filename):
    """

    Arguments:
        JOBS_LIST (Array): the list of the search results.
        filename (String): the name of the file the user defines.

    """
    with open(filename, 'a', errors='ignore') as csvfile:
        fieldnames = ['Job Number', 'Title', 'Company', 'Location', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in JOBS_LIST:
            writer.writerow(row)


def parse_html(html, job_num):

    """

    Parse HTML data and append it to the jobs list.

    TODO: this function will vary the most dependent on the type of data the host site has currently.

    Arguments:
         html (String): the data of the html to be parsed.
         job_num (String): the page number of jobs we searching for.

    """

    base_url = 'https://www.glassdoor.com'
    soup = BeautifulSoup(html, 'html.parser')
    job_titles = soup.find_all('div', attrs={'class':'flexbox jobTitle'})
    for a in job_titles:
        try:
            next_listing = a.findNext('a',attrs={'class' : 'jobLink'})
            title = next_listing.text
            list_url = next_listing['href']

            company_listing = a.findNext('div', attrs={'class' : 'flexbox empLoc'})
            next_company = company_listing.findNext('div')
            company = next_company.text
            company = company.replace(u'\xa0','').strip()
            company = company.replace(u'\n\n\n\n','').strip()

            job_num += 1
            NUM_JOBS.append(job_num)

        except JobNotFound:
            print("Error can't find job listing")

        # Convert company to string then split and make new key/value 'Location'
        # TODO: weird edge case to revisit.
        try:
            company = str(company)
            company, location = company.split('–')
        except:
            print("Can't change company string")

        # Add job data to JOBS_LIST
        job_info = {
                'Job Number' : job_num,
                'Title' : title,
                'Company' : company,
                'Location' : location,
                'URL' : base_url + list_url
            }

        JOBS_LIST.append(job_info)

    return JOBS_LIST
