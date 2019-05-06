# -*- coding: utf-8 -*-
#
# Main module for initializing swifter
#
# ------------------------------------------------


# imports
# -------
import requests, os
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver


from .start_scrape import start_browser, start_search, write_to_file, get_proxies

job = 'Lab Technician'
location = 'Austin, TX'

if __name__ == '__main__':
    output_filename = 'jobs.csv'
    url = 'https://www.glassdoor.com/index.htm'
    proxies = get_proxies()

    # Start driver and return driver object named 'browser'
    # Params: URL
    browser = start_browser(url)

    # Start search and return job_list
    # Params: browser, job, location
    job_list = start_search(browser, job, location)

    # Write to csv file
    # Params: job_list, output_filename
    write_to_file(job_list, output_filename)

