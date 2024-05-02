from typing import List, Dict, Any

import pandas as pd
from pystac_client import Client


class FetchUniqueTileDatePystac:
    """Fetching feature details using polygons"""

    def __init__(self, start_date: str, end_date: str, processing_level: str,
                 cloud_cover_perc: str):
        self.start_date = start_date
        self.end_date = end_date
        self.processing_level = processing_level
        self.cloud_cover_perc = cloud_cover_perc

    def get_unique_tile_date(self,
                             simplified_polygon_list: List[Dict[str, Any]]) -> \
    List[pd.DataFrame]:
        """
         Fetching features list using polygon list
        :param simplified_polygon_list:
        :return:
        """
        api_df_list = []
        client = Client.open("https://earth-search.aws.element84.com/v1/")
        collection = f"sentinel-2-{self.processing_level}"
        date_range = f"{self.start_date}/{self.end_date}"
        cloud_cover = int(self.cloud_cover_perc.split(",")[-1])
        filters = {"eo:cloud_cover": {"lt": cloud_cover}}
        for polygon_ in simplified_polygon_list:
            search = client.search(
                collections=[collection],
                intersects=polygon_,
                datetime=date_range,
                query=filters,
            )
            df = pd.DataFrame.from_dict(search.items_as_dicts())
            df[["tileid", "startDate"]] = (
                df["id"].str.split("_", expand=True).iloc[:, 1:3]
            )
            df["startDate"] = pd.to_datetime(df["startDate"])
            api_df_list.append(df)

        return api_df_list
