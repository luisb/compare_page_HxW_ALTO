#!/usr/bin/python
import sys

if len(sys.argv) == 1:
	print "FATAL: " + __file__ + " expects to be passed one or more files."
	print "usage: " + __file__ + " file [file]..."
	sys.exit()

import lxml.etree as ET
from StringIO import StringIO

landscape_file_count = 0

for File in sys.argv:
	if File == __file__:
		continue
	
	tree = ET.parse(File)
	
	with open(File,'r') as f:
		# read data form file into "data"
		data = f.read()

		# parse the file in memory
		root = ET.parse(StringIO(data))
		
		# get the Page element and store the HEIGHT and WIDTH attributes in respective vars
		for page in root.getiterator('{http://www.loc.gov/standards/alto/ns-v2#}Page'):
			height = page.attrib['HEIGHT']
			width  = page.attrib['WIDTH']
			
			# compare height and width; if width > height, landscape detected. print a message to that effect
			if height > width:
				continue  
			else: 
				landscape_file_count = landscape_file_count + 1
				print File + ": " + height + " x " + width + "; landscape detected."

print "Analysis complete. " + str(landscape_file_count) + (" file " if landscape_file_count == 1 else " files ") + "found in landscape orientation"

