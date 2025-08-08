#!/usr/bin/env python3
"""
Weekly Project Agent - simplified.

This script automatically creates and publishes full-stack side projects on a weekly schedule.
Each project has a date, name, theme, and description. On the scheduled date, the script creates a new repository on GitHub, generates template files (Flask backend and simple HTML frontend), and commits them.

Set the environment variables GITHUB_TOKEN and GITHUB_USERNAME before running.
"""

import os
import base64
import datetime
import time
import requests
import schedule
from dataclasses import dataclass
from typing import List

@dataclass
class Project:
    name: str
    description: str
    start_date: datetime.date
    theme: str

# Define the project schedule - update dates as needed
PROJECTS: List[Project] = [
    Project(name="expense-tracking-budgeting-app", description="A web app to track income and expenses, categorise transactions, and visualise monthly budgets.", start_date=datetime.date(2025,8,11), theme="Finance"),
    Project(name="cryptocurrency-portfolio-tracker", description="Track crypto asset performance; input holdings and view price history and portfolio value.", start_date=datetime.date(2025,8,18), theme="Finance"),
    Project(name="stock-portfolio-management", description="Manage a virtual stock portfolio: add tickers, see current prices and compute gains/losses.", start_date=datetime.date(2025,8,25), theme="Finance"),
    Project(name="peer-to-peer-payment-service", description="Simulate a simple peer-to-peer payment system for sending and receiving virtual currency and viewing balances and history.", start_date=datetime.date(2025,9,1), theme="Finance"),
    Project(name="loan-and-mortgage-calculator", description="Compute monthly payments and amortisation schedules for loans and mortgages.", start_date=datetime.date(2025,9,8), theme="Finance"),
    Project(name="invoice-and-billing-system", description="Generate invoices, track due dates, record payments and provide an admin dashboard.", start_date=datetime.date(2025,9,15), theme="Finance"),
    Project(name="investment-portfolio-analyzer", description="Upload investment holdings to analyse allocations by asset class, geography and sector with charts.", start_date=datetime.date(2025,9,22), theme="Finance"),
    Project(name="personal-finance-dashboard", description="Unified dashboard summarising budget, savings and investments; pulls data from other finance apps.", start_date=datetime.date(2025,9,29), theme="Finance"),
    Project(name="automated-savings-planner", description="Help users set savings goals and allocate income to different goals with projections and reminders.", start_date=datetime.date(2025,10,6), theme="Finance"),
    Project(name="race-results-dashboard", description="Display race results from the OpenF1 API; show finishing order, time gaps and fastest laps.", start_date=datetime.date(2025,10,13), theme="Formula1"),
    Project(name="lap-telemetry-visualizer", description="Visualise lap-by-lap telemetry for a driver using OpenF1 API: speed, throttle, brake.", start_date=datetime.date(2025,10,20), theme="Formula1"),
    Project(name="driver-performance-comparison", description="Compare two drivers across races and seasons with metrics like points scored, qualifying vs race pace and consistency.", start_date=datetime.date(2025,10,27), theme="Formula1"),
    Project(name="real-time-race-tracker", description="Dashboard polling OpenF1 API for live lap data, positions, gaps and sector times.", start_date=datetime.date(2025,11,3), theme="Formula1"),
    Project(name="pit-strategy-analyzer", description="Analyse pit stop timing for a race and suggest alternative strategies using historical data.", start_date=datetime.date(2025,11,10), theme="Formula1"),
    Project(name="simple-race-prediction-model", description="Train a simple machine learning model to predict finishing positions based on qualifying and past performance.", start_date=datetime.date(2025,11,17), theme="Formula1"),
    Project(name="load-balancer-demo", description="Implement a basic HTTP reverse proxy that distributes requests across multiple backend servers, demonstrating round-robin and health checks.", start_date=datetime.date(2025,11,24), theme="SystemDesign"),
    Project(name="in-memory-message-queue", description="Build a simple publish-subscribe message queue with topics, producers and consumers and HTTP APIs.", start_date=datetime.date(2025,12,1), theme="SystemDesign"),
    Project(name="distributed-cache-simulator", description="Simulate a distributed key-value cache with multiple nodes and consistent hashing; provide HTTP interface.", start_date=datetime.date(2025,12,8), theme="SystemDesign"),
    Project(name="url-shortener-service", description="Create a URL shortening service that generates short links and collects basic analytics.", start_date=datetime.date(2025,12,15), theme="SystemDesign"),
    Project(name="social-media-feed-backend", description="Implement backend for a social media feed with posts, following relationships and a timeline.", start_date=datetime.date(2025,12,22), theme="SystemDesign"),
    Project(name="distributed-file-storage", description="Design a simple distributed file storage system that splits files across nodes and allows download via an API.", start_date=datetime.date(2025,12,29), theme="SystemDesign"),
]

def github_api_headers(token: str):
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

def create_repo(token: str, name: str, description: str):
    url = "https://api.github.com/user/repos"
    payload = {"name": name, "description": description, "private": False, "auto_init": False}
    r = requests.post(url, headers=github_api_headers(token), json=payload)
    r.raise_for_status()
    return r.json()

def push_file(token: str, owner: str, repo: str, path: str, content: str, message: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    b64 = base64.b64encode(content.encode()).decode()
    payload = {"message": message, "content": b64, "branch": "main"}
    r = requests.put(url, headers=github_api_headers(token), json=payload)
    r.raise_for_status()

def generate_files(project: Project):
    files = {}
    pretty_name = project.name.replace("-", " ").title()
    files["README.md"] = f"# {pretty_name}\n\n{project.description}\n"
    files["backend/app.py"] = (
        "from flask import Flask, jsonify\n"
        "app = Flask(__name__)\n\n"
        "@app.route('/api/hello')\n"
        "def hello():\n"
        "    return jsonify({'message': 'Hello from " + project.name + "'})\n\n"
        "if __name__ == '__main__':\n"
        "    app.run(debug=True, host='0.0.0.0', port=5000)\n"
    )
    files["backend/requirements.txt"] = "flask\n"
    files["frontend/index.html"] = (
        "<!DOCTYPE html>\n"
        "<html lang='en'>\n"
        "<head><meta charset='UTF-8'><title>" + pretty_name + "</title></head>\n"
        "<body>\n"
        "<h1>" + pretty_name + "</h1>\n"
        "<p id='message'>Loading...</p>\n"
        "<script>\n"
        "fetch('/api/hello').then(res=>res.json()).then(data=>{document.getElementById('message').innerText=data.message;});\n"
        "</script>\n"
        "</body>\n"
        "</html>\n"
    )
    return files

def repository_exists(token: str, owner: str, name: str) -> bool:
    url = f"https://api.github.com/repos/{owner}/{name}"
    r = requests.get(url, headers=github_api_headers(token))
    return r.status_code == 200

def publish_project(project: Project):
    token = os.environ["GITHUB_TOKEN"]
    owner = os.environ["GITHUB_USERNAME"]
    if repository_exists(token, owner, project.name):
        print(f"Repository {project.name} already exists.")
        return
    print(f"Creating repository {project.name}")
    create_repo(token, project.name, project.description)
    files = generate_files(project)
    for path, content in files.items():
        print(f"Adding {path} to {project.name}")
        push_file(token, owner, project.name, path, content, f"Add {path}")

def check_schedule():
    today = datetime.date.today()
    for project in PROJECTS:
        if project.start_date <= today:
            publish_project(project)

def main():
    check_schedule()
    schedule.every().day.at('10:00').do(check_schedule)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()
