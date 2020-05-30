

class GoogleImage(object):
    """ Google image object
    """
    def __init__(self, url, label, image_id):
        """ Constructor

        :param url (str) - url of the image
        :param label (str) - label associated to this image (example "power_line")
        :param image_id (int) - image id
        """
        self.url = url
        self.label = label
        self.image_id = image_id

    @property
    def filename(self):
        """ Gets the image filename.

        :return (str) - image filename relative to the data directory
        """
        return "{0}/{0}_{1}.png".format(self.label, self.image_id)

    @staticmethod
    def load(data):
        """ Loads from data and create a new GoogleImage

        :param data {str:str} - object as a dictionary
        :return: (GoogleImage) - new GoogleImage object from data.
        """
        url = data["url"]
        label = data["label"]
        image_id = data["image_id"]
        return GoogleImage(url, label, image_id)
