# -*- coding: utf-8 -*-
#
# Main module for initializing swifter
#
# ------------------------------------------------


from start_scrape import start_browser, start_search, write_to_file
from helper import start_browser

job = 'Software Developer'
location = 'Austin, TX'

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Define what data you would like to scrape')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    output_filename = 'jobs.csv'
    url = 'https://www.glassdoor.com/index.htm'

    # Start driver and return driver object named 'browser'
    # Params: URL
    browser = start_browser(url)

    # Start search and return job_list
    # Params: browser, job, location
    job_list = start_search(browser, job, location)

    # Write to csv file
    # Params: job_list, output_filename
    write_to_file(job_list, output_filename)

