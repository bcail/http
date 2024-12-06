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
from functools import partial
import io
import sys


def default_handler(request):
    path = request['path']
    headers = {}
    body = b''

    if path == '/':
        status = 200
        if request['method'] == 'POST':
            body = request['body'].read()
        else:
            body = '200 OK'.encode('utf8')
    else:
        status = 404
        body = '404 Not Found'.encode('utf8')
    if body:
        headers['Content-Length'] = len(body)
    return {
        'status': status,
        'headers': headers,
        'body': io.BytesIO(body),
    }


def log(message):
    print(f'{datetime.datetime.now()} {message}')


RESPONSE_STATUSES = {
    200: 'OK',
    401: 'Unauthorized',
    404: 'Not Found',
}


async def read_request(reader):
    request_line = await reader.readline()
    headers = {}
    while True:
        line = await reader.readline()
        header_line = line.decode('utf8').strip()
        if header_line:
            header, value = header_line.split(':', maxsplit=1)
            headers[header.lower()] = value.strip()
        else:
            break
    content_length = int(headers.get('content-length', '0'))
    body = b''
    if content_length:
        body = await reader.read(content_length)
    method, path, protocol = request_line.decode('utf8').strip().split()
    if '?' in path:
        path, query = path.split('?')
    else:
        query = ''
    return {
        'protocol': protocol,
        'method': method,
        'path': path,
        'query': query,
        'headers': headers,
        'body': io.BytesIO(body),
    }


def response_header_bytes(response):
    status_line = f'HTTP/1.1 {response["status"]} {RESPONSE_STATUSES[response["status"]]}'
    date_line = 'Date: %s' % datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers = '\r\n'.join([status_line, date_line, 'Server: Apache'] + [f'{header}: {value}' for header, value in response['headers'].items()])
    return f'{headers}\r\n\r\n'.encode('utf8')


async def handle_request(reader, writer, handler):
    try:
        request = await read_request(reader)
        response = handler(request)

        headers = response_header_bytes(response)

        writer.write(headers)
        await writer.drain()

        if response['body']:
            writer.write(response['body'].read())
            await writer.drain()

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        log(str(e))


async def main(port=8000, handler=None):
    if not handler:
        handler = default_handler
    server = await asyncio.start_server(
        partial(handle_request, handler=handler), '127.0.0.1', port)

    print(f'Serving on port {port}')

    async with server:
        await server.serve_forever()


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run()
