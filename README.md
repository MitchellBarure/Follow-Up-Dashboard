Ministry Follow-Up Dashboard

A small full-stack application that helps a ministry or fellowship team manage follow-up for attendees and contacts.

Instead of manually scrolling through Google Sheets, this dashboard:
- Reads records from a shared Google Sheet using the **Google Sheets API**
- Shows them in a web UI with **search** and **filters**
- Lets team members update **status + notes**
- Lets the team lead create **new records**
- Writes all changes back to the same Google Sheet

TABLE OF CONTENTS
Overview
Features
Tech Stack
Architecture
Prerequisites
Installation & Setup
--Local Development
Google Sheets API Setup
Deployment
Server Setup (Web01 & Web02)
Load Balancer Configuration
API Documentation
Usage
Project Structure
Challenges & Solutions
Credits
License

OVERVIEW
**?what does the application do and target audience
This is a custom web application that uses Google Sheets as a data store via API. The dashboard provides filtering, workflow enforcement, status controls, statistics, and team coordination features that Google Sheets alone cannot provide.
Live Demo: **?insert url

FEATURES
Real-time google sheets integration
Advanced filtering (by category, status and search by name/phone number)
Team Dashboard 
Status management (allows updates on status & notes)
Live updates (chnages instantly show in google sheets)
Load balanced (deployed across two servers for reliability)
Responsive design

TECH STACK
Frontend: Vanilla HTML, CSS & Js
Backend: Python, http.server(standard library), Google sheets API v4
Data store: Google sheet (acts like a simple shared database)
Infrastructure: Nginx , load balancer and ubuntu servers (web01, web02 & LB-01)

ARCHITECTURE
1. User access **?insert url
2. Load balancer routes traffic to Web01 oe wEB02
3. Nginx serves statis files
4. API requests proxied to python backend on port 8000
5. Backend reads/writes to google sheets via the API
6. Updates reflected in real time

PREREQUISITES
Python 3.8+, Google Cloud platform account, Ubuntu servers, domain name, basic knowledge on ssh, nginx configuration and google cloud console

INSTALLATION & SETUP
For local deployment:
1. Clone & Enter the repo using git clone and cd.
2. Set up & Activate Python Virtual Environment (Use python3 -m venv venv & source venv/bin/activate)
3. Install dependencies (pip install -r requirements.txt)
4. Configure the environment (create .env file/export variables)
5. Run the backedn (python app.py)
6. Open the frontend (python -m http://localhost:3000)
You can now visit http://localhost:3000 **?

GOOGLE SHEETS API SETUP:
1. Create a google cloud project
2. Create a service account
3. Set up a google sheet
4. Configure the credentials/ json key

DEPLOYMENT
1. ssh into each server
2. install dependencies (update system, install python, pip, nginx and git)
3. Clone and set up the application 
4. Configure nginx (sudo nano /etc/nginx/sites-available/repository_name)
5. Enable the site
6. Run Python backend as a service
7. Start service
8. Test the individual servers
9. Configure your load balancer

API DOCUMENTATION
Base URL:
 - Local: http://localhost:8000
 - Production: http://map.yourdomain.tech
Endpoints:
1. GET /api/contacts
 - Retrieve all contacts from Google Sheets.
 
2. PUT /api/contacts/:id
 - Update contact status and notes.

3. Status Values:

 - NOT_CONTACTED
 - CONTACTED
 - COMING
 - NOT_COMING
 - MAYBE

USAGE **?
Team Members
Team Leads
Filtering & Searching

PROJECT STRUCTURE
map-fellowship-dashboard/
├── index.html              # Main frontend interface
├── styles.css              # Styling
├── app.js                  # Frontend logic & API calls
├── app.py                  # Python HTTP server
├── sheets_client.py        # Google Sheets API wrapper
├── requirements.txt        # Python dependencies **?
├── credentials.json        # Google service account (not in repo)
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── demo/                  # Screenshots/demo materials
└── demo-video.mp4

ERROR HANDLING**?

CHALLENGES & SOLUTIONS: **?
Challenge 1: [INSERT TITLE]
Problem:
Solution:

CREDITS
Google Sheets API - Data storage and synchronization powered by Google LLC
gspread library - Python wrapper for Google Sheets API
Nginx - Web server and load balancing
Mitchell Barure - Developer

LICENSE **?

CONTACT 
Developer: Mitchell Barure
Email: m.barure@alustudent.com
Github **?
Demo Video: **?