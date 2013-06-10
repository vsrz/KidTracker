#!/usr/bin/python
#
# Http Reader
# Loads a page into a string and searches for a matching string


"""
 Copyright (c) 2012-2013 Jeremy B. Villegas
 All rights reserved.
 
 Redistribution and use in source and binary forms are permitted
 provided that the above copyright notice and this paragraph are
 duplicated in all such forms and that any documentation,
 advertising materials, and other materials related to such
 distribution and use acknowledge that the software was developed
 by Jeremy Villegas.  The name Jeremy Villegas may not be used to 
 endorse or promote products derived from this software without 
 specific prior written permission. THIS SOFTWARE IS PROVIDED
 ``AS IS'' AND WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES, 
 INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF 
 MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""

import urllib2
from re import findall

class HttpReader:	
	content = str()

	# Opens and saves the contents of a webpage to self.content
	# If basic_auth value is specfied, the appropriate authorization
	# is sent via "Authorization" header
	def __init__( self, page, auth_string=None ):
		opener = urllib2.build_opener()
		if auth_string:
			opener.addheaders = [ ('Authorization', 'Basic ' + auth_string ) ]

		try:
			self.content = opener.open(page).read()
		except:
			print "Unable to contact site: " + page

	def FindInPage( self, search_string ):
		matches = findall(search_string, self.content);
		return len( matches ) > 0

	def FindInARPTable( self, search_mac ):
		table = str()
		for each in self.content.lstrip().split('\n'):
			if each[0:11].lower() == "setarptable":
				table = each

		return len(findall( search_mac, table )) > 0



