import os
from xml.etree import ElementTree as ET

def xmlparser(file_name):
	dom = ET.parse(file_name)
	result = []
	#elements = [object for object in dom.findall('object/robndbox') if object.findtext('name') =='digits']

	elements = dom.findall('object')
	##print elements
	for objectTag in elements :
		if objectTag[1].text != "digits":
			continue
		robndbox = objectTag.findall("robndbox")[0]
		cx = float(robndbox.find("cx").text)
		cy = float(robndbox.find("cy").text)
		w = float(robndbox.find("w").text)
		h = float(robndbox.find("h").text)
		angle = float(robndbox.find("angle").text)
		return (cx, cy, w, h, angle)
		#result.append( (cx, cy, w, h, angle))
	#return result

if __name__ == "__main__":
	file_name = 'challenging1.xml'
	full_file = os.path.abspath(os.path.join('data', file_name))
	xmlparser(file_name)
