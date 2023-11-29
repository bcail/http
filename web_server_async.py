'''
See https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
'''
import asyncio


async def handle_request(reader, writer):
    data = await reader.read(1024)
    input_msg = data.decode()
    addr = writer.get_extra_info('peername')

    print(f'Received {input_msg!r} from {addr!r}')

    output_msg = 'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>'
    print(f'Send: {output_msg!r}')
    writer.write(output_msg.encode('utf8'))
    await writer.drain()

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def main(port=8000):
    server = await asyncio.start_server(
        handle_request, '127.0.0.1', port)

    print(f'Serving on port {port}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
