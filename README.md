# 🚀 RepoRadar: Advanced GitHub Profile CLI

## 📖 The Journey (From Origin to End)
This project started as a simple classwork task: Build a basic Python tool to fetch just **one** GitHub user's profile and save it as a JSON file. 

But then we upgraded it into an **Advanced CLI Tool** for our final assignment! We gave it superpowers to:
1. Fetch **multiple usernames** at the exact same time.
2. **Retry 3 times** automatically if the internet drops (so it doesn't crash immediately).
3. Save any unexpected errors securely into a separate **error log** file.
4. Organize all the fetched data into a neat **CSV (Excel-like)** summary table.
5. Check its own code using automated **Pytest**.

---

## 📁 What is inside each file? (File Breakdown)
If you are new to this project, here is a simple explanation of what every single file does:

* **`main.py` (The Brain 🧠):** 
  This is the main engine. It reads the names you type in the terminal, goes to the GitHub API, handles the 3x retries if the internet is slow, and writes the final data into a CSV file.

* **`test_main.py` (The Auto-Checker 🤖):** 
  Instead of a human manually checking if the code works, this file uses a tool called `pytest`. It runs fake and real usernames through our code to automatically verify that everything is perfectly working.

* **`requirements.txt` (The Shopping List 🛒):** 
  It contains the list of all external Python libraries our project needs (`requests`, `python-dotenv`, `pytest`). By running one command, Python reads this file and installs everything.

* **`.env` (The Secret Locker 🔒):** 
  This file keeps our `GITHUB_TOKEN` secret. GitHub allows 60 free searches per hour, but with this token, we get 5,000 searches. We keep it here so it stays safe on our computer.

* **`.gitignore` (The Security Guard 🛡️):** 
  Before we upload our code to GitHub, this file tells Git: *"Hey, do NOT upload the secret `.env` file, and do NOT upload the heavy `venv` folder!"* It keeps our GitHub repository clean and secure.

* **`error.log` (The Diary of Mistakes 📓):** 
  If you search for a user that doesn't exist (404 error) or your WiFi turns off, the script writes the exact time and reason for the failure in this text file instead of throwing ugly red errors on the screen.

* **`output/summary.csv` (The Final Result 📊):** 
  Once the data is successfully fetched, it is organized here in a beautiful table structure with columns for Login, Name, Public Repos, and Followers.

---

## 🛠️ Step-by-Step Setup Guide
Want to run this on your own computer? Follow these easy steps:

**Step 1: Create a safe space (Virtual Environment)**
`python -m venv venv`

**Step 2: Turn it on**
# On Windows:
`.\venv\Scripts\Activate.ps1`

**Step 3: Buy the groceries (Install required libraries)**
`pip install -r requirements.txt`

**Step 4: Set up your keys**
Create a `.env` file in the folder and put your GitHub token inside: `GITHUB_TOKEN=your_token_here`

---

## 💻 How to use the Tool?
Open your terminal and type `python main.py` followed by any GitHub usernames you want to search. For example:

`python main.py octocat khanwarda thisuserisfake123`

**What will happen?**
1. It will successfully fetch `octocat` and `khanwarda`.
2. It will realize `thisuserisfake123` does not exist and quietly write that error in `error.log`.
3. Finally, it will create a `summary.csv` in the `output` folder with the data of the successful users!

To run the automated tests, simply type:
`pytest -v -s`