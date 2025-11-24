Ministry Follow-Up Dashboard: Rescuing Follow-Up from Google Sheet Hell

A small, full-stack application designed to modernize and streamline the crucial contact follow-up process for ministry or fellowship teams.

I built this app to replace manual, error-prone scrolling through sprawling Google Sheets. This dashboard provides a focused, real-time workflow interface that just works:

I read records from a shared Google Sheet using the Google Sheets API (treating it like a live, dynamic data store).

I present the data in a responsive web UI with advanced search and filters that actually save time.

I allow team members to efficiently update a contact's status and notes without ever opening the spreadsheet.

I enable the team lead to create new records directly via the UI.

I write all changes back to the same Google Sheet instantly, maintaining a single source of truth for the whole team.

TABLE OF CONTENTS

Overview

Features

Tech Stack

Architecture

Prerequisites

Installation & Setup

Local Development

Google Sheets API Setup

Deployment

API Documentation

Usage

Project Structure

Error Handling

Challenges & Solutions

Credits

License

Contact

1. Overview

This application is a custom web solution built to rescue ministry teams from the pain of Google Sheet overload. By leveraging the Google Sheets API v4, I created a dashboard that enforces workflow, provides status controls, and streamlines team coordination—all things a static spreadsheet cannot handle alone. This delivers genuine, practical value to the end-users.

Target Audience: Ministry, church, or fellowship teams responsible for managing outreach or attendee follow-up pipelines.

Live Demo: ?insert url

2. Features

Real-time Google Sheets Integration: Instant data exchange with the external API ensures the dashboard and the Sheet are always in sync.

Advanced Data Interaction: Filter by status or category, and search by name or phone number—making data actionable instead of overwhelming.

Status Management: Clear, enforced workflow states for tracking progress (NOT_CONTACTED, COMING, etc.).

Load Balanced: Deployed across two separate servers (Web01, Web02) for high availability, meaning the application is reliable and always accessible.

Responsive Design: Fully usable on desktop, tablet, and mobile devices for updates on-the-go.

3. Tech Stack

Frontend: Vanilla HTML, CSS, & JavaScript (keeping the client lightweight and fast).

Backend: Python, http.server (standard library module), Google Sheets API v4.

Key Python Dependencies: google-api-python-client, gspread, oauth2client (for secure API communication).

Data Store: A designated Google Sheet (simple, shared data persistence).

Infrastructure: Nginx web server, Systemd (for service management), Load Balancer (LB-01), and two Ubuntu web servers (Web01, Web02).

4. Architecture

The application is deployed using a robust, highly available three-tier architecture. This implementation is crucial for stability and ensuring continuous service.

On Each Web Server (Web01, Web02):

Nginx (Port 80): Acts as the entry point. It serves the static frontend files (index.html, styles.css, app.js) directly for maximum speed.

Reverse Proxy (Port 8000): Nginx proxies all dynamic API requests (/api/) directly to the Python server running on port 8000.

Python Backend (app.py): The standard Python server runs continuously on port 8000, processes the request, and handles all external communication with the Google Sheets API.

Systemd: Manages and monitors the Python server process, ensuring the API is always running and automatically restarted if it fails.

Load Balancing (LB-01):
The dedicated Load Balancer uses Nginx's upstream module with a Round Robin algorithm to distribute incoming user traffic evenly to Web01 and Web02. Since the application is stateless (all data is externalized to the Sheets API), this provides seamless redundancy.

5. Prerequisites

Python 3.8+

Google Cloud Platform (GCP) Account with Google Sheets API enabled.

Admin access (via SSH) to three Ubuntu servers (Web01, Web02, LB-01).

A domain name configured to point to the Load Balancer's public IP.

6. Installation & Setup

Local Development

Clone & Enter the repo:
- git clone [https://github.com/MitchellBarure/Follow-Up-Dashboard.git](https://github.com/MitchellBarure/Follow-Up-Dashboard.git)
- cd Follow-Up-Dashboard

Set up & Activate Python Virtual Environment:
- python3 -m venv venv
- source venv/bin/activate

Install dependencies:
- pip install -r requirements.txt
- Configure the environment: Create a .env file containing the Sheet ID and local path to your credentials.json. NEVER commit this file to Git.

Run the Backend API Server (simple testing only):
- python app.py

Open the Frontend (using a static server): Open a new terminal window:
- python3 -m http.server 3000

Visit http://localhost:3000 to interact with the dashboard.


Google Sheets API Setup

- Create a Google Cloud Project and enable the Google Sheets API.

- Create a Service Account and download the JSON key file (credentials.json).

- Set up a Google Sheet with the required headers.

- Configure the credentials: Share the Google Sheet (Editor access) with the Service Account's email address (found in your JSON key file).


7. Deployment

The deployment process ensures the application runs robustly across the two web servers before the Load Balancer (LB-01) routes traffic.

A. Server Setup (Web01 & Web02)

Install Base Dependencies: Install Python, Nginx, and Git on both servers.

sudo apt update && sudo apt install python3 python3-pip python3-venv nginx git



Clone and Setup App: Clone the repository and set up the virtual environment (venv). Install all dependencies.

Configure Python Service (Systemd): This critical step ensures high uptime and auto-restart capability for the Python server.

Create the service file (/etc/systemd/system/followup.service).

Note: The ExecStart command uses the full path to the Python executable inside the virtual environment to start app.py directly on port 8000.

Enable and start the service:

sudo systemctl daemon-reload
sudo systemctl start followup.service
sudo systemctl enable followup.service



Configure Nginx (Reverse Proxy):

Create the Nginx configuration file (/etc/nginx/sites-available/fellowship_dashboard).

The configuration serves static assets directly and explicitly proxies API requests to the Python process running on port 8000:

# Snippet from Nginx config:
location /api/ {
# Proxy directly to the python http.server process
proxy_pass [http://127.0.0.1:8000](http://127.0.0.1:8000);
# ... standard proxy headers
}



Enable the site and restart Nginx.

Test Individual Servers: Confirm the app is fully functional on each server's IP address.

B. Load Balancer Configuration (LB-01)

Define Upstream Servers: Configure Nginx on LB-01 to route traffic to the two web servers (Web01, Web02) on port 80.

# Snippet from Nginx Load Balancer config:
upstream dashboard_backend {
# Using Round Robin distribution (default)
server web01_internal_ip:80;
server web02_internal_ip:80;
}

server {
listen 80;
server_name map.yourdomain.tech;
location / {
proxy_pass http://dashboard_backend;
# ... standard proxy headers
}
}



Verification: Restart Nginx and access the application via the public domain. I verify traffic is correctly distributed by checking the access logs on Web01 and Web02.

8. API Documentation

The application exposes a minimal RESTful API for data interaction.?

Base URL:

Local: http://localhost:8000

Production: http://3.87.53.138 (The application is accessed via the load balancer’s public IP address)

Endpoints:

GET /api/contacts: I retrieve all contacts from Google Sheets.

PUT /api/contacts/:id: I update contact status and notes based on the contact's unique row index (:id).

POST /api/contacts: I create a new contact record.

Status Values:

NOT_CONTACTED

CONTACTED

COMING

NOT_COMING

MAYBE

9. Usage

Team Members

Team members primarily focus on filtering the dataset and using the Edit modal to update contact status and detailed interaction notes, saving time and improving data quality.

Team Leads

Team leads focus on high-level oversight and managing the input of new contacts via the "Add Contact" feature.

10. Project Structure

map-fellowship-dashboard/
├── index.html              # Main frontend interface
├── styles.css              # Styling
├── app.js                  # Frontend logic & API calls
├── app.py                  # Python HTTP server
├── sheets_client.py        # Google Sheets API wrapper
├── service_account.json    # Google service account (not in repo)
├── .gitignore              # Git ignore rules
└── demo/                   # Screenshots/demo materials?
└── demo-video.mp4      # Demo video submission



11. Error Handling

I handle errors gracefully at both the front and back end, preventing critical failures and providing clear user feedback:

Client-Side (JavaScript): All fetch calls are wrapped in try...catch. If a network or server error occurs, a user-friendly, non-blocking UI alert is displayed (e.g., "Failed to save update. Check connection.").

Server-Side (Python): Robust try...except blocks surround all external API calls in sheets_client.py. This catches specific Google API errors (like rate limiting or permission issues) and ensures the backend returns correct HTTP status codes (400, 500) instead of crashing.

12. Challenges & Solutions

Challenge 1: How to Hide the Golden Keys (Secure Credential Management)

Problem: I needed to provide the Python app access to the sensitive Service Account credentials during deployment without committing the credentials.json file or exposing secrets in Nginx config.

Solution: I load all sensitive data from environment variables that are securely stored within the Systemd service file (followup.service). The physical credentials.json file is placed outside the web root on the server and its path is referenced only by the Python script, making it non-publicly accessible.

Challenge 2: Making Python Stable (Process Management)

Problem: Running python app.py directly is not stable or reliable enough for production deployment; I needed a robust way to ensure the API stayed running 24/7 and restarted on failure.

Solution: I used Systemd to manage the process. This ensures the application is started on boot, runs continuously, and automatically restarts if the process terminates unexpectedly (Restart=always), guaranteeing the service is always available.

13. Credits

Google Sheets API: Data storage and synchronization powered by Google LLC.

gspread library: Python wrapper for Google Sheets API.

Nginx: Web server and load balancing.

Developer: Mitchell Barure

15. Contact

Developer: Mitchell Barure
Email: m.barure@alustudent.com
Github Repository: https://github.com/MitchellBarure/Follow-Up-Dashboard
Demo Video Link: ?insert demo video url