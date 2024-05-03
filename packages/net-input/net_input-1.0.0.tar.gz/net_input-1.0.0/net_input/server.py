import re
import socketserver

import keyboard
import mouse  # type: ignore


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data: bytes = self.request[0]
        command = data.decode()
        if match := re.fullmatch(r"mouse,move,(\d+),(\d+)", command):
            x, y = match.groups()
            x, y = int(x), int(y)
            mouse.move(x, y)  # type: ignore
        elif match := re.fullmatch(r"mouse,press,(\w+)", command):
            button = match.group(1)
            mouse.press(button)
        elif match := re.fullmatch(r"mouse,release,(\w+)", command):
            button = match.group(1)
            mouse.release(button)
        elif match := re.fullmatch(r"keyboard,press,(.+)", command):
            key = match.group(1)
            keyboard.press(key)
        elif match := re.fullmatch(r"keyboard,release,(.+)", command):
            key = match.group(1)
            keyboard.release(key)
        elif match := re.fullmatch(r"keyboard,write,(.+)", command):
            text = match.group(1)
            keyboard.write(text, delay=0.035)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        print(f"Starting server at {HOST}:{PORT}")
        server.serve_forever()
