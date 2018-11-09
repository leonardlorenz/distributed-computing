from threading import Thread
import time

class msg_sender(Thread):
    def __init__(self, CONN, send_ascii):
        self.CONN = CONN
        self.send_ascii = send_ascii
        Thread.__init__(self)

    def run(self):
        print("initialized message sender")
        while True:
            # send message of type group join
            if self.send_ascii == True:
                cli_input = str("\n" +
                "\n░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄"+
                "\n░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄"+
                "\n░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█"+
                "\n░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░█"+
                "\n░▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░█"+
                "\n█▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒█"+
                "\n█▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█"+
                "\n░█▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█"+
                "\n░░█░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█"+
                "\n░░░█░░██░░▀█▄▄▄█▄▄█▄████░█"+
                "\n░░░░█░░░▀▀▄░█░░░█░███████░█"+
                "\n░░░░░▀▄░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█"+
                "\n░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░█"+
                "\n░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░█"+
                "\n░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░█")
                time.sleep(5)
            else:
                cli_input = str(input())
                print("input saved")
                if cli_input == "/exit":
                    break;
            message = "dslp/1.1\r\n" + cli_input + "\r\n" + "dslp/end\r\n"
            self.CONN.sendall(message.encode('utf-8'))
            print("input sent")
