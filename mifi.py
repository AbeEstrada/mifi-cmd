#!/usr/bin/env python
import urllib2

class Mifi:
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
            elif f[0] == 'WwRssi':
                self.signal = f[1]

def main():
    mifi = Mifi()
    if mifi.status:
        print '%s %s' % (mifi.network, mifi.technology)
        print 'Signal: %s' % (mifi.signal)

if __name__ == '__main__':
    main()