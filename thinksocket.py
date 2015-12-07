import os
import socket
import struct
from time import sleep
from msgpack import packb, unpackb

THINKNODE_HOST = os.getenv("THINKNODE_HOST")
THINKNODE_PORT = int(os.getenv("THINKNODE_PORT"))
THINKNODE_PID  = os.getenv("THINKNODE_PID")
BUFFER_SIZE = 4096

class ThinkSocket(object):

    def __init__(self, sock=None):
        self.sock = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.sock.close()

    def connect(self, host=THINKNODE_HOST, port=THINKNODE_PORT):
        self.sock.connect((host, port))

    def decode_version(self, version):
        if version == 0:
            return "1"
        else:
            return None

    def decode_action(self, code):
        if code == 0:
            return "register"
        elif code == 1:
            return "function"
        elif code == 2:
            return "progress"
        elif code == 3:
            return "result"
        elif code == 4:
            return "failure"
        elif code == 5:
            return "ping"
        elif code == 6:
            return "pong"
        else:
            return None

    def encode_version(self, version):
        if version == "1":
            return bytearray.fromhex("00")
        else:
            return None

    def encode_action(self, action):
        if action == "register":
            return bytearray.fromhex("00")
        elif action == "function":
            return bytearray.fromhex("01")
        elif action == "progress":
            return bytearray.fromhex("02")
        elif action == "result":
            return bytearray.fromhex("03")
        elif action == "failure":
            return bytearray.fromhex("04")
        elif action == "ping":
            return bytearray.fromhex("05")
        elif action == "pong":
            return bytearray.fromhex("06")
        else:
            return None

    def encode_protocol(self, protocol):
        if protocol == "MsgPack":
            return bytearray.fromhex("0000")
        else:
            return None

    def send_header(self, version, action, length):
        v = self.encode_version(version)
        a = self.encode_action(action)
        r = bytearray.fromhex("00")
        l = bytearray(4)
        struct.pack_into(">I", l, 0, length)
        header = v + r + a + r + l
        self.sock.send(header)

    def send_result(self, result):
        msg = packb(result)
        length = len(msg)
        self.send_header("1", "result", length)
        self.sock.send(msg)

    def send_progress(self, progress, message):
        length = 4 + 2 + len(message)
        self.send_header("1", "progress", length)
        prog_info = bytearray(4)
        struct.pack_into(">f", prog_info, 0, progress)
        self.sock.send(prog_info)
        msg_len = bytearray(2)
        struct.pack_into(">H", msg_len, 0, len(message))
        self.sock.send(msg_len)
        self.sock.send(message)

    def receive(self, msglen):
        bytes_received = 0
        chunks = []

        while bytes_received < msglen:
            chunk = self.sock.recv(min(BUFFER_SIZE, msglen - bytes_received))
            # if we get an empty chunk, we've had an error
            if chunk == b"":
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_received = bytes_received + len(chunk)

        return "".join(chunks)

    def receive_header(self):
        header = {}
        chunked_header = self.receive(8)
        v, r1, c, r2, length = struct.unpack(">BBBBI", chunked_header)
        header["version"] = self.decode_version(v)
        header["action"] = self.decode_action(c)
        header["length"] = length
        return header

    def receive_request(self, length):
        # Receive name length
        chunked_name_length = self.receive(1)
        name_length = struct.unpack(">B", chunked_name_length)[0]

        # Receive name
        chunked_name = self.receive(name_length)
        name = chunked_name.decode("utf-8")

        # Receive argument count
        chunked_count = self.receive(2)
        count = struct.unpack(">H", chunked_count)[0]

        # Receive arguments one by one
        args = []
        for i in range(count):
            chunked_arg_length = self.receive(4)
            arg_length = struct.unpack(">I", chunked_arg_length)[0]
            chunked_arg = self.receive(arg_length)
            args.append(unpackb(chunked_arg))

        # Construct function
        func = {}
        func["name"] = name
        func["args"] = args

        return func

    def register(self):
        self.send_header("1", "register", 34)
        self.sock.send(self.encode_protocol("MsgPack"))
        self.sock.send(THINKNODE_PID);