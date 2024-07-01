import socket
import os
from faker import Faker

fake = Faker()

# TCP/IPソケットを作成する
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# サーバーのUNIXソケットのパスを設定
server_address = '/tmp/socket_file'

# 以前の接続が残っていた場合は、サーバーアドレスをアンリンクする
try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}' .format(server_address))

# サーバーアドレスにソケットをバインドする
sock.bind(server_address)

# ソケットが接続要求を待機するようにする
sock.listen(1)

# クライアントからの接続を待つ
while True:
    # クライアントからの接続を受け入れる
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        while True:
            data = connection.recv(16)
            data_str = data.decode('utf-8')

            print('Received ' + data_str)

            if data:
                if data_str == 'name':
                    response = 'Processing ' + fake.name()
                elif data_str == 'address':
                    response = 'Processing ' + fake.address()
                else:
                    response = 'nameかaddressを入力してください'
                connection.sendall(response.encode())
            
            else:
                print('no data from', client_address)
                break

    finally:
        print("Closing current connection")
        connection.close()
