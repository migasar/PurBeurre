"""
Handle the recovery of the data

Fetch the data from an external repository.
and deal with the reformatting of the data.
"""


import requests 

import Static.constant as constant


class API:
    """Set the API """

    def __init__(self, url, parameters):
        self.url = url
        self.parameters = parameters

    # def add_parameter(self, parameter):
    #     """Set the parameters of the API """
    #     self.parameters.update(parameter)


class APICaller:
    """
    Creates a request to connect with an API and to collect data from a website
    """

    def __init__(self, api):
        self.url = api.url
        self.parameters = api.parameters

        self.response = requests.get(self.url, params=self.parameters)
        self.payload = None

    # def get_response(self):
    #     """Make a get request to the API. """
    #
    #     self.response = requests.get(self.url, params=self.parameters)
    #     # A variant :
    #     # for i in range(1, 10):
    #     #     parameters["page"] = i
    #
    #     return self.response

    def test_response(self):
        """Print the status code of the response. """

        if self.response is None:
            return "The request has yet to be made. "

        else:
            return "status code of the response : {}".format(str(self.response.status_code))

    def format_response(self):
        """Create a dictionary, uniquely with the JSON elements from the request. """

        if self.response is None:
            return "The request has yet to be made. "

        else:
            self.payload = self.response.json()
            return self.payload


class DataCleaner:
    """
    Handle a JSON object to structure it and to manipulate its content
    """

    pass
