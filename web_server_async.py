#!/usr/bin/env python3
'''
https://github.com/python/cpython/blob/main/Lib/http/server.py
https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
https://ruslanspivak.com/lsbaws-part1/
'''
import asyncio
import datetime
from http.server import HTTPStatus
import sys


PROTOCOL = 'HTTP/1.1'
SERVER_LINE = 'Server: Apache'


async def handle_request(reader, writer):
    request_line = await reader.readline()
    headers = []
    while True:
        line = await reader.readline()
        if line.strip():
            headers.append(line.decode('utf8').strip())
        else:
            break
    method, path, protocol = request_line.decode('utf8').strip().split()

    if path == '/':
        status = HTTPStatus.OK
        text = '200 OK'
    else:
        status = HTTPStatus.NOT_FOUND
        text = '404 Not Found'

    body = text.encode('utf8')
    status_line = f'{PROTOCOL} {status} {status.phrase}'
    date_line = 'Date: %s' % datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length_line = f'Content-Length: {len(body)}'
    connection_line = 'Connection: close'
    headers = '\r\n'.join([status_line, SERVER_LINE, date_line, content_length_line, connection_line])
    output_msg = f'{headers}\r\n\r\n'.encode('utf8') + body
    writer.write(output_msg)
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main(port=8000):
    server = await asyncio.start_server(
        handle_request, '127.0.0.1', port)

    print(f'Serving on port {port}')

    async with server:
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nKeyboard interrupt received, exiting.")
    sys.exit(0)
