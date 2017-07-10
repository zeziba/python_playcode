"""
Created By: Charles Engen

Copyright (c) 2017 Charles Engen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import sys
import threading
import time
from socket import *


DEBUG = False

def portscanner(host_id="127.0.0.1", ports=list(range(256))):

	global DEBUG
    
	threads = []
	ports_found = []
	
	class ThreadedScan(threading.Thread):
		
		def __init__(self, threadID, host, port):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.host = host
			self.port = port
			self._found = False
		
		def found(self):
			return self._found
		
		def run(self):
			try:
				connection_socket = socket(AF_INET, SOCK_STREAM)
				connection_socket.connect((self.host, self.port))
				connection_socket.close()
				ports_found.append(self.port)
			except:
				if DEBUG: print("Failed at port:" + str(self.port))
	
	for index, p in enumerate(ports):
	    threads.append(ThreadedScan("Thread" + str(index + 1), host_id, p))
		
	for t in threads:
		t.start()
	
	for item in threads:
		item.join()
	
	return ports_found
	
def main(ports_to):
	
	def get_host_by_name(host_):
		try:
			return gethostbyname(host_)
		except:
			return -1
	setdefaulttimeout(1)
	found_ports = dict(ports_to)
	for host in ports_to.keys():
		ip_ = get_host_by_name(host)
		if ip_:
			found_ports[host] = portscanner(ip_, found_ports[host])
	print("Found:\n" + str(found_ports))
	

if __name__ == "__main__":
	ports_to_scan = {}
	
	def parse(text):
		nums = []
		for chunk in text.split(","):
			if "-" in chunk:
				temp = chunk.split("-")
				nums = range(int(temp[0]), int(temp[1])+1)
			else:
				nums.append(int(chunk))
		return nums
	
	for index, arg in enumerate(sys.argv):
		if index > 0:
			t = arg.split(":")
			ports_to_scan[t[0]] = parse(t[1])
			if DEBUG: print("Begining Scan, Host and ports to get scanned:\n" + str(ports_to_scan))
			main(ports_to_scan)
	if len(sys.argv) == 1: print("Example: python portscanner.py 127.0.0.1:0,1,2,25-142,200,255\nCan also take multiple host/ports at one time\nExample: python portscanner.py 10.0.0.1:1-50 25.25.12.1:1,1,25")
