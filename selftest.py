"""Local tester for server.py and client.py - not the hidden grader.

    python3 selftest.py

Starts your server.py in the background and connects several clients: one slow, one fast, then
asks who is connected. Change the examples and try your own.
"""
import os
import socket
import subprocess
import sys
import threading
import time

HOST = "127.0.0.1"
PORT = 2405


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    server = subprocess.Popen([sys.executable, os.path.join(here, "server.py")], cwd=here)
    try:
        time.sleep(1)
        sys.path.insert(0, here)
        from client import run_command, who

        with socket.create_connection((HOST, PORT)) as slow, \
                socket.create_connection((HOST, PORT)) as fast:
            slow.settimeout(10)
            fast.settimeout(10)
            print("slow client address:", slow.getsockname())
            print("fast client address:", fast.getsockname())

            thread = threading.Thread(target=run_command, args=(slow, "sleep 3"))
            thread.start()
            time.sleep(0.2)
            start = time.time()
            print("fast client got:", run_command(fast, "echo fast")["stdout"].strip())
            print(f"after {time.time() - start:.2f} seconds (should be well under 3)")
            thread.join()

            print("who:", who(fast))
            slow.close()
            time.sleep(0.5)
            print("who after one left:", who(fast))
    finally:
        server.kill()


if __name__ == "__main__":
    main()
