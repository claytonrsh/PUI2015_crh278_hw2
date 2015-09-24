# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:21:52 2015

@author: clayton
"""

import sys
import json
import pandas as pd
import urllib2

if __name__ == '__main__':
    # set values to read bus data
    api_key = sys.argv[1]
    busID = sys.argv[2]

    # set url with read in api_key and busID
    url = 'http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=' \
        + '%s&VehicleMonitoringDetailLevel=calls&LineRef=%s' \
        % (api_key, busID)
    req = urllib2.urlopen(url)  # request url
    data = json.loads(req.read())  # read data

    # extract active vehicles from downloaded data
    buses = pd.DataFrame(data['Siri']['ServiceDelivery']
                             ['VehicleMonitoringDelivery'][0])

    # check if entered route has buses
    if 'VehicleActivity' in buses.columns:
        # initialize column names and output DataFrame
        columns = ['Latitude', 'Longitude', 'Stop Name', 'Stop Status']
        output = pd.DataFrame(data=None, columns=columns)

        # iterate through bus list printing bus, lat, and lon
        for bus in buses.index.tolist():
            busLat = buses['VehicleActivity'][bus][
                'MonitoredVehicleJourney']['VehicleLocation']['Latitude']
            busLon = buses['VehicleActivity'][bus][
                'MonitoredVehicleJourney']['VehicleLocation']['Longitude']
            # check if OnwardCalls exists
            if 'OnwardCalls' in buses['VehicleActivity'][bus][
                    'MonitoredVehicleJourney']:
                stopName = buses['VehicleActivity'][bus][
                    'MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][
                    0]['StopPointName']
                stopStatus = buses['VehicleActivity'][bus][
                    'MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][
                    0]['Extensions']['Distances']['PresentableDistance']
            else:
                stopName = 'NA'
                stopStatus = 'NA'
            newRow = pd.DataFrame({
                'Latitude': busLat, 'Longitude': busLon,
                'Stop Name': stopName, 'Stop Status': stopStatus},
                index=[bus])
            output = output.append(newRow)

        # write to csv
        output.to_csv(sys.argv[3], encoding='utf-8', index=False)
        print 'csv written!'
    else:
        print 'Oops, no buses for route %s!' % (busID)
