import re
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.point import Point
from OSMPythonTools.nominatim import Nominatim, NominatimResult
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

boro_dict = {
    'Manhattan': 'New York',
    'New York': 'New York',
    'Brooklyn': 'Kings',
    'Kings': 'Kings',
    'Queens': 'Queens',
    'Bronx': 'Bronx',
    'The Bronx': 'Bronx',
    'Staten Island': 'Richmond',
    'Richmond': 'Richmond'
}

class IntersectionGC:
    def __init__(self):
        self.nominatim = Nominatim()
        self.overpass = Overpass()
        self.results = None

        query = 'NYC'
        result = self.nominatim.query(query).areaId()
        self.area_id = result

    def get_intersection(
        self,
        street1: str,
        street2: str,
        county: str) -> Point:
        """
        Retrieves street intersection Point(lon, lat) from OSM.
        County/boro name (i.e. 'Kings' or 'Brooklyn') required.
        """
        county = boro_dict[county]
        coords1 = self._get_street_geo(
            self._clean_street(street1),
            county
        )
        coords2 = self._get_street_geo(
            self._clean_street(street2),
            county
        )
        intersection = coords1.intersection(coords2)

        return intersection
            
    def _get_street_geo(
        self,
        street: str,
        county: str) -> MultiLineString:
        """
        Helper method to make OSM Overpass street query and return MultiLineString.
        """
        county_id = self._get_county_area_id(county)
        query = overpassQueryBuilder(
            area=county_id,
            elementType='way',
            selector=['highway', '"name"="{}"'.format(self._clean_street(street))],
            out='body',
            includeGeometry=True
        )
        r = self.overpass.query(query, timeout=100)
        
        geos = []
        for ele in r.elements():
            geo = ele.geometry()
            coords = geo['coordinates']
            geo = LineString(coords)
            geos.append(geo)
        result = MultiLineString(geos)
        
        return result

    def _clean_street(self, address: str) -> str:
        """
        Helper method to clean street strings.
        """
        address = self._ordinal_rep(address)
        address = self._standardize_street(address)
        address = self._abb_to_full(address)

        return address

    def _ordinal_rep(self, s: str) -> str:
        """
        Helper function to convert numerical cardinality to ordinality.
        """
        num = re.search(r'[0-9]+\s', s)
        if num == None:
            return s
        else:
            num = re.search(r'[0-9]+', s)[0]
            if len(num) > 1:
                if (num[-1] == '1') and (num[-2] != '1'):
                    ord = num + 'st'
                elif num[-1] == '2' and (num[-2] != '1'):
                    ord = num + 'nd'
                elif num[-1] == '3' and (num[-2] != '1'):
                    ord = num + 'rd'
                else:
                    ord = num + 'th'
            else:
                if (num[-1] == '1'):
                    ord = num + 'st'
                elif num[-1] == '2':
                    ord = num + 'nd'
                elif num[-1] == '3':
                    ord = num + 'rd'
                else:
                    ord = num + 'th'

            return s.replace(num, ord)

    def _abb_to_full(self, street: str) -> str:
        """
        Helper function to convert cardinality abbreviation to full.
        """
        if 'W ' in street:
            street = 'West ' + street.split('W ')[1]
        if 'E ' in street:
            street = 'East ' + street.split('E ')[1]
        if 'N ' in street:
            street = 'North ' + street.split('N ')[1]
        if 'S ' in street:
            street = 'South ' + street.split('S ')[1]

        return street

    def _standardize_street(self, street: str) -> str:
        """
        Helper function to standardize street names.
        """
        if ' St' in street:
            street = street.split(' St')[0] + ' Street'
        if ' Ave' in street:
            street = street.split(' Ave')[0] + ' Avenue'
        if ' Rd' in street:
            street = street.split(' Rd')[0] + ' Road'
        if ' Pkwy' in street:
            street = street.split(' Pkwy')[0] + ' Parkway'
        if ' Blvd' in street:
            street = street.split(' Blvd')[0] + ' Boulevard'
        if ' Ct' in street:
            street = street.split(' Ct')[0] + ' Court'
        if ' Ln' in street:
            street = street.split(' Ln')[0] + ' Lane'

        return street

    def _get_county_area_id(self, county: str) -> NominatimResult:
        """
        Helper method to get county area ID.
        """
        query = '{} County, NY'.format(county)
        result = self.nominatim.query(query)

        return result