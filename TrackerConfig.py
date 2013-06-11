#!/usr/bin/python
#
# Tracker Configuration file handling
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

import sys, os, io, ConfigParser
from base64 import b64encode


"""
Deals with handling the alerts
"""
class TrackerConfig:
	device_status = []
	device_names = []
	device_ids = []
	device_present = []
	logfile = str()
	configfile = "tracker.cfg"

	# google voice configuration
	gvuser = str()
	gvpass = str()
	notify = []
	threshold = 0

	# ddwrt config
	router_user = str()
	router_pass = str()
	router_page = str()

	# Authorization header for basic auth on the router
	router_auth = str()

	def __init__( self ):
		configdata = str()
		# first check if the file exists
		try:
			filehandle = open( self.configfile, "r")
			for each in filehandle:
				configdata += each
			filehandle.close()
		except:
			print self.configfile + " could not be read"
			print "Default configuration will be created"			
			self.CreateInitialConfig()

		if configdata:
			self.ReadConfig( configdata )

	"""
	Called when the initial configuration file could not be read
	"""
	def CreateInitialConfig( self ):
		self.device_status = [0, 0]
		self.device_names = ["Phone 1", "Phone 2"]
		self.device_ids = ["AA:BB:CC:DD:EE:FF", "00:11:22:33:44:55"]
		self.device_present = [ False, False ]
		self.logfile = "tracker.log"

		# google voice configuration
		self.gvuser = "user@gmail.com"
		self.gvpass = "pass40r12"
		self.notify = ["8580000000", "7600000000"]

		# ddwrt config
		self.router_user = "admin"
		self.router_pass = "r011t3r"
		self.router_page = "http://10.3.3.254/Status_Lan.asp"

		self.WriteConfig()
		print "Config file written"
		sys.exit()


	def ListToString( self, val ):
		x = 0
		ret = str()
		for item in val:
			if x > 0:
				ret += ","
			x += 1
			ret += str(item)
		return ret

	def StringToList( self, val ):
		x = 0
		return val.strip().split(',')

	# Reads the config into the class given the configuration as a parameter
	def ReadConfig( self, data ):
		config = ConfigParser.ConfigParser()
		config.readfp( io.BytesIO( data ) )

		# DDWRT Settings
		self.router_user = config.get( 'ddwrt', 'router_user', 1)
		self.router_pass = config.get( 'ddwrt', 'router_pass', 1)
		self.router_page = config.get( 'ddwrt', 'router_page', 1)
		self.router_auth += b64encode( self.router_user + ":" + self.router_pass )

		# GV Config
		self.gvuser = config.get( 'gvconfig', 'gvuser', 1 )
		self.gvpass = config.get( 'gvconfig', 'gvpass', 1 )
		self.notify = self.StringToList(config.get( 'gvconfig', 'notify', 1 ))
		self.threshold = int( config.get( 'gvconfig', 'threshold', 1 ) )

		# Tracker Configuration
		# for status, unserialize the integers
		status = self.StringToList( config.get( 'tracker', 'device_status', 1 ) )		
		for each in status:
			self.device_status.append( int(each) )

		# for present, use bools
		status = self.StringToList( config.get( 'tracker', 'device_present', 1 ) )
		for each in status:
			self.device_present.append( each == "True" )

		self.device_names = self.StringToList( config.get( 'tracker', 'device_names', 1 ) )
		self.device_ids = self.StringToList( config.get( 'tracker', 'device_ids', 1 ) )
		self.logfile = config.get( 'tracker', 'logfile', 1 )

	# Write the config with all the member variables of this class
	# in reverse order so that they appear cleanly
	def WriteConfig( self ):
		config = ConfigParser.ConfigParser()

		# DDWRT Settings
		config.add_section('ddwrt')
		config.set( 'ddwrt', '# router_page', 'Page to search device_ids out of')
		config.set( 'ddwrt', 'router_user', self.router_user )
		config.set( 'ddwrt', 'router_pass', self.router_pass )
		config.set( 'ddwrt', 'router_page', self.router_page )

		# GV Config
		config.add_section('gvconfig')
		config.set( 'gvconfig', '# notify', 'Comma separated list of phone numbers that will be notified' )
		config.set( 'gvconfig', '# threshold', 'Amount of pings a device must miss in order to send an alert' )
		config.set( 'gvconfig', 'gvuser', self.gvuser )
		config.set( 'gvconfig', 'gvpass', self.gvpass )
		config.set( 'gvconfig', 'notify', self.ListToString( self.notify ) )
		config.set( 'gvconfig', 'threshold', self.threshold )

		# Tracker configuration
		config.add_section( 'tracker' )
		config.set( 'tracker', '# device_ids', 'Comma separated list of the MAC addresses of each device to track' )
		config.set( 'tracker', '# device_names', 'Comma separated list of the names of the tracked devices' )
		config.set( 'tracker', '# device_status', 'Comma separated list of ping status of the device' )
		config.set( 'tracker', '# device_present', 'Comma separated list of True/False whether or not device is considered here' )
		config.set( 'tracker', 'device_ids', self.ListToString( self.device_ids ) )
		config.set( 'tracker', 'device_names', self.ListToString( self.device_names ) )
		config.set( 'tracker', 'device_present', self.ListToString( self.device_present ) )

		# for status, serialize the integers
		x = 0
		status = str()
		for each in self.device_status:
			if x > 0:
				status += ","
			x += 1
			status += str(each)
		config.set( 'tracker', 'device_status', status )

		# Logger Config
		config.set( 'tracker', 'logfile', self.logfile )

		# attempt to write the file
		with open(self.configfile, "wb") as configfile:
			config.write(configfile)

