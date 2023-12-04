'''
https://github.com/python/cpython/blob/main/Lib/http/server.py
https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
https://ruslanspivak.com/lsbaws-part1/
'''
import asyncio
from http.server import HTTPStatus


PROTOCOL = 'HTTP/1.1'


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
    else:
        status = HTTPStatus.NOT_FOUND

    output_msg = f'{PROTOCOL} {status} {status.phrase}\r\n\r\n'
    writer.write(output_msg.encode('utf8'))
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main(port=8000):
    server = await asyncio.start_server(
        handle_request, '127.0.0.1', port)

    print(f'Serving on port {port}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
