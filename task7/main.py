import socket

HOST = ""
PORT = "44444"

def main():
    SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
	s.bind((HOST, PORT))
    except socket.error as msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
    SOCK.listen(10)
    while True:
        SOCK.accept()

if __name__ == "__main__":
    main()
