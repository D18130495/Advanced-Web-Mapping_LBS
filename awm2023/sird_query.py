from django.contrib.gis.geos import GEOSGeometry, Point
from awm2023.models import WorldBorder


def query():
    pnt = Point(954158.1, 4215137.1, srid=32140)
    pnt = GEOSGeometry('SRID=32140;POINT(954158.1 4215137.1)')
    qs = WorldBorder.objects.filter(mpoly__intersects=pnt)
    print(qs.query)
    print(qs)
