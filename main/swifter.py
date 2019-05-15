# -*- coding: utf-8 -*-
#
# Main module for initializing swifter
#
# ------------------------------------------------


from glassdoor.start_scrape import start_search, write_to_file
from helper import start_browser

if __name__ == '__main__':

    import optparse

    # Parse Arguments
    parser = optparse.OptionParser(usage='usage: %prog [options] arguments')
    parser.add_option('-d', '--chromedriver',
                      action="store", dest="chromedriver",
                      help="the file path",  nargs='?')

    # Have the option to enumerate later.
    parser.add_option('-j', '--job',
                      action="store", dest="job",
                      help="enumerate all representations of file pass in options: True | False",
                      )

    parser.add_option('-c', '--city',
                      action="store", dest="city",
                      help="enumerate all representations of file pass in options: True | False",
                      )

    parser.add_option('-s', '--state',
                      action="store", dest="state",
                      help="enumerate all representations of file pass in options: True | False",
                      )

    parser.add_option('-p', '--output_file_path',
                      action="store", dest="output_file_path",
                      help="enumerate all representations of file pass in options: True | False",
                      nargs='?')

    options, args = parser.parse_args()

    # Raise Parser Errors if things are not found.
    if not options.job:
        parser.error('Job not given')

    if not options.city:
        parser.error('City not given')

    if not options.state:
        parser.error('State not given')


    # Handle Defaults
    if options.chromedriver:
        chromedriver_path = options.chromedriver
    else:
        chromedriver_path = ('main/drivers/chromedriver_74')


    if options.output_file_path:
        output_filename = options.output_file_path
    else:
        output_filename = 'jobs.csv'

    url = 'https://www.glassdoor.com/index.htm'

    # Start driver and return driver object named 'browser'
    # Params: URL
    browser = start_browser(url, chromedriver_path)

    # Start search and return job_list
    # Params: browser, job, location
    job_list = start_search(browser, options.job, str((options.city) + ", " + str(options.state)))

    # Write to csv file
    # Params: job_list, output_filename
    write_to_file(job_list, output_filename)

