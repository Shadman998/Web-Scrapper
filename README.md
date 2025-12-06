🕷️ Quotes Web Scraper & Dashboard

A robust Python web scraping application built to extract, clean, and analyze quotes from quotes.toscrape.com.

This project goes beyond a simple script by integrating a Streamlit user interface, allowing non-technical users to scrape data and download clean CSV datasets without touching a single line of code.

🚀 Features

Interactive UI: Built with Streamlit to replace command-line arguments with a friendly dashboard.

Dynamic Scraping: Users can specify exactly how many pages to scrape via a slider.

Data Cleaning Pipeline:

Removes "Smart Quotes" (curly quotes) and other non-standard characters using Regex.

Handles UTF-8 encoding to prevent "Mojibake" (garbled text) in Excel.

Robust Error Handling: Includes try-except blocks to handle network timeouts or missing HTML elements gracefully.

One-Click Export: Generates an Excel-ready CSV file instantly.

🛠️ Tech Stack

Python 3.10+

BeautifulSoup4: For parsing HTML and navigating the DOM tree.

Requests: For handling HTTP sessions and headers (User-Agent spoofing).

Pandas: For structuring data and handling CSV exports.

Streamlit: For the frontend web interface.

⚙️ Installation & Usage

Clone the repository:

git clone [https://github.com/shadman998/web-scraper.git]
cd web-scraper-app


Install dependencies:

pip install -r requirements.txt


Run the application:

streamlit run app.py


Open your browser:
The app should automatically open at http://localhost:8501.

📂 Project Structure

├── scrapper.py         # Main application logic (Streamlit + Scraping)
├── requirements.txt    # List of dependencies
├── .gitignore          # Files to exclude from Git (pycache, etc.)
└── README.md           # Project documentation


🧠 What I Learned

Building this project helped solidify core Data Engineering concepts:

DOM Traversal: Understanding how to navigate HTML trees to extract specific data points.

Request Headers: How to mimic browser behavior to avoid 403 Forbidden errors.

Data Serialization: The importance of utf-8-sig when working with Excel-compatible CSVs.

Deployment: Hosting a Python app on the web using Streamlit Cloud.

Built by Shadman as part of the journey to becoming a Top 1% ML Engineer. 🚀