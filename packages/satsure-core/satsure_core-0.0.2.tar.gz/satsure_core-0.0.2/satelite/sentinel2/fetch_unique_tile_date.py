from typing import List

import pandas as pd
import requests


class FetchUniqueTileDate:
    """Fetching feature details using Tiles"""
    METADATA = {
        "l2a": {"producttype": "S2MSI2A", "processinglevel": "S2MSI2A"},
        "l1c": {"producttype": "S2MSI1C", "processinglevel": "S2MSI1C"},
    }

    def __init__(self, cloud_cover_perc: str, start_date: str, end_date: str,
                 processing_level: str):
        self.cloud_cover_perc = cloud_cover_perc
        self.start_date = start_date
        self.end_date = end_date
        self.processing_level = processing_level

    def get_unique_tile_date(self, tile_list: List[str]) -> List[
        pd.DataFrame]:
        """
        Fetching features list using tile ids
        :param tile_list:
        :return: list
        """
        api_df_list = []
        for tileId in tile_list:
            url = (
                f'https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?cloudCover=[{self.cloud_cover_perc}]'
                f'&startDate={self.start_date}T00:00:00Z&completionDate={self.end_date}T23:59:59Z&'
                f'productType={self.METADATA[self.processing_level]["producttype"]}&'
                f'processingLevel={self.METADATA[self.processing_level]["processinglevel"]}&tileId={tileId}&maxRecords=1000')
            response = requests.get(url)
            json = response.json()
            df = pd.DataFrame.from_dict(json["features"])
            # Extract specific keys from the 'metadata' column
            df["productIdentifier"] = df["properties"].apply(
                lambda x: x.get("productIdentifier")
            )
            df["title"] = df["properties"].apply(lambda x: x.get("title"))
            df["startDate"] = df["properties"].apply(
                lambda x: x.get("startDate"))
            df["startDate"] = pd.to_datetime(df["startDate"])
            df["completionDate"] = df["properties"].apply(
                lambda x: x.get("completionDate")
            )
            df["productType"] = df["properties"].apply(
                lambda x: x.get("productType")
            )
            df["processingLevel"] = df["properties"].apply(
                lambda x: x.get("processingLevel")
            )
            df["cloudCover"] = df["properties"].apply(
                lambda x: x.get("cloudCover"))
            api_df_list.append(df)

        return api_df_list
