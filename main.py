#!/usr/bin/python
#
# Tracking service which when called from Cron will alert
# the host based on when a device joins or leaves the 
# wireless network
#
# Jeremy Villegas
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


import sys, os, time, io, ConfigParser
import urllib2, re
from base64 import b64encode

# custom imports
from googlevoice import Voice
from TrackerConfig import TrackerConfig
from GVWrapper import GVWrapper
from HttpReader import HttpReader
from Tests import Tests
from Logger import Logger

# If this is a test run
tests = False

# Run Tests
if tests == True:
	t = Tests()
	sys.exit()
	
# Load the config file
config = TrackerConfig()

# Load Google Voice Module
gvoice = GVWrapper()

# Load the log file
logger = Logger( config.logfile )

message = str()

# Load webpage
page = HttpReader( config.router_page, config.router_auth )

# now find the new state of each device in the list
for each in range( len(config.device_ids) ):
	
	last_state = config.device_status[each]
	new_state = page.FindInARPTable( config.device_ids[each] )
	
	# if there is a change in state
	if( new_state != last_state ):
		change = " left "
		if new_state == True:
			change = " joined "

		# Make the state change
		config.device_status[each] = new_state

		# Append to the text message
		message += config.device_names[each] + " has" + change + "the wireless network. "
		logger.Log(" STATE CHANGE: " + message)
	else:
		logger.Log( config.device_names[each] + " State: " + str( config.device_status[each] ) )

# Write the config file
config.WriteConfig()

# Send a text message if necessary
if message:
	gvoice.login( config.gvuser, config.gvpass )
	logger.Log("Sent text message to " + str( config.notify ) )
	if len( config.notify ) > 0:
		gvoice.SendAlert( message, config.notify )


