import io
import os
from PIL import Image
import requests
import time

from src.google_image import GoogleImage
from src.google_images import GoogleImagesForLabel


class QueryImageScraper(object):
    """Scraper of google images from a query.
    """

    def __init__(self, driver, query, count_image_to_fetch, data_path):
        """Constructor.

        :param driver (webdriver) - webdriver from selenium library
        :param query (str) - query (example "dogs" "power line"
        :param count_image_to_fetch (int) - number of image to fetchxf
        :param data_path (str) - path of the data folder where to save the images.
        """
        self.driver = driver
        self.query = query
        self.total_count_image_to_fetch = count_image_to_fetch

        # Create the directory folder
        self._data_path = data_path
        self._label = self.query.replace(" ", "_")  # No space in the file names and folder
        self._image_path = os.path.join(data_path, self._label)
        os.makedirs(self._image_path, exist_ok=True)

        # Set to contain the downloaded urls to avoid saving duplicates
        self._downloaded_urls = set()

        # Constant parameters:
        self._number_click_on_more_results = 5  # number of times to click on more results
        self._progress_bar_step = 10
        self._sleep_between_interactions = 0.1
        self._sleep_between_scrolling = 0.2
        self._sleep_between_clicking_on_more_results = 0.5

    def download_images(self):
        """ Downloads self.total_image_count google images associate to self.query. The images are saved in
        data_path/label/. All the image information is saved in data_path/label.txt/
        """
        image_id = 0
        google_images = GoogleImagesForLabel(self._label, self._data_path)

        for url in self._fetch_image_urls():
            if image_id >= self.total_count_image_to_fetch:
                print(f"Found: {image_id} image links, done!")
                break

            google_image = self._save_image(url, image_id)
            if google_image is not None:
                google_images.add(google_image)
                image_id += 1

            if image_id % self._progress_bar_step == 0:
                print("Downloaded count {0} / {1}".format(image_id, self.total_count_image_to_fetch))

        # Save the auxiliary data
        aux_filename = google_images.get_filename()
        google_images.save(aux_filename)
        print("Saved auxiliary data in {}".format(aux_filename))

    def _fetch_image_urls(self):
        """ Fetches the urls of the images corresponding to self.query

        :return: iterator on the urls
        """

        # Google query
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # Load the page
        self.driver.get(search_url.format(q=self.query))

        results_start = 0
        while True:
            self._scroll_to_end(self._number_click_on_more_results)

            # get all image thumbnail results
            thumbnail_results = self.driver.find_elements_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)

            print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

            for img in thumbnail_results[results_start:number_results]:

                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(self._sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls
                actual_images = self.driver.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        url = actual_image.get_attribute('src')
                        if url in self._downloaded_urls:
                            continue
                        self._downloaded_urls.add(actual_image.get_attribute('src'))
                        yield url

            print("Found:", len(self._downloaded_urls), "image links, looking for more ...")

            # move the result startpoint further down
            if results_start == number_results:
                results_start = 0
            else:
                results_start = len(thumbnail_results)

    def _save_image(self, url, image_id):
        """ Saves the image from url into a file.

        :param url (str) - url of the image
        :param image_id (int) - image id. The image will be saved in <data_path>/<label>_<image_id>.png
        :return: (GoogleImage) - google image. If the image couldn't be saved, it will be None.
        """
        try:
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            google_image = GoogleImage(url, self._label, image_id)
            file_path = os.path.join(self._data_path, google_image.filename)
            with open(file_path, 'wb') as f:
                image.save(f, "PNG", quality=85)
        except Exception as e:
            return None

        return google_image

    def _scroll_to_end(self, number_click_on_more_results, number_of_scrolls=10):
        """Scrolls the webpage to get more elements to scrap.

        :param number_click_on_more_results (int) - number of call to more results
        :param number_of_scrolls (int) - number of scrolling
        """
        for __ in range(number_click_on_more_results):
            for __ in range(number_of_scrolls):
                # multiple scrolls needed to show all images
                self.driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(self._sleep_between_scrolling)

            time.sleep(self._sleep_between_clicking_on_more_results)

            # Load more results
            try:
                self.driver.execute_script("document.querySelector('.mye4qd').click();")
            except Exception as e:
                break
