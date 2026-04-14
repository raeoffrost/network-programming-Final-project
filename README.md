# Micro HTTP Server

## Overview
This project is a simple HTTP/1.1 server built using Python sockets. It demonstrates how a basic web server works by handling requests and responses manually without using any frameworks.

## Features
- TCP socket server
- Parses HTTP GET requests
- Serves local HTML files
- Returns 404 Not Found for missing files

## Requirements
- Python 3 installed

## Setup and Run
1. Open the project folder in a terminal
2. Run the server:

  `py micro_http_server.py`

3. Open a browser and go to:

  `http://localhost:8080/`

## Testing
- `/` → loads `index.html` (must exist in the same folder)
- `/filename.html` → loads that file if it exists
- `/does-not-exist` → returns a 404 page 

### Notes
- The server only handles basic GET requests
- All files must be in the same directory as the server script
