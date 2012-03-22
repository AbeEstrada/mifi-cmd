#!/usr/bin/env python
import urllib2

class Mifi(object):
    status = False

    def __init__(self):
        url = 'http://192.168.1.1/getStatus.cgi?dataType=TEXT'

        try:
            response = urllib2.urlopen(url)
            data = response.read()
            self.status = True
            self.parsedata(data)
        except:
            self.status = False

    def parsedata(self, data):
        for feature in data.split("\x1b"):
            f = feature.split('=')
            if f[0] == 'WwNetwkName':
                self.network = f[1]
            elif f[0] == 'WwNetwkTech':
                self.technology = f[1]
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
            elif f[0] == 'BaBattStat':
                self.battery = int(f[1])
            elif f[0] == 'BaBattChg':
                if int(f[1]) == 0:
                    self.charging = 'Not Charging'
                elif int(f[1]):
                    self.charging = 'Charging'

def main():
    mifi = Mifi()
    if mifi.status:
        print '%s %s (%s)' % (mifi.network, mifi.technology, mifi.roaming)
        print 'Signal: %i' % (mifi.signal)
        print '%s' % (mifi.ip)
        print 'Battery: %s (%s)' % (mifi.battery, mifi.charging)

if __name__ == '__main__':
    main()