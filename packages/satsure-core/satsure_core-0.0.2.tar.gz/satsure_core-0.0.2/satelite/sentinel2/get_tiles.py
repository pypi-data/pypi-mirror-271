from os import environ

import fiona
from fiona.session import AWSSession
from sqlalchemy import text

from satelite.config import create_session


class GetTiles:
    """To get tiles from different resources"""

    @staticmethod
    def get_tile_from_geom(geom_list: list) -> list:
        """generate tile from in geom
        :rtype: list
        """
        tile_list = set()
        session = create_session()
        sql_query = text(
            f"""SELECT tile FROM tileids WHERE ST_Intersects( geometry,
                                            ST_GeomFromGeoJSON(:geojson_geometry)) """
        )
        for geom_ in geom_list:
            result = session.execute(sql_query,
                                     {"geojson_geometry": str(geom_)})
            rows = result.fetchall()
            for row in rows:
                tile_list.add(row[0])

        tile_list = list(tile_list)

        return tile_list

    @staticmethod
    def get_tile_from_rids(rids: list, shape_path: str):
        """To get tiles from rids
        :param rids:
        :param shape_path:
        :return: list
        """
        master_tile_list = []
        session = create_session()
        with fiona.Env(
                session=AWSSession(
                    aws_access_key_id=environ.get(
                        "AWS_ACCESS_KEY_ID", None
                    ),
                    aws_secret_access_key=environ.get(
                        "AWS_SECRET_ACCESS_KEY", None
                    ),
                    requester_pays=True,
                    region_name=environ.get(
                        "AWS_DEFAULT_REGION", None
                    ),
                )
        ) as env:
            for region_ in rids:
                with fiona.open(
                        f"s3://satsure-immutables/{shape_path}/{region_}.shp"
                ) as src:
                    bbox = src.bounds

                sql_query = text(
                    """SELECT tile FROM tileids
                                    WHERE ST_Intersects(
                                        geometry,
                                        ST_MakeEnvelope(:minx, :miny, :maxx, :maxy, 4326) -- 4326 is the SRID, adjust if needed
                                    )
                                    """
                )
                result = session.execute(
                    sql_query,
                    {
                        "minx": bbox[0],
                        "miny": bbox[1],
                        "maxx": bbox[2],
                        "maxy": bbox[3],
                    },
                )
                rows = result.fetchall()
                tile_list = set()
                for row in rows:
                    tile_list.add(row[0])
                master_tile_list.extend(tile_list)

        session.close()
        return master_tile_list
