import socket
import sys

# TCP/IPソケットを作成する
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# サーバーが待ち受けている特定の場所にソケットを接続する
server_address = '/tmp/socket_file'
print('connecting to {}'.format(server_address))

try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

#  サーバーに接続できたら、サーバーにメッセージを送信する
try:
    message = input('メッセージを入力してください : ')
    sock.sendall(message.encode())
    
    # サーバーからの応答を待つ時間を2秒間に設定する
    sock.settimeout(2)

    # サーバーからの応答を待ち、応答があれば表示する
    try:
        while True:
            # サーバーからのデータを受け取る
            data = str(sock.recv(32))

            # データがあればそれを表示し、なければループを終了
            if data:
                print('Server response: ' + data)
            else:
                break
    
    except(TimeoutError):
        print('Socket timeout, ending listening for server messages')

# すべての操作が完了したら、最後にソケットを閉じて通信を終了する
finally:
    print('closing socket')
    sock.close()
