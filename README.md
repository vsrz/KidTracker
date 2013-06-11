KidTracker
==========

Small python application that scrapes a DD-WRT ARP Table and alerts you via text when a client joins or leaves the wireless network. I use it to figure out when my kids' cell phones get in wireless range after school. This effectively lets me know when they get home.


Requirements
------------

Requires installation of the pygooglevoice API created by Joe McCall & Justin Quick. Get it at https://github.com/pettazz/pygooglevoice.

Call main.py in a cronjob in the interval to poll the system. On the first run, a configuration file "tracker.cfg" will be generated. Edit this file before running it again.


Potential Issues
----------------

Sometimes devices can fall off the ARP table, especially if they are not talking for a period of time. Probably need to figure out a way to have the router ping the broadcast IP just before the cronjob runs for this process. You could schedule the cron between a certain time period where you expect the device to show up to shorten the probability that a device will be undetected due to an ARP timeout.

Increasing the threshold in tracker.cfg will help alleviate this, but will throw off the speed at which you will receive your alerts. In my setup, I poll every minute, and send an alert once a device appears active after 5 polls.
