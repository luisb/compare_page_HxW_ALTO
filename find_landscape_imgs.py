#!/usr/bin/python
import sys

if len(sys.argv) == 1 or len(sys.argv) == 2:
	print "FATAL: " + __file__ + " expects to be passed a mode, either 'et' or 'xpath', and a file."
	print "usage: " + __file__ + " [et|xpath] file [file]..."
	sys.exit()

elif sys.argv[1] == 'et':
	# try to find the right elementtree module
	try:
		import elementtree.ElementTree as ET
	except ImportError:
		import xml.etree.ElementTree as ET

elif sys.argv[1] == 'xpath':
	import lxml.etree as ET
	from StringIO import StringIO



mode = sys.argv[1]
landscape_file_count = 0

for File in sys.argv:
	if File == __file__ or File in ('et', 'xpath'):
		continue
	
	tree = ET.parse(File)
	
	if mode == 'et':
		root = tree.getroot()
	
		for page in root.getiterator('{http://www.loc.gov/standards/alto/ns-v2#}Page'):
			height = page.attrib['HEIGHT']
			width  = page.attrib['WIDTH']

			if height > width:
				continue  
			else: 
				landscape_file_count = landscape_file_count + 1
				print File + ": " + height + " x " + width + "; landscape detected."

	elif mode == 'xpath':
		with open(File,'r') as f:
			data = f.read()
			#print data
			root = ET.parse(StringIO(data))
			#print root
			#r = root.xpath("//*[@*[namespace-uri()='http://www.loc.gov/standards/alto/ns-v2#']]")
			#r = root.xpath("*")
			#print r
			#print r[0].tag
			
			#r[0].tag == 'HEIGHT'
			
			for page in root.getiterator('{http://www.loc.gov/standards/alto/ns-v2#}Page'):
				height = page.attrib['HEIGHT']
				width  = page.attrib['WIDTH']
				
				if height > width:
					continue  
				else: 
					landscape_file_count = landscape_file_count + 1
					print File + ": " + height + " x " + width + "; landscape detected."
	else:
		print "Something terribly wrong has occured. Quitting."
		sys.exit()
print "Analysis complete. " + str(landscape_file_count) + (" file " if landscape_file_count == 1 else " files ") + "found possibly in landscape orientation"