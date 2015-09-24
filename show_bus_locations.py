# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:21:52 2015

@author: clayton
"""

import sys
import json
import pandas as pd
import urllib2

if __name__=='__main__':
    # set values to read bus data
    api_key = sys.argv[1]
    busID = sys.argv[2]
    
    # set url with read in api_key and busID, request and read data from that url
    url = 'http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s' % (api_key, busID)
    req = urllib2.urlopen(url)
    data = json.loads(req.read())
    
    # extract active vehicles from downloaded data
    buses = pd.DataFrame(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0])
    
    # print bus line and total number of buses
    print 'Bus Line: ', busID
    print 'Number of active buses: ', buses.index.max()
    
    # iterate through bus list printing bus, lat, and lon
    for bus in buses.index.tolist():
        busLat = buses['VehicleActivity'][bus]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
        busLon = buses['VehicleActivity'][bus]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
        print 'Bus %s is at Latitude %s and Longitude %s' % (bus, busLat, busLon)
        
