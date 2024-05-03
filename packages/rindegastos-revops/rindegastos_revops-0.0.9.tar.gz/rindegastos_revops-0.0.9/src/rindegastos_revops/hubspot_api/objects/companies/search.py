from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from ....hubspot_api.helpers.dates import str_isoformat
from ....hubspot_api.properties import read_all

from datetime import datetime
import json
import requests


class CompaniesSearch():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 from_date:datetime, 
                 to_date:datetime, 
                 property_filter:str = "createdate", 
                 full_property:bool = False,
                 properties:list = []):
        
        self.client = client
        self.from_date = from_date
        self.to_date = to_date
        self.property_filter = property_filter
        self.full_property = full_property
        self.properties = properties
        

    def call(self, after:int = 0, limit:int = 100) -> requests.Response:
        
        if self.full_property:
            properties = read_all.read_all_properties(self.client, Endpoints.PROPERTIES_COMPANIES_READ_ALL)["df"]["name"].to_list()
            
        payload = {
            "limit": limit,
            "after": after,
            "filterGroups": [
                {
                    "filters": [
                        {"propertyName": self.property_filter, "value": str_isoformat(self.from_date), "operator": "GTE"},
                        {"propertyName": self.property_filter, "value": str_isoformat(self.to_date), "operator": "LTE"},
                    ]
                }
            ],
            "sorts": [
                {
                "propertyName": "createdate",
                "direction": "DESCENDING"
                }
            ],
            "properties": properties
        }


        response = requests.request("POST", self.client.endpoint(Endpoints.COMPANIES_SEARCH), headers=self.client.headers, data=json.dumps(payload))
        
        return response