# weekly-project-agent

This repository contains `weekly_project_agent.py` – a script that automatically generates and publishes a full‑stack side project every week until 31 December 2025.  The projects rotate through Finance & FinTech, Formula 1 analytics and System Design themes.  Each generated project includes a minimal Flask backend and a simple HTML frontend, and the script uses the GitHub API to create a new repository for each entry in the schedule.

## Usage

Install the dependencies:

```sh
pip install -r weekly_project_agent/requirements.txt
```

Export a personal access token to authorize GitHub API calls:

```sh
export GITHUB_TOKEN=ghp_yourSecretTokenHere
```

Run the agent:

```sh
python weekly_project_agent/weekly_project_agent.py
```

To automate weekly runs, schedule the script via cron or a similar scheduler.

## Project schedule

| Week | Date (2025) | Theme | Project |
|----:|:-----------:|:-----:|:------------------------------------------------------------|
| 1   | Aug 11      | Finance     | Expense Tracking and Budgeting App |
| 2   | Aug 18      | Finance     | Cryptocurrency Portfolio Tracker |
| 3   | Aug 25      | Finance     | Stock Portfolio Management |
| 4   | Sept 1      | Finance     | Peer‑to‑Peer Payment Service |
| 5   | Sept 8      | Finance     | Loan and Mortgage Calculator |
| 6   | Sept 15     | Finance     | Invoice and Billing System |
| 7   | Sept 22     | Finance     | Investment Portfolio Analyzer |
| 8   | Sept 29     | Finance     | Personal Finance Dashboard |
| 9   | Oct 6       | Finance     | Automated Savings Planner |
| 10  | Oct 13      | Formula 1   | Race Results Dashboard |
| 11  | Oct 20      | Formula 1   | Lap Telemetry Visualizer |
| 12  | Oct 27      | Formula 1   | Driver Performance Comparison |
| 13  | Nov 3       | Formula 1   | Real‑Time Race Tracker |
| 14  | Nov 10      | Formula 1   | Pit Strategy Analyzer |
| 15  | Nov 17      | Formula 1   | Simple Race Prediction Model |
| 16  | Nov 24      | System Design | Load Balancer Demo |
| 17  | Dec 1       | System Design | In‑Memory Message Queue |
| 18  | Dec 8       | System Design | Distributed Cache Simulator |
| 19  | Dec 15      | System Design | URL Shortener Service |
| 20  | Dec 22      | System Design | Social Media Feed Backend |
| 21  | Dec 29      | System Design | Distributed File Storage |
