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
	
	# grab information from the device from the configuration file
	last_state = config.device_status[each]
	is_present = config.device_present[each]
	device_name = config.device_names[each]
	
	# search the page for the device	
	new_state = page.FindInARPTable( config.device_ids[each] )

	# if the device is online, and the device's last state is not
	# larger than the alert threshold, increment the ping counter
	if( new_state == True and last_state < config.threshold ):				
		config.device_status[each] += 1
		logger.Log(device_name + " has pinged on the network. State: " + str( config.device_status[each] ) )
	
	# but if the device is not online, and the last state is
	elif( new_state == False and last_state > 0 ):
		config.device_status[each] -= 1	
		logger.Log(device_name + " dropped a ping on the network. State: " + str( config.device_status[each] ) )


	# determine if we need to send a message
	if( new_state == True and config.device_status[each] >= config.threshold and is_present == False ):
		message += device_name + " has joined the wireless network. "
		config.device_present[each] = True
		logger.Log("STATE CHANGE: " + message)

	elif( new_state == False and config.device_status[each] <= 0 and is_present == True ):
		message += device_name + " has left the wireless network. "
		config.device_present[each] = False
		logger.Log("STATE CHANGE: " + message)

	# Append to the text message
	# Uncomment below if you want to make a log entry for each poll
	# logger.Log( config.device_names[each] + " State: " + str( config.device_status[each] ) + " Present: " + str( config.device_present[each] ) )

# Write the config file
config.WriteConfig()

# Send a text message if necessary
if message:
	gvoice.login( config.gvuser, config.gvpass )
	logger.Log("Sent text message to " + str( config.notify ) )
	if len( config.notify ) > 0:
		for number in config.notify:
			gvoice.SendAlert( number, message )


