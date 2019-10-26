#!/bin/bash
# Script to update CGNSaaS with external IP from interface eth0
if ([ $reason = "BOUND" ] || [ $reason = "RENEW" ] || [ $reason = "CARRIER"])
then
        ipsec stop
        /usr/bin/python3 /home/pi/NSaaS_Pi/ip_update.py 2>&1 >> /var/log/ip_update.log
        echo "interface up script triggered" >> /var/log/ip_update.log
        ipsec start
fi
