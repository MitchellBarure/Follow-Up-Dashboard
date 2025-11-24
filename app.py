"""
app.py
This script acts as a middleman between the Google sheet and the frontend BY:
 1. Listening for HTTP requests
 2. Talking to sheets_client.py to read, create and update records
 3. Returning JSON data to the user
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from sheets_client import read_records, update_record, add_record

HOST = "0.0.0.0"
PORT = 8080

#Direct server on what to do when a requests comes through
class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    #Read all records using API endpoint (gET api/records)
    def do_GET(self):
        if self.path == "/api/records":
            try:
                records = read_records()
                self._set_headers(200)
                self.wfile.write(json.dumps(records).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    #Create a new record using API endpoint (Post api/records)
    def do_POST(self):
        if self.path == "/api/records":
            content_length = int(self.headers.get("Content-Length", 0))
            body_data = self.rfile.read(content_length).decode()

            try:
                body_json = json.loads(body_data)

                name = body_json.get("name")
                phone = body_json.get("phone")
                assigned_to = body_json.get("assignedTo")
                category = body_json.get("category")
                status = body_json.get("status")
                notes = body_json.get("notes", "")

                #Input Validation
                if not name or not phone or not assigned_to or not category:
                    raise ValueError("Missing required fields")

                new_id = add_record(name, phone, assigned_to, category, status, notes)

                self._set_headers(201)
                self.wfile.write(json.dumps({
                    "message": "Record added",
                    "id": new_id
                }).encode())

            except ValueError as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": "Internal server error"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    #Update a record using an API endpoint (Put /api/records/<id>)
    def do_PUT(self):
        if self.path.startswith("/api/records/"):
            record_id = self.path.split("/")[-1]

            content_length = int(self.headers.get("Content-Length", 0))
            body_data = self.rfile.read(content_length).decode()

            try:
                body_json = json.loads(body_data)
                status = body_json.get("status")
                notes = body_json.get("notes")

                if not status:
                    raise ValueError("Missing status field")

                #Call update_record
                success = update_record(record_id, status, notes)

                #Error handling: check if the record id exists
                if success:
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"Message": "Record Updated"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"Error": "Record Not Found"}).encode())

            except ValueError as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"Error": str(e)}).encode())

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"Error": "internal server error!"}).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

def run():
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Server running on http://{HOST}:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()