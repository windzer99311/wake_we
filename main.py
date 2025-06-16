import streamlit as st
import threading
import time
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Constants
VIRTUAL_START_STR = "2025-06-13 00:00:00"
VIRTUAL_START = datetime.strptime(VIRTUAL_START_STR, "%Y-%m-%d %H:%M:%S")
BOOT_TIME_FILE = "boot_time.txt"
LOG_FILE = "logs.txt"

# Set or load the real boot time
if os.path.exists(BOOT_TIME_FILE):
    with open(BOOT_TIME_FILE, "r", encoding='utf-8') as f:
        REAL_SERVER_START = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S")
else:
    REAL_SERVER_START = datetime.now()
    with open(BOOT_TIME_FILE, "w", encoding='utf-8') as f:
        f.write(REAL_SERVER_START.strftime("%Y-%m-%d %H:%M:%S"))

# ✅ Wake web background task using Selenium with proper log format
def wake_web():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    st.write(f"DEBUG:DRIVER:{driver}")
    while True:
        time.sleep(30)
        log_lines = []
        now_str = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

        try:
            with open('weblist.txt', 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
                for url in urls:
                    try:
                        driver.get(url)
                        log_line = f"{now_str} ✅ {url} → 200"
                    except:
                        log_line = f"{now_str} ❌ {url} → Error"
                    print(log_line)
                    log_lines.append(log_line)
        except FileNotFoundError:
            log_lines.append(f"{now_str} ❌ weblist.txt not found.")
wake_web()
