from threading import Thread
import main
import time

class msg_sender(Thread):
    def __init__(self, CONN, send_ascii):
        self.CONN = CONN
        self.send_ascii = send_ascii
        Thread.__init__(self)

    def run(self):
        print("initialized message sender")
        while True:
            if main.STILL_RUNS == False:
                break
            else:
                # send message of type group join
                if self.send_ascii == False:
                    cli_input = str(input())
                    if cli_input == "/exit":
                        main.STILL_RUNS = False
                else:
                    cli_input = str("" +
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
                message = "dslp/1.1\r\n" + "group notify\r\n" + cli_input + "\r\n" + "dslp/end\r\n"
                self.CONN.sendall(message.encode('utf-8'))
