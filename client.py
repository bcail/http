#!/usr/bin/env python3
from http.client import HTTPConnection, HTTPResponse

method = 'GET'
host = 'localhost'
port = 8000
path = '/'
print(f'Request: {method} -- {host}:{port}{path}')

con = HTTPConnection(host, port=port)
con.request(method, path)

r = con.getresponse()
print(f'{r.status} -- {r.reason}')
body = r.read().decode('utf8')
print(f'body: {body}')

# r = HTTPResponse(con.sock, method=con._method)
# raw_data = r.fp.read()
# print(raw_data.decode('utf8'))

con.close()
