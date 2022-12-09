import pygeohash as pgh




def point_to_geohash(geo_points):
    try:
        return pgh.encode(geo_points[0], geo_points[1], precision=10)
    except Exception as e:
        print(e)
        return 1




def geohash_to_point(hash):
    try:
        return pgh.decode(hash)
    except:
        return ''