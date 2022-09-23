#!/usr/bin/env python3

import socket
import time
import sys
from multiprocessing import Process


#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    host = "www.google.com"
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ps:
        print("Starting porxy server")
        ps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        ps.bind((HOST, PORT))
        #set to listening mode
        ps.listen(1)
        
        #continuously listen for connections
        while True:
            conn, addr = ps.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pe:
                print("Connecting to google")
                remote_ip = get_remote_ip(host)
                pe.connect((remote_ip, port))
                p = Process(target=handle_echo, args=(pe, addr, conn))
                p.daemon = True
                p.start()
                print("Started Process ", p)
            conn.close()



def handle_echo(proxy_end, addr, conn):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)

if __name__ == "__main__":
    main()





