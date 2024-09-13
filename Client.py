import random
import socket

fileno=0
output='html'+ str(fileno+1)
HOST = '192.168.6.76'  # The server's hostname or IP address
PORT = 8080  # The port used by the server
communica=True
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print('no connection :( please try again later')


        while True:
            data = s.recv(1024)
            thing = data.decode('ascii')
            question = thing.replace('1024', '')
            if thing != '':
                print(question)
            if '1024' in thing:  # Use the already decoded 'thing'
                msg = input('\n')
                s.sendall(msg.encode('ascii'))
            if thing == '4153':
                with open(output, 'wb') as f:
                    output = 'html' + str(random.randint(1,1000000))
                    while True:
                        data = s.recv(1024)
                        print('recieving file')# Receive data in chunks
                        if not data:
                            print('File transported')# If no more data is sent, break the loop
                            break
                        f.write(data)
            if 'Agent connected' in thing:
                while True:
                    msg = input("Client: ")
                    s.send(msg.encode())
                    if msg.lower() == 'exit':
                        break
                    data = s.recv(1024).decode()
                    print(f"Server: {data}")
                    if data.lower() == 'exit':
                        break







