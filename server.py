import multiprocessing
import threading
import asyncio
from socket import socket
from time import sleep
import socket
import requests
from bs4 import BeautifulSoup
import pickle
import random
# Variables and configurations
download = 'Get off my client'
url1 = 'Enter webpage1024'
file_no=str(random.randint(0,100000))
filename = f'downloaded_page{file_no}.html'
msg = 'Enter password1024'
host = '192.168.6.76'
port = 8080
login = False
auth = '1024'
conf = 'Welcome'
option1 = '1. Html'
option2 = '2. Agent'
agent=False
# Function to save and send webpage
def save_and_send_webpage(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        print(f"Webpage saved as {filename}")


    # First loop handling client connection

while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn: socket
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                conn.sendall(msg.encode('ascii'))
                while True:
                    data = conn.recv(1024)
                    decode= data.decode('ascii')
                    if not data:
                        break
                    if 'erebos' == str(decode) or login == True:
                        login = True
                        conn.sendall(conf.encode("ascii"))
                        sleep(0.5)
                        conn.sendall(option1.encode("ascii"))
                        sleep(0.5)
                        conn.sendall(option2.encode("ascii"))
                        conn.sendall(auth.encode('ascii'))
                        while True:
                            data = conn.recv(1024)
                            if data.decode('ascii') == '1':
                                conn.sendall(url1.encode('ascii'))
                                url = conn.recv(1024)
                                page = 'https://'+url.decode('ascii')
                                save_and_send_webpage(page, filename)
                                with open(filename, 'rb') as file:
                                    conn.send(b'4153')
                                    conn.sendall(file.read())

                            elif data.decode('ascii') == '2':
                                conn.send(b'Agent connecting')
                                if input('Connect to client? Y/N') == 'y' or 'Y':
                                    conn.send(b'Agent connected')
                                    while True:
                                        while True:
                                            data = conn.recv(1024).decode()
                                            if not data or data.lower() == 'exit':
                                                print("Client disconnected or sent 'exit'")
                                                break
                                            print(f"Client: {data}")
                                            msg = input("Server: ")
                                            conn.send(msg.encode())
                                            if msg.lower() == 'exit':
                                                break




                    elif decode != 'erebos':
                        conn.send(b'Get off my client')
                        print('Ejected invalid user at', addr)
                        login=False
                        sleep(5)
                        conn.close()
                        s.close()

# Second loop for handling user input and communication


