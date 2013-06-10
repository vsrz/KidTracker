#!/usr/bin/python
#
# Logging mechanism class
# 06/09/2013


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
from datetime import datetime

class Logger:
	datefmt = "%Y-%m-%d %H:%M:%S"
	logfile = "tracker.log"
	filehandler = None

	def __init__( self, logfile=None ):
		if logfile:
			self.logfile = logfile
		self.filehandler = open( self.logfile, "a" )		

	def Log( self, message ):
		now = datetime.now()
		self.filehandler.write( now.strftime( self.datefmt ) + " " + message + "\n" )

	def __del__( self ):
		self.filehandler.close()


