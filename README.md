Ministry Follow-Up Dashboard: Rescuing Follow-Up from Google Sheet Hell

This application is a custom web solution built to rescue ministry teams from the pain of Google Sheet overload. By leveraging the Google Sheets API v4, I created a dashboard that enforces workflow, provides status controls, and streamlines team coordination—all things a static spreadsheet cannot handle alone. This delivers genuine, practical value to the end-users.

Target Audience: Ministry, church, or fellowship teams responsible for managing outreach or attendee follow-up pipelines.

Live Demo: https://youtu.be/5eRUDqzzBrY?si=l_KeoriVxF555C5b

# TABLE OF CONTENTS

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

# 1. Overview
A small, full-stack application designed to modernize and streamline the crucial contact follow-up process for ministry or fellowship teams.

I built this app to replace manual, error-prone scrolling through sprawling Google Sheets. This dashboard provides a focused, real-time workflow interface that just works:

It reads records from a shared Google Sheet using the Google Sheets API (treating it like a live, dynamic data store).

PresentS the data in a responsive web UI with advanced search and filters that actually save time.

Allows team members to efficiently update a contact's status and notes without ever opening the spreadsheet.

Enables the team lead to create new records directly via the UI.

Writes all changes back to the same Google Sheet instantly, maintaining a single source of truth for the whole team.

# 2. Features

Real-time Google Sheets Integration: Instant data exchange with the external API ensures the dashboard and the Sheet are always in sync.

Advanced Data Interaction: Filter by status or category, and search by name or phone number—making data actionable instead of overwhelming.

Status Management: Clear, enforced workflow states for tracking progress (NOT_CONTACTED, COMING, etc.).

Load Balanced: Deployed across two separate servers (Web01, Web02) for high availability, meaning the application is reliable and always accessible.

Responsive Design: Fully usable on desktop, tablet, and mobile devices for updates on-the-go.

# 3. Tech Stack

Frontend: Vanilla HTML, CSS, & JavaScript (keeping the client lightweight and fast).

Backend: Python, http.server (standard library module), Google Sheets API v4.

Key Python Dependencies: google-api-python-client, gspread, oauth2client (for secure API communication).

Data Store: A designated Google Sheet (simple, shared data persistence).

Infrastructure: Nginx web server, Systemd (for service management), Load Balancer (LB-01), and two Ubuntu web servers (Web01, Web02).

# 4. Architecture

The application is deployed using a robust, highly available three-tier architecture. This implementation is crucial for stability and ensuring continuous service.

On Each Web Server (Web01, Web02):

Nginx (Port 80): Acts as the entry point. It serves the static frontend files (index.html, styles.css, app.js) directly for maximum speed.

Reverse Proxy (Port 8000): Nginx proxies all dynamic API requests (/api/) directly to the Python server running on port 8000.

Python Backend (app.py): The standard Python server runs continuously on port 8000, processes the request, and handles all external communication with the Google Sheets API.

Systemd: Manages and monitors the Python server process, ensuring the API is always running and automatically restarted if it fails.

Load Balancing (LB-01):
The dedicated Load Balancer uses Nginx's upstream module with a Round Robin algorithm to distribute incoming user traffic evenly to Web01 and Web02. Since the application is stateless (all data is externalized to the Sheets API), this provides seamless redundancy.

# 5. Prerequisites

Python 3.8+

Google Cloud Platform (GCP) Account with Google Sheets API enabled.

Admin access (via SSH) to three Ubuntu servers (Web01, Web02, LB-01).

A domain name configured to point to the Load Balancer's public IP.

# 6. Installation & Setup

## Local Development

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


## Google Sheets API Setup

- Create a Google Cloud Project and enable the Google Sheets API.

- Create a Service Account and download the JSON key file (credentials.json).

- Set up a Google Sheet with the required headers.

- Configure the credentials: Share the Google Sheet (Editor access) with the Service Account's email address (found in your JSON key file).


# Local Setup & Deployment Instructions

## 🚀 LOCAL SETUP

### Step 1: Clone Repository
```bash
git clone https://github.com/MitchellBarure/Follow-Up-Dashboard.git
cd Follow-Up-Dashboard
```

### Step 2: Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Add Credentials
Place your `credentials.json` file in the project root (get this from Google Cloud Console).

### Step 4: Configure Sheet ID
Edit `sheets_client.py` and add your Google Sheet ID:
```python
SHEET_ID = "your_sheet_id_here"
```

### Step 5: Run Backend
```bash
python app.py
```
Server starts on `http://localhost:8000`

### Step 6: Open Frontend
Open `index.html` directly in your browser, or serve it:
```bash
python -m http.server 3000
# Then visit http://localhost:3000
```

---

## 🌐 DEPLOYMENT TO WEB SERVERS

### Deploy to Web-01 and Web-02 (Do for BOTH servers)

#### Step 1: Connect via SSH
```bash
# For Web-01
ssh -i ~/.ssh/my_key ubuntu@54.211.70.81

# For Web-02
ssh -i ~/.ssh/my_key ubuntu@44.201.147.220
```

#### Step 2: Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git nginx
```

#### Step 3: Clone Repository
```bash
cd /var/www
sudo git clone https://github.com/MitchellBarure/Follow-Up-Dashboard.git map-dashboard
sudo chown -R ubuntu:ubuntu /var/www/map-dashboard
cd map-dashboard
```

#### Step 4: Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 5: Upload Credentials
From your **local machine**, run:
```bash
# For Web-01
scp -i ~/.ssh/my_key credentials.json ubuntu@54.211.70.81:/var/www/map-dashboard/

# For Web-02
scp -i ~/.ssh/my_key credentials.json ubuntu@44.201.147.220:/var/www/map-dashboard/
```

#### Step 6: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/map-dashboard
```

**Paste this configuration:**
```nginx
server {
    listen 80;
    server_name _;
    
    location / {
        root /var/www/map-dashboard;
        index index.html;
        try_files $uri $uri/ =404;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        add_header X-Served-By "web-01" always;
    }
}
```
**Note:** Change `"web-01"` to `"web-02"` on the second server

**Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/map-dashboard /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 7: Create Systemd Service
```bash
sudo nano /etc/systemd/system/map-dashboard.service
```

**Paste:**
```ini
[Unit]
Description=MAP Dashboard API Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/map-dashboard
Environment="PATH=/var/www/map-dashboard/venv/bin"
ExecStart=/var/www/map-dashboard/venv/bin/python app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start map-dashboard
sudo systemctl enable map-dashboard
sudo systemctl status map-dashboard
```

#### Step 8: Test Individual Server
From your **local machine**:
```bash
# Test Web-01
curl http://54.211.70.81/api/contacts

# Test Web-02
curl http://44.201.147.220/api/contacts

# Or open in browser:
# http://54.211.70.81
# http://44.201.147.220
```

---

## ⚖️ LOAD BALANCER CONFIGURATION

### Step 1: Connect to Load Balancer
```bash
ssh -i ~/.ssh/my_key ubuntu@3.87.53.138
```

### Step 2: Install Nginx
```bash
sudo apt update
sudo apt install -y nginx
```

### Step 3: Configure Load Balancer
```bash
sudo nano /etc/nginx/sites-available/map-lb
```

**Paste this configuration:**
```nginx
upstream backend {
    server 54.211.70.81:80;
    server 44.201.147.220:80;
}

server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable configuration:**
```bash
sudo ln -s /etc/nginx/sites-available/map-lb /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: Test Load Balancing
From your **local machine**:
```bash
# Run multiple times - should alternate between web-01 and web-02
for i in {1..10}; do
  curl -s -I http://3.87.53.138/api/contacts | grep X-Served-By
done
```

**Expected output:**
```
X-Served-By: web-01
X-Served-By: web-02
X-Served-By: web-01
X-Served-By: web-02
...
```

**Or test in browser:**
- Visit `http://3.87.53.138`
- Open DevTools → Network tab → Refresh page
- Check Response Headers for `X-Served-By`
- Refresh multiple times - should alternate between `web-01` and `web-02`

---

### Verification Checklist

- [ ] Local setup works: `http://localhost:3000`
- [ ] Web-01 works: `http://54.211.70.81`
- [ ] Web-02 works: `http://44.201.147.220`
- [ ] Load balancer works: `http://3.87.53.138`
- [ ] Load balancer alternates between servers (check `X-Served-By` header)
- [ ] Can load contacts from Google Sheets
- [ ] Can update contact status and notes
- [ ] Changes save to Google Sheets in real-time

## B. Load Balancer Configuration (LB-01)

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

# 8. API Documentation

Google Sheets API (Overview)
https://developers.google.com/sheets/api

Google Sheets API – REST reference
https://developers.google.com/sheets/api/reference/rest

Python Google API Client Library
https://github.com/googleapis/google-api-python-client

Using service accounts (Google Cloud)
https://cloud.google.com/iam/docs/service-accounts


### Base URL:

Local: http://localhost:8000

Production: http://3.87.53.138 (The application is accessed via the load balancer’s public IP address)

### Endpoints:

GET /api/contacts: I retrieve all contacts from Google Sheets.

PUT /api/contacts/:id: I update contact status and notes based on the contact's unique row index (:id).

POST /api/contacts: I create a new contact record.

### Status Values:

NOT_CONTACTED

CONTACTED

COMING

NOT_COMING

MAYBE

# 9. Usage

Team Members
- Team members primarily focus on filtering the dataset and using the Edit modal to update contact status and detailed interaction notes, saving time and improving data quality.

Team Leads
- Team leads focus on high-level oversight and managing the input of new contacts via the "Add Contact" feature.

# 10. Project Structure

Follow-Up-Dashboard/
├── index.html              # Main frontend interface
├── styles.css              # Styling
├── app.js                  # Frontend logic & API calls
├── app.py                  # Python HTTP server
├── sheets_client.py        # Google Sheets API wrapper
├── service_account.json    # Google service account (not in repo)
├── .gitignore              # Git ignore rules
└── images                  # Screenshots of UI


# 11. Error Handling

I handle errors gracefully at both the front and back end, preventing critical failures and providing clear user feedback:

Client-Side (JavaScript): All fetch calls are wrapped in try...catch. If a network or server error occurs, a user-friendly, non-blocking UI alert is displayed (e.g., "Failed to save update. Check connection.").

Server-Side (Python): Robust try...except blocks surround all external API calls in sheets_client.py. This catches specific Google API errors (like rate limiting or permission issues) and ensures the backend returns correct HTTP status codes (400, 500) instead of crashing.

# 12. Challenges & Solutions

Challenge 1: How to Hide the Golden Keys (Secure Credential Management)

Problem: 
I needed to provide the Python app access to the sensitive Service Account credentials during deployment without committing the credentials.json file or exposing secrets in Nginx config.
Solution:
I load all sensitive data from environment variables that are securely stored within the Systemd service file (followup.service). The physical credentials.json file is placed outside the web root on the server and its path is referenced only by the Python script, making it non-publicly accessible.

Challenge 2: Frontend Filtering Broke Due to Inconsistent Data

Problem:
Some fields from Google Sheets returned empty or inconsistent values, causing search + filters to fail or show “No records found.”
Solution:
Implemented a normalizeValue() helper and added defensive checks (record.Status || ""). This made filtering stable regardless of data quality.

Challenge 3: Keeping the Python Backend Running Reliably

Problem:
Running python app.py manually is unstable and doesn’t restart on crash or boot.
Solution:
Created a systemd service to run the API continuously, restart on failure, and start automatically on boot.

Challenge 4: NGINX Returned 404 for CSS/JS Files
Problem:
Frontend HTML loaded, but static files (CSS/JS) returned 404 via NGINX.
Solution:
Fixed the root directory in /etc/nginx/sites-available/default and restarted NGINX. Static assets then loaded correctly on both servers.

Challenge 5: Google Sheets API Worked on One Server but Not the Other
Problem:
Backend failed on one server because service_account.json was missing or in the wrong directory.
Solution:
Uploaded the credentials to both servers, set correct paths and permissions, and verified Google Sheets API access on each machine.

Challenge 6: Browser Blocked API Calls (CORS Error)

Problem:
Frontend couldn’t call the Python API due to missing CORS headers.
Solution:
Added:
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS
Access-Control-Allow-Headers: Content-Type
to the Python server, fixing CORS issues.

Challenge 7: Load Balancer Not Distributing Traffic at First

Problem:
Requests always hit the same backend server, making it unclear if load balancing worked.
Solution:
Monitored access logs on both servers while refreshing the load balancer URL. This confirmed round-robin distribution and validated the NGINX config.


# 13. Credits

Google Sheets API: Data storage and synchronization powered by Google LLC.

gspread library: Python wrapper for Google Sheets API.

Nginx: Web server and load balancing.

Developer: Mitchell Barure

# 15. Contact

Developer: Mitchell Barure
Email: m.barure@alustudent.com
Github Repository: https://github.com/MitchellBarure/Follow-Up-Dashboard
Demo Video Link: https://youtu.be/5eRUDqzzBrY?si=l_KeoriVxF555C5b
