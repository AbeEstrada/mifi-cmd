#!/usr/bin/env python

def status():
    import urllib2
    url = 'http://192.168.1.1/getStatus.cgi?dataType=TEXT'
    response = urllib2.urlopen(url)
    data = response.read()
    print data

if __name__ == '__main__':
    status()