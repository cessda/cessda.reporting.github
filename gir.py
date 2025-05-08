import requests
import sys
import argparse
from datetime import datetime, timezone

# GitHub repo info
OWNER = "cessda"
REPO = "cessda.metadata.profiles"
BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

def parse_github_datetime(dt_str):
    """Parses GitHub timestamps like '2024-12-31T12:34:56Z' as aware UTC datetime."""
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

def fetch_issues(token, owner, repo):
    issues = []
    page = 1    
    headers = {"Authorization": f"token {token}"}
    base_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    while True:
        params = {
            "state": "all",
            "per_page": 100,
            "page": page,
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching issues:", response.text)
            sys.exit(1)

        data = response.json()
        if not data:
            break

        # Filter out pull requests
        issues.extend([issue for issue in data if 'pull_request' not in issue])
        page += 1
    return issues

def filter_issues_by_creation_date(issues, from_date, to_date):
    filtered_issues = []
    for issue in issues:
        created_at = parse_github_datetime(issue['created_at'])
        if from_date <= created_at <= to_date:
            filtered_issues.append(issue)
    return filtered_issues

def generate_report(issues, from_date, to_date):
    created_in_period = 0
    closed_completed = 0
    closed_other = 0
    open_as_of_end = 0
    open_as_of_start = 0
    open_in_release = 0
    open_in_backlog = 0

    for issue in issues:
        created_at = parse_github_datetime(issue['created_at'])
        closed_at = parse_github_datetime(issue['closed_at']) if issue.get('closed_at') else None
        state = issue['state']
        closed_reason = issue.get('closed_reason')
        labels = [label['name'] for label in issue.get('labels', [])]
        milestone = issue.get('milestone')

        # 1. Created in period
        if from_date <= created_at <= to_date:
            print(f"Issue (ID: {issue['number']}) created at: {created_at}, included in period.")
            created_in_period += 1

        # 2. Closed as completed
        if closed_at:
            print(f"Issue (ID: {issue['number']}) closed at: {closed_at}, closed reason: {closed_reason or 'None'}")
            if from_date <= closed_at <= to_date:
                if closed_reason is None or closed_reason == "completed":
                    closed_completed += 1
                elif closed_reason == "not_planned":
                    closed_other += 1
            else:
                print(f"Issue (ID: {issue['number']}) closed outside the period.")

        # 3. Open as of start date
        if created_at <= from_date and (state == "open" or (closed_at and closed_at >= from_date)):
            open_as_of_start += 1

        # 4. Open as of end date
        if created_at <= to_date and (state == "open" or (closed_at and closed_at > to_date)):
            open_as_of_end += 1

        # 5. Open in release
        if state == "open" and milestone:
            open_in_release += 1

        # 6. Open in backlog
        if state == "open" and not milestone:
            open_in_backlog += 1
        
        
        # Check for "other" labels if not already counted as completed or not_planned
        other_labels = ["duplicate", "wontfix", "invalid"]
        if closed_at and from_date <= closed_at <= to_date and (closed_reason == "not_planned" or any(label in other_labels for label in labels)):            
            closed_other += 1
    return {
        "Open as of Start Date": open_as_of_start,
        "Created in Period": created_in_period,
        "Closed as Completed": closed_completed,
        "Closed as Other": closed_other,
        "Open as of End Date": open_as_of_end,
        "Open in Release": open_in_release,
        "Open in Backlog": open_in_backlog
    }

def main():
    parser = argparse.ArgumentParser(description="GitHub Issue Report")
    parser.add_argument("token_file", help="Path to file containing GitHub token")
    parser.add_argument("owner", help="Repository owner (e.g., 'cessda')")
    parser.add_argument("repo", help="Repository name (e.g., 'cessda.metadata.profiles')")
    parser.add_argument("from_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("to_date", help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    # Read token from file
    with open(args.token_file, 'r') as f:
        token = f.read().strip()

    from_dt = datetime.fromisoformat(args.from_date).replace(tzinfo=timezone.utc)
    to_dt = datetime.fromisoformat(args.to_date).replace(tzinfo=timezone.utc)

    print("Fetching issues from GitHub...")
    issues = fetch_issues(token, args.owner, args.repo)

    report = generate_report(issues, from_dt, to_dt)

    print("\n📊 Report:")
    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
