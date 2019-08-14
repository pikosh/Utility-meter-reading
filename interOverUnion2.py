import shapely.geometry
#from shapely import geometry, affinity
import shapely.affinity
from parser3 import xmlparser
from measure_image2 import measure_image2
#import shapely.affinity

class RotatedRect:
	def __init__(self, cx, cy, w, h, angle):
		self.cx = cx
		self.cy = cy
		self.w = w
		self.h = h
		self.angle = angle

	def get_contour(self):
		w = self.w
		h = self.h
		c = shapely.geometry.box(-w, -h, w, h)
		rc = shapely.affinity.rotate(c, self.angle)
		return shapely.affinity.translate(rc, self.cx, self.cy)

	def intersection(self, other):
		return self.get_contour().intersection(other.get_contour())
	def union(self, other):
		return self.get_contour().union(other.get_contour())

#r1 = RotatedRect(138, 217, 276, 103, 0)
#r2 = RotatedRect(190, 193, 267, 40, 3.04)
#print xmlparser("small1.xml")
#r1 = RotatedRect(*measure_image2("image1.jpg"))
#r2 = RotatedRect(*xmlparser("image1.xml"))
#print (measure_image("image1.jpg"))
#print (measure_image('/home/perizat/Рабочий стол/thesis/current work/data set/image1.jpg'))
#print (xmlparser("image1.xml"))
#print r2.get_contour()
#print (r1.intersection(r2).area / r1.union(r2).area)
