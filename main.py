"""
PROJECT: Advanced GitHub CLI (Assignment Task)
PURPOSE OF THIS CODE: 
To fetch multiple GitHub user profiles at once, handle internet errors by retrying 3 times, 
save any errors in a log file, and finally save a summary of all users in a CSV file.
"""

# 1. IMPORTING LIBRARIES (Bringing in our toolboxes)
import sys      # Used to read multiple usernames from the terminal command
import os       # Used to create folders and read our .env token
import time     # Used to add a delay (pause) between our 3 retries
import csv      # Used to write our data into a .csv (Excel-like) file
import requests # Used to talk to the GitHub API (the internet waiter)
import logging  # Used to write our errors into a file instead of just printing them
from dotenv import load_dotenv

# Load our secret token from the .env file
load_dotenv()

# --- SETTING UP THE ERROR LOGGER ---
# TASK: Log errors to a file instead of only printing them.
# WHY: So developers can look at the 'error.log' file later to see what went wrong.
logging.basicConfig(
    filename='error.log',          # The name of the file where errors will go
    level=logging.ERROR,           # We only want to log ERRORs, not general info
    format='%(asctime)s - %(message)s' # Adds a timestamp (date & time) before each error message
)

def fetch_user_data(username):
    """
    TASK: Get ONE user's data from GitHub.
    WHY A SEPARATE FUNCTION?: Breaking code into small functions makes it easier to test (pytest) later.
    """
    url = f"https://api.github.com/users/{username}"
    token = os.getenv("GITHUB_TOKEN")
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # TASK: Retry a failed request up to 3 times before giving up.
    # WHY: Sometimes the internet drops for a second. We shouldn't fail immediately.
    # HOW: We use a loop that runs exactly 3 times (1, 2, 3).
    for attempt in range(1, 4):
        try:
            print(f"[{attempt}/3] Fetching data for '{username}'...")
            
            # Make the API request. Wait maximum 10 seconds.
            response = requests.get(url, headers=headers, timeout=10)
            
            # If the user doesn't exist (404), it's a permanent error. Do not retry.
            if response.status_code == 404:
                print(f"  -> User '{username}' does not exist.")
                logging.error(f"User '{username}' not found (404).")
                return None # Stop trying and return nothing
            
            # If there's another error (like GitHub server crash), raise an exception to jump to 'except'
            response.raise_for_status()
            
            # If everything was successful, convert data to a Python dictionary and return it
            print(f"  -> Success for '{username}'!")
            return response.json()
            
        except (requests.ConnectionError, requests.Timeout) as e:
            # This handles internet disconnections or timeouts
            print(f"  -> Network error on attempt {attempt}. Retrying in 2 seconds...")
            logging.error(f"Network issue for {username} on attempt {attempt}: {e}")
            time.sleep(2) # Pause the code for 2 seconds before the next try
            
        except Exception as e:
            # This catches any other random crashes
            print(f"  -> An unexpected error occurred for '{username}'.")
            logging.error(f"Unexpected error for {username}: {e}")
            break # Break completely out of the retry loop because it's a fatal error
            
    # If the loop finishes all 3 attempts and still fails, record the final failure
    print(f"  -> Giving up on '{username}' after 3 attempts.")
    logging.error(f"Completely failed to fetch {username} after 3 attempts.")
    return None

def main():
    """
    TASK: The main flow of our CLI tool.
    It reads usernames, fetches their data, and writes a Summary CSV.
    """
    # TASK: Accept several usernames in one run.
    # sys.argv[0] is the file name 'main.py'. 
    # [1:] means "give me a list of everything typed AFTER 'main.py'".
    usernames = sys.argv[1:]
    
    # If the list is empty (user forgot to type names), stop the code.
    if len(usernames) == 0:
        print("Error: Please provide at least one username.")
        print("How to use: python main.py <username1> <username2> <username3>")
        return

    # Create 'output' folder if it does not exist
    os.makedirs("output", exist_ok=True)
    csv_file_path = "output/summary.csv"
    
    # TASK: Write a summary CSV (login, name, public repos, followers)
    # HOW: Open the file in 'w' (write) mode. newline='' prevents empty blank rows.
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        
        # Write the very first row (the column headings)
        writer.writerow(["Login", "Name", "Public Repos", "Followers"])
        
        # Loop through every username the user typed in the terminal
        for username in usernames:
            # Go fetch the data using the function we built above
            user_data = fetch_user_data(username)
            
            # If we successfully got the data (it is not None), save it to the CSV
            if user_data is not None:
                # We use .get() so if a field is missing, it puts a default value instead of crashing
                login = user_data.get("login", "N/A")
                name = user_data.get("name", "N/A")
                repos = user_data.get("public_repos", 0)
                followers = user_data.get("followers", 0)
                
                # Write this user's data as a new row in the CSV
                writer.writerow([login, name, repos, followers])
                
    print(f"\nAll done! Check '{csv_file_path}' for your summary table.")
    print("If any errors occurred, they are saved in 'error.log'.")

# This tells Python to run the main() function when we start the script
if __name__ == "__main__":
    main()