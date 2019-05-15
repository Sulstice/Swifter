
## Swifter (The Data Cleaner & Scraper we all <3)
![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)


**Background:** A unique look into scraping data for jobs, the motivation behind this project is to gain 
an outlook about talent pool within a city. In combination with not only the talent pool here but what is up and coming in 
the pipelines of universities. Glassdoor was chosen because of it's rapid growth as a household name in job searching. 
Monster, Indeed, and others have become a little antiquated. It's main competitor is LinkedIn in terms of job searching.


**Goal:** Come up with metrics on what a city's talent pool is looking for and determine what is needed down the pipeline. 

Using the method of scraping (name idea came from the company swiffer and myself scraping dirt off a balcony)    
![PMI IMAGE](./imgs/swifter.jpg)

### Prerequisites - Browsers

As of right now this script only supports the browser Google Chrome 

This script also requires the chromedriver. If you are using a chrome driver other than version 74, Google chrome's driver
is placed into the drivers directory. Feel free to modify the script if so to call the correct driver. 

Drivers for google chrome can be found here: [Chrome Driver](http://chromedriver.chromium.org/downloads)

### Prerequisites - Language

What things you need to install the package

```

python3

```

If you do not have python3 installed on your machine, please refer to this guide on how to install: [Python Installation](https://realpython.com/installing-python/)



### Installing

1st step is to clone the github repository  

```

git clone https://github.com/Sulstice/Swifter.git

```

Next either create a venv or use the python3 module you have to install the requirements.txt into running Swifter


```

python -m pip install -r requirements.txt

```


## Running the Swifter Program

After successful installion of Swifter you can run the code using these options:

```
Example

python -m main/swifter.py -j Software Developer -c Austin -s TX

```

### Set attributes of an option
Options of the Swifter Application:
- `--job | -j`: Position that the user is searching for. Default: `str`
- `--city | -c`: City that the user is searching for. Default: `str`
- `--state | -s`: State that the user is searching for. Default: `str`
- `--chromedriver | -c`: Chromedriver executable path. Default: `str` path to the chromedriver 74 inside the repo. 
- `--output_file_path | -p`: File path to the CSV returned from the scrape data. Default: `str` outputs to data.csv

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Suliman Sharif** - *Initial work* - [Sulstice](https://github.com/Sulstice)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Disclaimer

While scraping can sometimes be used as a legitimate way to access all kinds of data on the internet, it’s also important to consider the legal implications. 
There are many cases where scraping data may be considered illegal, or open you to the possibility of being sued. 
Similar to using a firearm, some uses of web scraping techniques can be used for utility or sport, while others can land you in jail. 
I am not a lawyer, but you should be smart about how you use it.

For now the code is updated with a version using the swifter-email into glassdoor. 
As of right now there is no blocker in using that emails since it is primarily for swifter purposes. As the user base will 
grow, if so, then swifter will be taken down in the adoption of user-based emails. 

## Acknowledgments


