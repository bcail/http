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


async def read_request(reader):
    request_line = await reader.readline()
    headers = []
    while True:
        line = await reader.readline()
        if line.strip():
            headers.append(line.decode('utf8').strip())
        else:
            break
    method, path, protocol = request_line.decode('utf8').strip().split()
    content_length = 0
    for h in headers:
        if 'content-length' in h.lower():
            content_length = int(h.split(':')[1].strip())
    request_body = b''
    if content_length:
        request_body = await reader.read(content_length)
    return {
        'method': method,
        'path': path,
        'protocol': protocol,
        'headers': headers,
        'body': request_body,
    }


def response_bytes(status, body):
    status_line = f'{PROTOCOL} {status} {status.phrase}'
    date_line = 'Date: %s' % datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length_line = f'Content-Length: {len(body)}'
    connection_line = 'Connection: close'
    headers = '\r\n'.join([status_line, SERVER_LINE, date_line, content_length_line, connection_line])
    return f'{headers}\r\n\r\n'.encode('utf8') + body


async def handle_request(reader, writer):
    request = await read_request(reader)

    if request['path'] == '/':
        status = HTTPStatus.OK
        if request['method'] == 'POST':
            body = request['body']
        else:
            body = '200 OK'.encode('utf8')
    else:
        status = HTTPStatus.NOT_FOUND
        body = '404 Not Found'.encode('utf8')

    output_msg = response_bytes(status, body)

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
