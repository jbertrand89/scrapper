import argparse
from selenium import webdriver

from src.query_image_scraper import QueryImageScraper


# Put the path for your ChromeDriver here
CHROME_DRIVER_PATH = 'webdriver/chromedriver'
FIREFOX_DRIVER_PATH = 'webdriver/geckodriver'


def parse_arguments():
    """ Parses all the argument of the command line.

    :return: the args
    """
    argparser = argparse.ArgumentParser(
        description="Scrapper arguments.")

    argparser.add_argument(
        '-n',
        '--number_to_fetch',
        type=int,
        help="path of the data folder.",
        default=10)

    argparser.add_argument(
        '-q',
        '--query_name',
        help="whether you want to normalize the dataset",
        default="dog")

    argparser.add_argument(
        '-i',
        '--data_path',
        help="path of the data folder.",
        default="data")

    argparser.add_argument(
        '-b',
        '--browser_name',
        help="browser name",
        default="firefox")

    return argparser.parse_args()


def main():

    # Get the command line arguments
    arguments = parse_arguments()

    # Instantiate the webdriver
    if arguments.browser_name == "chrome":
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    else:
        driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH)

    query_image_scraper = QueryImageScraper(
        driver, arguments.query_name, arguments.number_to_fetch, arguments.data_path)
    query_image_scraper.download_images()

    driver.quit()


if __name__ == "__main__":

    main()
