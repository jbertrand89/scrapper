import json
import os

from src.google_image import GoogleImage


class GoogleImagesForLabel(object):
    """ Google images associated to a label.
    """
    def __init__(self, label, data_path):
        """ Constructor

        :param label (str) - label of the objects (example "power_line")
        :param data_path (str) - path of the data folder
        """
        self.label = label
        self.data_folder = data_path
        self.images = []

    def add(self, google_image):
        """Adds a google image to self.images

        :param google_image (GoogleImage) - google image to add
        """
        self.images.append(google_image)

    def get_filename(self):
        """ Gets the auxiliary filename to store all the downloaded information.

        :return: (str) - filename
        """
        return os.path.join(self.data_folder, "{0}.txt".format(self.label))

    def save(self, filename):
        """ Saves the object into a file.

        :param filename (str) - full path of the file where to save the object
        """
        with open(filename, "w+") as writer:
            json.dump(self.__dict__, writer, default=lambda x: x.__dict__)

    @staticmethod
    def load(filename):
        """ Loads from a file.

        :param filename (str) - full path of the file where the object is saved
        :return: (GoogleImagesForLabel) - new object
        """
        with open(filename, "r+") as reader:
            data = json.load(reader)

        label = data["label"]
        data_folder = data["data_folder"]
        google_images = GoogleImagesForLabel(label, data_folder)

        # Add images
        images = data["images"]
        for image_data in images:
            google_image = GoogleImage.load(image_data)
            google_images.add(google_image)

        return google_images
