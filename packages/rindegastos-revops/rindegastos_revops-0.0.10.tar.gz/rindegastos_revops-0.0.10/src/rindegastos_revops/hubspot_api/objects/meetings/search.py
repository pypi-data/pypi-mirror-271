from ..search import Search
from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints

from datetime import datetime


class MeetingsSearch():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 from_date:datetime, 
                 to_date:datetime, 
                 property_filter:str = "hs_createdate"):
        
        self.calls_search = Search(
            client=client,
            properties_endpoint = Endpoints.PROPERTIES_MEETINGS_READ_ALL,
            object_endpoint = Endpoints.MEETINGS_SEARCH,
            property_filter = property_filter,
            from_date = from_date,
            to_date = to_date
        )


    def records(self):
        object_records = self.calls_search.all_pages_df()
        return object_records