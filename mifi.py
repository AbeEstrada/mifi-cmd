#!/usr/bin/env python
import sys
import urllib
import urllib2
from bs4 import BeautifulSoup

class Mifi(object):
    status = False

    def __init__(self):
        url = 'http://192.168.1.1/getStatus.cgi?dataType=TEXT'
        try:
            response = urllib2.urlopen(url)
            data = response.read()
            self.status = True
            self.parseData(data)
        except:
            self.status = False

    def parseData(self, data):
        for feature in data.split("\x1b"):
            f = feature.split('=')
            if f[0] == 'WwNetwkName':
                self.network = f[1]
            elif f[0] == 'WwNetwkTech':
                self.technology = f[1]
            elif f[0] == 'WwConnStatus':
                self.connectionStatus = int(f[1])
                if int(f[1]) == 0:
                    self.connection = 'Searching'
                elif int(f[1]) == 1:
                    self.connection = 'Connecting'
                elif int(f[1]) == 2:
                    self.connection = 'Connected'
                elif int(f[1]) == 3:
                    self.connection = 'Disconnecting'
                elif int(f[1]) == 4:
                    self.connection = 'Disconnected'
                elif int(f[1]) == 5:
                    self.connection = 'Not Activated (EVDO)'
                elif int(f[1]) == 6:
                    self.connection = 'Modem Failure'
                elif int(f[1]) == 7:
                    self.connection = 'No SIM'
                elif int(f[1]) == 8:
                    self.connection = 'SIM Locked'
                elif int(f[1]) == 9:
                    self.connection = 'SIM Failure'
                elif int(f[1]) == 10:
                    self.connection = 'Network Locked (invalid SIM)'
                elif int(f[1]) == 11:
                    self.connection = 'Dormant (EVDO)'
            elif f[0] == 'WwRoaming':
                if int(f[1]) == 0:
                    self.roaming = 'Not Roaming'
                elif int(f[1]) == 1:
                    self.roaming = 'Roaming'
                elif int(f[1]) == 2:
                    self.roaming = 'Extended Network'
            elif f[0] == 'WwRssi':
                self.signal = int(f[1])
            elif f[0] == 'WwIpAddr':
                self.ip = f[1]
            elif f[0] == 'WwDNS1':
                self.dns = f[1]
            elif f[0] == 'BaBattStat':
                self.battery = int(f[1])
            elif f[0] == 'BaBattChg':
                if int(f[1]) == 0:
                    self.charging = 'Not Charging'
                elif int(f[1]) == 1:
                    self.charging = 'Charging'

    def stoken(self):
        url = 'http://192.168.1.1/'
        try:
            response = urllib2.urlopen(url)
            data = response.read()
            soup = BeautifulSoup(data)
            return soup.find('input', attrs={ 'name': 'stoken' }).get('value')
        except:
            return False

    def connect(self):
        self.c('connect')

    def disconnect(self):
        self.c('disconnect')

    def c(self, action):
        url = 'http://192.168.1.1/wwan.cgi'
        token = self.stoken()
        if token:
            if action == 'connect' or action == 'disconnect':
                values = { 'nextfile': '204', 'todo': action, 'stoken': token }
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                print response.read()

def status():
    mifi = Mifi()
    if mifi.status:
        print '%s %s (%s)' % (mifi.network, mifi.technology, mifi.roaming)
        print 'Signal: %i' % (mifi.signal)
        print 'Status: %s' % (mifi.connection)
        if mifi.connectionStatus == 2:
            print '%s - %s' % (mifi.ip, mifi.dns)
        print 'Battery: %s (%s)' % (mifi.battery, mifi.charging)

def main(argv):
    mifi = Mifi()
    if len(argv) > 0:
        if argv[0] == 'connect':
            if mifi.connection == 'Disconnected':
                mifi.connect()
                print 'Connecting...'
            else:
                status()
        elif argv[0] == 'disconnect':
            if mifi.connection == 'Connected' or mifi.connection == 'Dormant' or
                mifi.connection == 'No SIM': # No SIM (it's a bug)
                mifi.disconnect()
                print 'Disconnecting...'
            else:
                status()
        else:
            status()
    else:
        status()

if __name__ == '__main__':
    main(sys.argv[1:])