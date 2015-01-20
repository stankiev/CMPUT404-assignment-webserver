# coding: utf-8
import SocketServer
import os


# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Dylan Stankievech
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
	request_lines = []
	first_line_tokens = []
	uri = ""
	server_directory = "www"

	def handle(self):
		
		self.data = self.request.recv(1024).strip()
		self.request_lines = self.data.split("\r\n")
		valid = self.check_request()

		if (valid):
			self.uri = self.first_line_tokens[1]

			if ("/../" in self.uri):
				self.not_found()
				return

			if (self.uri[0] == "/"):
				self.uri = self.uri[1:]

			resource = self.server_directory + "/" + self.uri
			found = False

			if (os.path.isfile(resource)):
				found = True
			elif (resource.endswith("/") and os.path.isfile(resource + "index.html")):
				found = True
				resource = resource + "index.html"
			elif (os.path.isfile(resource + "/" + "index.html")):
				found = True
				resource = resource + "/" + "index.html"

			if (found):
				content_type = "Content-Type: "
				if (resource.endswith(".html")):
					content_type += "text/html; charset=utf-8"
				elif (resource.endswith(".css")):
					content_type += "text/css"
				elif (resource.endswith(".json")):
					content_type += "application/json"
				elif (resource.endswith(".js")):
					content_type += "application/javascript"
				elif (resource.endswith(".txt")):
					content_type += "text/plain; charset=utf-8"
				elif (resource.endswith(".pdf")):
					content_type += "application/pdf"
				elif (resource.endswith(".jpg") or resource.endswith(".jpeg")):
					content_type += "image/jpeg"
				else:
					self.unsupported_media()
					return
				
				f = open(resource)
 				contents = f.read()

				self.request.sendall("HTTP/1.1 200 OK\r\n" + content_type + "\r\n\r\n" + contents)
			else:
				self.not_found()
		else:
			self.bad_request()

	def check_request(self):
		if (len(self.request_lines) < 1):
			return False
	
		self.first_line_tokens = self.request_lines[0].split(" ")
		if (len(self.first_line_tokens) != 3):
			return False

		if (self.first_line_tokens[0] != "GET"):
			return False
		
		return True


	def bad_request(self):
		self.request.sendall("HTTP/1.1 400 Bad Request\r\n\r\n" + 
		"<!DOCTYPE html>" +
		"<html>" +
		"<head>" +
		"<title>400 Bad Request</title>" +
        "<meta http-equiv=\"Content-Type\"" +
        "content=\"text/html;charset=utf-8\"/>" +
		"</head>" +
		"<body>" +
		"<h1>400 Bad Request</h1>" +
		"</div>" +
		"</body>" +
		"</html>")

	def unsupported_media(self):
		self.request.sendall("HTTP/1.1 415 Unsupported Media Type\r\n\r\n" + 
		"<!DOCTYPE html>" +
		"<html>" +
		"<head>" +
		"<title>415 Unsupported</title>" +
        "<meta http-equiv=\"Content-Type\"" +
        "content=\"text/html;charset=utf-8\"/>" +
		"</head>" +
		"<body>" +
		"<h1>415 Unsupported Media Type</h1>" +
		"</div>" +
		"</body>" +
		"</html>")

	def not_found(self):
		self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n" + 
		"<!DOCTYPE html>" +
		"<html>" +
		"<head>" +
		"<title>404 Not Found</title>" +
        "<meta http-equiv=\"Content-Type\"" +
        "content=\"text/html;charset=utf-8\"/>" +
		"</head>" +
		"<body>" +
		"<h1>404 Page Missing</h1>" +
		"</div>" +
		"</body>" +
		"</html>")
		
		

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
