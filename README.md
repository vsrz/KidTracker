KidTracker
==========

Small python application that scrapes a DD-WRT ARP Table and alerts you via text when a client joins or leaves the wireless network. I use it to figure out when my kids' cell phones get in wireless range after school. This effectively lets me know when they get home.


Requirements
------------

Requires installation of the pygooglevoice API created by Joe McCall & Justin Quick. Get it at https://github.com/pettazz/pygooglevoice.

HttpReader.py is only written to work with DD-WRT at this time, since that's the router I have. If you want to make it work for yours, you'll have to provide your own search string and webpage to poll. 

Call main.py in a cronjob in the interval to poll the system. On the first run, a configuration file "tracker.cfg" will be generated. Edit this file before running it again.


Potential Issues
----------------

The whole premise of this relies on the ability to read the ARP table of the main router. DD-WRT makes this table available on Status_Lan.asp which makes this easy in my case. If your particular router doesn't have an easy way to fetch the ARP table via a webpage, you'll need to come up with another plan.
