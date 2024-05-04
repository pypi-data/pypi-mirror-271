import network
import time
import socket


class Server:
    def __init__(self, debug=False):
        self.pages = {}
        self.debug = debug

    def not_found_page(*args, **kwargs):
        return """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
                <body><h1>404</h1>
                </body></html>
                """

    def page_add(self, path, page_f, advanced=False):
        self.pages[path] = (page_f, advanced)

    def resolve_path(self, path):
        if path in self.pages:
            return self.pages[path]
        else:
            return (self.not_found_page, False)

    # if you do not see the network you may have to power cycle
    # unplug your pico w for 10 seconds and plug it in again
    def connect_wifi(self, ssid, password):
        self.ssid = ssid

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        if self.debug:
            print(1)
        self.wlan.connect(ssid, password)
        while (status := self.wlan.status()) == network.STAT_CONNECTING:
            time.sleep(0.1)

        if status == network.STAT_WRONG_PASSWORD:
            raise Exception("Wrong password. Connection failed.")
        if status == network.STAT_NO_AP_FOUND:
            raise Exception(
                "Network not found. Check SSID is correct and AP is reachable."
            )
        if status == network.STAT_CONNECT_FAIL:
            raise Exception("Connection to wifi failed due to other problems.")

        if status == network.STAT_GOT_IP:
            print("Pico connected to Wifi")
            print(f"Device IP address: {self.wlan.ifconfig()[0]}")
        else:
            raise Exception(f"Connection to wifi failed. {status}")

        self.s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # creating socket object
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(("", 80))
        self.s.listen(5)
        print("Pico is now listening for network traffic on port 80")
        if self.debug:
            print(2)

    def start(self):
        while True:
            try:
                if self.debug:
                    print(3)
                conn, addr = self.s.accept()
                print(
                    f"{chr(58).join([str(i) for i in time.localtime()[3:6]])} Received a connection from {addr}"
                )
                request = conn.recv(1024)
                if self.debug:
                    print(4)
                print(1)
                # Parse the request message
                request_lines = request.decode().split("\r\n")
                path = request_lines[0].split()[1]
                print(f"Requested path: {path}")

                # determine which function based on path
                page_f, advanced = self.resolve_path(path)
                if self.debug:
                    print(5)

                # generate response
                if advanced:
                    response = page_f(request_lines)
                else:
                    response = page_f()
                if self.debug:
                    print(6)

                headers = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response)}\r\n\r\n"

                conn.sendall(headers + response)
                conn.close()
                if self.debug:
                    print(7)
            except Exception as e:
                print(e)

    def disconnect_wifi(self):
        self.wlan.disconnect()
