#!/usr/bin/env python3
import sys

def download(url: str, times: int) -> None:

    import socket
    import ssl
    import urllib

    import pip._internal.network.session

    parsed_url = urllib.parse.urlparse(url)

    assert parsed_url.scheme == 'https'

    rbody = b'GET ' + parsed_url.path.encode() + b' HTTP/1.1\r\n' \
        b'Host: files.pythonhosted.org\r\n' \
        b'User-Agent: ' + pip._internal.network.session.user_agent().encode() + b'\r\n' \
        b'Accept: */*\r\n' \
        b'Accept-Encoding: gzip, deflate, br\r\n' \
        b'Connection: Keep-Alive\r\n' \
        b'\r\n'

    bsize = 2**22

    hostname = parsed_url.netloc
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssock.settimeout(1)
            for i in range(times):
                try:
                    ssock.send(rbody)
                except TimeoutError:
                    print('Receiving crap')
                    while True:
                        try:
                            data = ssock.recv(bsize)
                        except TimeoutError:
                            print('all received')
                            break

                if i % 1024 == 0:
                    print(i)


def main():

    if len(sys.argv) != 3:
        sys.exit(f'Usage: {sys.argv[0]} url times')

    url = sys.argv[1]
    times = int(sys.argv[2])

    download(url, times)


if __name__ == '__main__':
    main()
