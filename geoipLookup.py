#!/usr/bin/python
import sys
import pygeoip
from collections import defaultdict

gic = pygeoip.GeoIP('GeoIPCity.dat')
gio = pygeoip.GeoIP('GeoIPOrg.dat')
gi = pygeoip.GeoIP('GeoIPISP.dat')

resultColumns = ['ip', 'org', 'isp', 'region_name', 'city', 'postal_code', 'country_code', 'country_code3', 'country_name', 'area_code', 'metro_code', 'latitude', 'longitude']

sys.stdout.write('|'.join(resultColumns) + '\n')

for ip in sys.stdin.readlines():

    ip = ip.strip()
    org = gio.org_by_addr(ip)
    isp = gi.org_by_addr(ip)

    if org == None:
        org = unicode('')

    if isp == None:
        isp = unicode('')

    locationResult = gic.record_by_addr(ip)

    if locationResult == None:
        locationResult = {}        

    resultDict = defaultdict(unicode)

    for locationColumn in resultColumns:
        resultDict[locationColumn] = ''
        try:
            if locationColumn in locationResult:
                resultDict[locationColumn] = unicode(locationResult[locationColumn])
        except:
            print locationResult
            print sys.exc_info()

    resultDict['ip'] = ip    
    resultDict['org'] = org
    resultDict['isp'] = isp

    result = []

    for resultColumn in resultColumns:
        result.append(resultDict[resultColumn])

    sys.stdout.write('|'.join(result).encode('utf-8') + '\n')
