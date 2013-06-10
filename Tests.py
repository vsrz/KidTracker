#!/usr/bin/python
#
# Tests for the Tracker Project
# 

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
import sys, os
from TrackerConfig import TrackerConfig
#from GVWrapper import GVWrapper
from HttpReader import HttpReader


# Test class
class Tests:
	
	GVWrapperTest = False
	TrackerTest = True
	HttpReaderTest = False

	def __init__( self ):
		if self.GVWrapperTest:
			config = TrackerConfig()
			gv = GVWrapper()
			gv.login( config.gvuser, config.gvpass )			
			gv.SendAlert( "Testing tracker text message", config.notify )

		if self.TrackerTest:
			print "Initializing tracker...",
			tracker = TrackerConfig()
			print " Ok."

		if self.HttpReaderTest:
			print "Reading page...",
			config = TrackerConfig()
			h = HttpReader( config.router_page, config.router_auth )			
			print " Ok."
			print type(config.device_ids)
			h.FindInARPTable( config.device_ids[0] )

