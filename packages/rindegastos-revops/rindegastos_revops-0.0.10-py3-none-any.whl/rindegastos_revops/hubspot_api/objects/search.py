from ...hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from ...hubspot_api.helpers.get_dataframe import next_page, get_dataframe
from ...hubspot_api.helpers.dates import str_isoformat
from ...hubspot_api.properties import read_all

from typing import Optional
from datetime import datetime
import pandas as pd
import json
import requests


class Search():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 properties_endpoint: Endpoints,
                 object_endpoint: Endpoints,
                 property_filter:str,
                 from_date:datetime, 
                 to_date:datetime):
        
        self.client = client
        self.properties_endpoint = properties_endpoint
        self.object_endpoint = object_endpoint
        self.property_filter = property_filter
        self.from_date = from_date
        self.to_date = to_date


    def call(self, after:int = 0, limit:int = 100) -> requests.Response:
        
        properties_df = read_all.all_properties_df(self.client, self.properties_endpoint)
            
        payload = {
            "limit": limit,
            "after": after,
            "sorts": [
                {
                "propertyName": self.property_filter,
                "direction": "DESCENDING"
                }
            ],
            "properties": properties_df["name"].to_list(),
            "filterGroups": [
                {
                    "filters": [
                        {"propertyName": self.property_filter, "value": str_isoformat(self.from_date), "operator": "GTE"},
                        {"propertyName": self.property_filter, "value": str_isoformat(self.to_date), "operator": "LTE"},
                    ]
                }
            ],
        }

        response = requests.request("POST", self.client.endpoint(self.object_endpoint), headers=self.client.headers, data=json.dumps(payload))

        return response
    
    def all_pages_df(self) -> Optional[pd.DataFrame]:
        after = 0
        dfs = []

        while after != None:
            rq = self.call(after)
            if rq.status_code == 200:
                df =  get_dataframe(rq)
                dfs.append(df)
                after = next_page(rq.json())
            else:
                return None

        return pd.concat(dfs).reset_index(drop=True)