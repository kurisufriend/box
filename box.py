import socket
from PIL import Image
from io import BytesIO
from hashlib import sha256
from threading import Thread

_PORT = 1337

def handle_conn(conn):
    conn.sendall("hai~".encode("ascii"))
    data = b""
    while True:
        part = conn.recv(4096)
        if not part:
            break
        data += part
    try:
        img = Image.open(BytesIO(data))
    except OSError:
        conn.sendall("cannot parse image".encode("ascii"))
        return
    no_exif = Image.new(img.mode, img.size)# abandon metadata
    no_exif.putdata(list(img.getdata()))
    filename = f"store/{sha256(no_exif.tobytes()).hexdigest()}.{img.format.lower()}"
    no_exif.save(filename)
    conn.sendall(f"saved to {filename}".encode("ascii"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", _PORT))

s.listen()

while True:
    conn, conn_addr = s.accept()
    Thread(target=handle_conn, args=(conn,)).start()
