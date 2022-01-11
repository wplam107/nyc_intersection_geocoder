# NYC Intersection Geocoder
Package to help finding latitude and longitude for NYC street intersections utilizing [OSMPythonTools](https://github.com/mocnik-science/osm-python-tools).

## Dependencies:
- [OSMPythonTools](https://github.com/mocnik-science/osm-python-tools)
- [shapely](https://shapely.readthedocs.io/en/stable/index.html)
    - Note: [GEOS](https://trac.osgeo.org/geos) required

## Installation:
`pip install nyc_intersection_geocoder`

## Usage:
``` python
from nyc_intersection_geocoder.geocoder import IntersectionGC

encoder = IntersectionGC()
result = encoder.get_intersection(
    'Wythe Ave', 'N 4th Street', 'Brooklyn'
)
print(type(result)) # shapely.geometry.point.Point
print(result.coords.xy) # (array('d', [-73.962206]), array('d', [40.717871]))
```
Note: Geographic data for plot is ordered in (longitude, latitude) for to match (x, y) coordinates.