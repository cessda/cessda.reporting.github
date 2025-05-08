# GitHub Issues Report Script

This script fetches issue data from a specified GitHub repository and generates a report summarizing issue activity within a given period.

## Prerequisites

*   Python 3.6 or higher
*   `requests` library (install with `pip install requests`)

## Usage

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a GitHub Personal Access Token:**
    *   Go to your GitHub settings > Developer settings > Personal access tokens > Generate new token.
    *   Give the token a descriptive name (e.g., "Issue Report Script").
    *   Select the `repo` scope (this grants access to the repository's issues).
    *   Generate the token and copy it to your clipboard.

3.  **Create a `token.txt` file:**
    *   In the script's directory, create a file named `token.txt`.
    *   Paste your GitHub Personal Access Token into this file and save it.

4.  **Run the script:**
    ```bash
    python gir.py <path_to_token_file> <owner> <repo> <from_date> <to_date>
    ```
    *   Replace the placeholders with the appropriate values:
        *   `<path_to_token_file>`: The path to your `token.txt` file (e.g., `token.txt`).
        *   `<owner>`: The owner of the GitHub repository (e.g., `cessda`).
        *   `<repo>`: The name of the GitHub repository (e.g., `cessda.metadata.profiles`).
        *   `<from_date>`: The start date for the report period (YYYY-MM-DD).
        *   `<to_date>`: The end date for the report period (YYYY-MM-DD).

    **Example:**
    ```bash
    python gir.py token.txt cessda cessda.metadata.profiles 2024-01-01 2024-12-31
    ```

## Report Output

The script will print a report to the console with the following metrics:

*   Open as of Start Date: Number of issues open on the day before the start date.
*   Created in Period: Number of issues created within the specified period.
*   Closed as Completed: Number of issues closed as completed within the period.
*   Closed as Other: Number of issues closed for other reasons (not\_planned, duplicate, wontfix, invalid) within the period.
*   Open as of End Date: Number of issues open on the end date.
*   Open in Release: Number of open issues associated with a release (milestone).
*   Open in Backlog: Number of open issues not associated with a release (no milestone).

## Setting up a Virtual Environment (Recommended)

It's recommended to use a virtual environment to manage project dependencies.

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    ```
2.  **Activate the virtual environment:**
    *   macOS/Linux: `source .venv/bin/activate`
    *   Windows: `.venv\Scripts\activate`
3.  **Install required packages:** `pip install requests`


## License

This project is licensed under the CC0 1.0 Universal License. See the `LICENSE` file for details.