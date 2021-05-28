#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback

from cryptography.fernet import Fernet #importacao biblioteca cryptography


class Server(threading.Thread):#Gerencia o que recebe do servidor
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        lis = []
        lis.append(self.receive)
        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        chunk = s
                        chave = open("chave_simetrica.key", "rb").read() #Ler a mensagem criptografada no arquivo mensagem
                        f = Fernet(chave)
                        chave_decrypt = f.decrypt(chunk) # desencriptografar  a mensagem usnando a chave simetrica
                        print(chave_decrypt.decode() + '\n>>')
                except:
                    traceback.print_exc(file=sys.stdout)
                    break





class Client(threading.Thread):
    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg):
        sent = self.sock.send(msg)
        # print "Sent\n"
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = input("Enter the server IP \n>>")
            port = int(input("Enter the server Destination Port\n>>"))
        except EOFError:
            print("Error")
            return 1

        print("Connecting\n")
        s = ''
        self.connect(host, port)
        print("Connected\n")
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()
        while 1:
            #Loop para o envio da mensagem ele encripta e desigpta a mensagem
            # print "Waiting for message\n"
            msg = input('>>')
            if msg == 'exit':
                break
            if msg == '':
                continue
            # print "Sending\n"
            msg = user_name + ': ' + msg
            chave = Fernet.generate_key() #gerar uma chave
            with open("chave_simetrica.key", "wb") as key_file: #criar um arquivo mensagem com a chave gerada
                key_file.write(chave) #inserir a chave no arquivo
            
            f = Fernet(chave)
            dado = msg.encode()
            encrypt = f.encrypt(dado) #encriptografa a chave simetrica
            self.client(host, port, encrypt)
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()