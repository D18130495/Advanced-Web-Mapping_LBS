from awm2023.models import WorldBorder
from django.contrib.gis.geos import Point


def query_set():
    pnt_wkt = 'POINT(-95.3385 29.7245)'
    print(WorldBorder.objects.filter(mpoly__contains=pnt_wkt))


def query_instance():
    pnt = Point(12.4604, 43.9420)
    print(WorldBorder.objects.get(mpoly__intersects=pnt))
