# Server Health Check
A simple Python tool to monitor the health of a remote Linux server over SSH.
The tool performs common system health checks such as disk usage, memory usage, CPU usage, service status, port availability, and load average. It also generates a log file and transfers it to the remote server using SCP.

## Features
* SSH connectivity check
* Disk usage check
* Memory usage check
* CPU usage check
* Top CPU processes
* Service status check
* Port check
* Load average check
* Run all health checks
* Log generation and SCP file transfer

## Project Structure
server-health-check/
* main.py
* monitoring.py
* config.py
* README.md

## Sample Menu
1. Disk Usage Check
2. Memory Usage Check
3. CPU Usage Check
4. Top CPU Processes
5. Service Status Check
6. Port Check
7. Load Average Check
8. Run Full Health Check
9. Exit

