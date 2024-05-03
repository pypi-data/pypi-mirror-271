# net-input

Send mouse/keyboard inputs via network

## Installation

You can install the package via pip:

```
pip install net-input
```

## Usage

1. Start the server.

   ```
   net-input
   ```

1. Example client code.

   ```py
   import socket

   host, port = "127.0.0.1", 9999
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   sock.sendto(b"mouse,move,100,100", (host, port))
   sock.sendto(b"keyboard,write,Hello World", (host, port))
   ```

## License

This project is licensed under the terms of the MIT license.
