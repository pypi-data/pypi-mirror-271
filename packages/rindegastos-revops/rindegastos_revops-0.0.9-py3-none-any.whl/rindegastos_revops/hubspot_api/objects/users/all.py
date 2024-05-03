from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from ....hubspot_api.properties import read_all

import requests


class AllUsers():
    def __init__(self, client:HubspotConnectorApi):
        self.client = client
        
    def call(self, after:int = 0, limit:int = 100) -> requests.Response:
        properties = read_all.read_all_properties(self.client, Endpoints.PROPERTIES_USERS_READ_ALL)["df"]["name"].to_list()
        querystring = {"limit":limit,"after":after,"properties":properties,"archived":"false"}
        
        response = requests.request("GET", self.client.endpoint(Endpoints.USERS_ALL), headers=self.client.headers, params=querystring)

        return response