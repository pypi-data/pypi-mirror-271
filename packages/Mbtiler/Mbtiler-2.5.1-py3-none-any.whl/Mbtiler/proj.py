from math import pi, sin, log, exp, atan, tan, ceil
from gettext import gettext as _
from . import DEFAULT_TILE_SIZE
import numpy as np

DEG_TO_RAD = pi/180
RAD_TO_DEG = 180/pi
MAX_LATITUDE = 85.0511287798
EARTH_RADIUS = 6378137


def minmax (a,b,c):
    a = max(a,b)
    a = min(a,c)
    return a


class InvalidCoverageError(Exception):
    """ Raised when coverage bounds are invalid """
    pass


# http://ecn.t1.tiles.virtualearth.net/tiles/r012012012.png?g=685&mkt=en-us

#------------------------------------------------------------------------------
# <copyright company="Microsoft">
#     Copyright (c) 2006-2009 Microsoft Corporation.  All rights reserved.
# </copyright>
#------------------------------------------------------------------------------



class TileSystem:
	EarthRadius = 6378137.
	MinLatitude = -85.05112878
	MaxLatitude = 85.05112878
	MinLongitude = -180
	MaxLongitude = 180

	# def __init__(self):
	# 	pass

	def Clip(self, n, minValue, maxValue):
		return min(max(n, minValue), maxValue)

	def MapSize(self, levelOfDetail):
		return 256 << levelOfDetail

	def GroundResolution(self, latitude, levelOfDetail):
		latitude = self.Clip(latitude, self.MinLatitude, self.MaxLatitude)
		return np.cos(latitude * np.pi / 180.) * 2 * np.pi * self.EarthRadius / self.MapSize(levelOfDetail)

	def MapScale(self, latitude, levelOfDetail, screenDpi):
		return (latitude, levelOfDetail) * screenDpi / 0.0254;

	def LatLongToPixelXY(self, latitude, longitude, levelOfDetail):
		latitude = self.Clip(latitude, self.MinLatitude, self.MaxLatitude);
		longitude = self.Clip(longitude, self.MinLongitude, self.MaxLongitude);

		x = (longitude + 180) / 360; 
		sinLatitude = np.sin(latitude * np.pi / 180);
		y = 0.5 - np.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * np.pi);

		mapSize = self.MapSize(levelOfDetail);
		pixelX = self.Clip(x * mapSize + 0.5, 0, mapSize - 1);
		pixelY = self.Clip(y * mapSize + 0.5, 0, mapSize - 1);
		
		return int(pixelX), int(pixelY)

	def PixelXYToLatLong(self, pixelX, pixelY, levelOfDetail):
		mapSize = self.MapSize(levelOfDetail)
		x = (self.Clip(pixelX, 0, mapSize-1) / mapSize) - 0.5
		y = 0.5 - (self.Clip(pixelY, 0, mapSize - 1) / mapSize)

		latitude = 90. - 360. * np.arctan(np.exp(-y * 2 * np.pi)) / np.pi
		longitude = 360. * x

		return latitude, longitude

	def PixelXYToTileXY(self, pixelX, pixelY):
		return int(pixelX/256), int(pixelY/256)

	def PixelXYToTilePixelXY(self, pixelX, pixelY):
		return pixelX%256, pixelY%256

	def TileXYToPixelXY(self, tileX, tileY):
		return int(tileX*256), int(tileY*256)

	def TileXYToQuadKey(self, tileX, tileY, levelOfDetail):
		quadKey = ''
		for i in range(levelOfDetail,0,-1):
			digit = 0
			mask = 1 << (i-1)
			if (tileX & mask) != 0:
				digit += 1
			if (tileY & mask) != 0:
				digit += 1
				digit += 1
			quadKey += str(digit)
		return quadKey

	def QuadKeyToTileXY(self, quadKey):
		tileX = tileY = 0
		levelOfDetail = len(quadKey)
		for i in range(levelOfDetail,0,-1):
			mask = 1 << (i-1)
			# if quadKey[levelOfDetail - i] == '0':
			# 	break
			if quadKey[levelOfDetail - i] == '1':
				tileX |= mask
			elif quadKey[levelOfDetail - i] == '2':
				tileY |= mask
			elif quadKey[levelOfDetail - i] == '3':
				tileX |= mask
				tileY |= mask
			elif quadKey[levelOfDetail - i] != '0':
				raise Exception('Invalid QuadKey digit sequence.')
		return tileX, tileY

class GoogleProjection(object):

    NAME = 'EPSG:3857'

    """
    Transform Lon/Lat to Pixel within tiles
    Originally written by OSM team : http://svn.openstreetmap.org/applications/rendering/mapnik/generate_tiles.py
    """
    def __init__(self, tilesize=DEFAULT_TILE_SIZE, levels = [0], scheme='wmts'):
        if not levels:
            raise InvalidCoverageError(_("Wrong zoom levels."))
        self.Bc = []
        self.Cc = []
        self.zc = []
        self.Ac = []
        self.levels = levels
        self.maxlevel = max(levels) + 1
        self.tilesize = tilesize
        self.scheme = scheme
        c = tilesize
        for d in range(self.maxlevel):
            e = c/2;
            self.Bc.append(c/360.0)
            self.Cc.append(c/(2 * pi))
            self.zc.append((e,e))
            self.Ac.append(c)
            c *= 2

    def project_pixels(self,ll,zoom):
        d = self.zc[zoom]
        e = round(d[0] + ll[0] * self.Bc[zoom])
        f = minmax(sin(DEG_TO_RAD * ll[1]),-0.9999,0.9999)
        g = round(d[1] + 0.5*log((1+f)/(1-f))*-self.Cc[zoom])
        return (e,g)

    def unproject_pixels(self,px,zoom):
        e = self.zc[zoom]
        f = (px[0] - e[0])/self.Bc[zoom]
        g = (px[1] - e[1])/-self.Cc[zoom]
        h = RAD_TO_DEG * ( 2 * atan(exp(g)) - 0.5 * pi)
        if self.scheme == 'tms':
            h = - h
        return (f,h)

    def tile_at(self, zoom, position):
        """
        Returns a tuple of (z, x, y)
        """
        x, y = self.project_pixels(position, zoom)
        return (zoom, int(x/self.tilesize), int(y/self.tilesize))

    def tile_bbox(self, z_x_y):
        """
        Returns the WGS84 bbox of the specified tile
        """
        (z, x, y) = z_x_y
        topleft = (x * self.tilesize, (y + 1) * self.tilesize)
        bottomright = ((x + 1) * self.tilesize, y * self.tilesize)
        nw = self.unproject_pixels(topleft, z)
        se = self.unproject_pixels(bottomright, z)
        return nw + se

    def project(self, lng_lat):
        """
        Returns the coordinates in meters from WGS84
        """
        (lng, lat) = lng_lat
        x = lng * DEG_TO_RAD
        lat = max(min(MAX_LATITUDE, lat), -MAX_LATITUDE)
        y = lat * DEG_TO_RAD
        y = log(tan((pi / 4) + (y / 2)))
        return (x*EARTH_RADIUS, y*EARTH_RADIUS)

    def unproject(self, x_y):
        """
        Returns the coordinates from position in meters
        """
        (x, y) = x_y
        lng = x/EARTH_RADIUS * RAD_TO_DEG
        lat = 2 * atan(exp(y/EARTH_RADIUS)) - pi/2 * RAD_TO_DEG
        return (lng, lat)

    def tileslist(self, bbox):
        if len(bbox) != 4:
            raise InvalidCoverageError(_("Wrong format of bounding box."))
        xmin, ymin, xmax, ymax = bbox
        if abs(xmin) > 180 or abs(xmax) > 180 or \
           abs(ymin) > 90 or abs(ymax) > 90:
            raise InvalidCoverageError(_("Some coordinates exceed [-180,+180], [-90, 90]."))

        if xmin >= xmax or ymin >= ymax:
            raise InvalidCoverageError(_("Bounding box format is (xmin, ymin, xmax, ymax)"))

        ll0 = (xmin, ymax)  # left top
        ll1 = (xmax, ymin)  # right bottom

        l = []
        for z in self.levels:
            px0 = self.project_pixels(ll0,z)
            px1 = self.project_pixels(ll1,z)

            for x in range(int(px0[0]/self.tilesize),
                           int(ceil(px1[0]/self.tilesize))):
                if (x < 0) or (x >= 2**z):
                    continue
                for y in range(int(px0[1]/self.tilesize),
                               int(ceil(px1[1]/self.tilesize))):
                    if (y < 0) or (y >= 2**z):
                        continue
                    if self.scheme == 'tms':
                        y = ((2**z-1) - y)
                    l.append((z, x, y))
        return l
