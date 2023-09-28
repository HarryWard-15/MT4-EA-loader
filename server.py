import http.server
import socketserver
import subprocess

# Set the port you want the server to run on
port = 8000

# Create a custom request handler
class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/run_script':
            # Set the response header to indicate JSON content
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            try:
                # Execute the Python script
                result = subprocess.check_output(['python', 'ChannelMessages.py'], stderr=subprocess.STDOUT, universal_newlines=True)

                # Send the script's output as a response
                self.wfile.write(result.encode('utf-8'))
            except subprocess.CalledProcessError as e:
                # Handle script execution errors
                error_message = f"Error: {e.returncode}\n{e.output}"
                self.wfile.write(error_message.encode('utf-8'))
        else:
            # Serve files as usual for other paths
            http.server.SimpleHTTPRequestHandler.do_GET(self)

# Start the server with the custom request handler
with socketserver.TCPServer(("", port), CustomHandler) as httpd:
    print(f"Serving at port {port}")
    try:
        # The server will run until you manually stop it (e.g., by pressing Ctrl+C)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
