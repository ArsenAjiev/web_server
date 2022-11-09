import socket


def start_my_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('127.0.0.1', 8001)
        server.bind(address)
        server.listen(4)
        while True:
            print("working...")
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            content = load_page_from_get_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
    print('close socket')


def load_page_from_get_request(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = request_data.split(' ')[1]
    print(path)
    print(type(path))
    response = ''
    try:
        if path != '/':
            with open('views' + path, 'rb') as file:
                response = file.read()
            return HDRS.encode('utf-8') + response
        else:
            with open('views' + '/index.html', 'rb') as file:
                response = file.read()
            return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        with open('views' + '/error.html', 'rb') as file:
            response = file.read()

        return (HDRS_404).encode('utf-8') + response


if __name__ == '__main__':
    start_my_server()
