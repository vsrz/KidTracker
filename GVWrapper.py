#!/usr/bin/python
#
#

#from googlevoice import Voice

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

from googlevoice import Voice
from time import sleep

"""
Wrapper for the Google Voice client
"""
class GVWrapper:
	voice = None
	logged_in = False

	def __init__( self ):
		self.voice = Voice()

	def login( self, user, passwd ):
		try:
			self.voice.login( user, passwd )
			self.logged_in = True
		except:
			self.logged_in = False


	def SendAlert( self, text, number ):
		if logged_in:
			self.voice.send_sms( str(number), text )
			sleep(5)

