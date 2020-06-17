#!/usr/bin/env python3
import json
from http import server, HTTPStatus
import socketserver
import ssl
import datetime
import uuid

class EndpointHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.common_handler()

    def do_POST(self):
        self.common_handler()

    def common_handler(self):
        response = {"uuid": str(uuid.uuid4()), "time": datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%S %p")}
        wire_data_byte = json.dumps(response).encode()

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-length", len(wire_data_byte))
        
        self.end_headers()
        self.wfile.write(wire_data_byte)

    @staticmethod
    def run():
        port = EndpointHandler.port
        print('INFO: (Secured: {})Sample Server listening on localhost:{}...'.format(EndpointHandler.secured,
                                                                                            port))
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(('', port), EndpointHandler)
        cert_path = 'yourpemfile.pem'
        print("DEBUG: cert_path = " + cert_path)
        if EndpointHandler.secured:
            httpd.socket = ssl.wrap_socket(
                httpd.socket, server_side=True, certfile=cert_path)
        httpd.serve_forever()

    port = 8000
    protocol_version = 'HTTP/1.1'
    secured = False

def main():
    """
        Run as a standalone server if needed
    """
    EndpointHandler.run()


if __name__ == '__main__':
    main()
