import pandas as pd
import requests

def get_dataframe(response:requests.Response) -> pd.DataFrame:
    # Verificamos la existencia de los resultados
    response_json = response.json()
    df = pd.json_normalize(response_json, record_path="results", sep="_")
    return df

def next_page(dict:dict) -> int:
    if "paging" in dict.keys():
        after = int(dict["paging"]["next"]["after"])
        return after
    return None
