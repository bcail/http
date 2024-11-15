#!/usr/bin/env python3
'''
https://docs.python.org/3/library/asyncio-stream.html#examples
'''
import asyncio
import urllib.parse


def print_headers(headers):
    for header, value in headers.items():
        print(f'{header}: {value}')


async def web_client(url):
    print(url)
    url = urllib.parse.urlsplit(url)

    if url.scheme == 'http':
        port = 80
        use_ssl = False
    else:
        port = 443
        use_ssl = True

    if ':' in url.netloc:
        port = int(url.netloc.split(':')[-1])

    message = 'GET / HTTP/1.1\r\n\r\n'

    reader, writer = await asyncio.open_connection(
        url.hostname, port, ssl=use_ssl)

    writer.write(message.encode())
    await writer.drain()

    response_first_line = await reader.readline()
    response_first_line = response_first_line.decode('utf8').strip()
    print(f'Received: {response_first_line}')
    headers = {}
    while True: # read headers
        header_line = await reader.readline()
        if not header_line.strip():
            break
        header, value = header_line.decode('utf8').split(':', maxsplit=1)
        headers[header] = value.strip()

    print_headers(headers)

    writer.close()
    await writer.wait_closed()

asyncio.run(web_client('http://localhost:8000'))
