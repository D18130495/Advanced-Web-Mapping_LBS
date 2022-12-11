import overpy as overpy
from django.contrib.gis.geos import Polygon, Point
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.utils import json

from django_restful_api import serializers


class QueryOverpass(views.APIView):
    """
    class-based view use to query overpass information
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.OverpassSerializer

    def post(self, request, *args, **kwargs):
        try:
            # Create overpass API object
            api = overpy.Overpass()

            # Overpass top query template
            api_query_top = \
                """
                [out:json][timeout:25];
                (
                """

            # Overpass middle query template
            api_middle = ""

            # Overpass bottom query template
            api_query_bottom = \
                """
                );
                out body;
                >;
                out skel qt;
                """

            my_serializer = serializers.OverpassSerializer(data=request.data)

            # serializer passes the password format check
            if my_serializer.is_valid():
                bbox = my_serializer.validated_data["bbox"]

                # form query string for overpass
                for item in my_serializer.validated_data["query"]:
                    if item == "*":
                        api_middle += f'node["amenity"]{tuple(bbox)};\nway["amenity"]{tuple(bbox)};\nrelation["amenity"]{tuple(bbox)};'
                        break
                    else:
                        api_middle += f'node["amenity"="{item}"]{tuple(bbox)};\nway["amenity"="{item}"]{tuple(bbox)};\nrelation["amenity"="{item}"]{tuple(bbox)}; '

                api_query = f"{api_query_top}\n{api_middle}\n{api_query_bottom}\n"

                # run the query
                result = api.query(api_query)

                # GeoJSON result
                geojson_result = {
                    "type": "FeatureCollection",
                    "features": [],
                }

                # iterates each way, get centroid and remove duplicated
                nodes_in_way = []

                for way in result.ways:
                    geojson_feature = {
                        "type": "Feature",
                        "id": "",
                        "geometry": "",
                        "properties": {}
                    }

                    poly = []

                    for node in way.nodes:
                        # Record the nodes and make the polygon
                        nodes_in_way.append(node.id)
                        poly.append([float(node.lon), float(node.lat)])
                    # Make a poly out of the nodes in way.
                    try:
                        poly = Polygon(poly)
                    except Exception as e:
                        continue

                    geojson_feature["id"] = f"way_{way.id}"
                    geojson_feature["geometry"] = json.loads(poly.centroid.geojson)
                    geojson_feature["properties"] = {}
                    for k, v in way.tags.items():
                        geojson_feature["properties"][k] = v

                    geojson_result["features"].append(geojson_feature)

                # Process results that are 'nodes'
                for node in result.nodes:
                    # Ignore nodes which are also in a 'way' as we will have already processed the 'way'.
                    if node.id in nodes_in_way:
                        continue
                    geojson_feature = None
                    geojson_feature = {
                        "type": "Feature",
                        "id": "",
                        "geometry": "",
                        "properties": {}
                    }
                    point = Point([float(node.lon), float(node.lat)])
                    geojson_feature["id"] = f"node_{node.id}"
                    geojson_feature["geometry"] = json.loads(point.geojson)
                    geojson_feature["properties"] = {}
                    for k, v in node.tags.items():
                        geojson_feature["properties"][k] = v

                    geojson_result["features"].append(geojson_feature)

                # Return the complete GeoJSON structure.
                return Response(geojson_result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"result": False, "info": "Server error, overpass require failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
