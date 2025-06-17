import streamlit as st
import threading
import time
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    while True:
        log_lines = []
        now_str = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

        try:
            with open('weblist.txt', 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
                for url in urls:
                    try:
                        driver.get(url)
                        log_line = f"{now_str} ✅ {url} → 200"
                    except WebDriverException as e:
                        log_line = f"{now_str} ❌ {url} → Error: {e}"
                    print(log_line)
                    log_lines.append(log_line)
        except FileNotFoundError:
            log_lines.append(f"{now_str} ❌ weblist.txt not found.")

        if log_lines:
            with open(LOG_FILE, "a", encoding='utf-8') as f:
                for line in log_lines:
                    f.write(line + "\n")

        time.sleep(2700)

# Start background thread only once
if not hasattr(st, "_wake_thread_started"):
    threading.Thread(target=wake_web, daemon=True).start()
    st._wake_thread_started = True

# Auto-refresh every 1s
st_autorefresh(interval=30000, key="refresh")

# Virtual time display
elapsed_real = (datetime.now() - REAL_SERVER_START).total_seconds()
current_virtual = VIRTUAL_START + timedelta(seconds=elapsed_real)

st.title("Wake Web Streamlit")
st.write("### Time running since:")
st.code(current_virtual.strftime("%Y-%m-%d %H:%M:%S"))

# Load last 100 log lines from file
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding='utf-8') as f:
        lines = f.readlines()
        last_lines = lines[-100:]
        st.write("### Request Log")
        st.markdown(
            f"""
            <style>
                .log-box::-webkit-scrollbar {{
                    width: 10px;
                }}
                .log-box::-webkit-scrollbar-track {{
                    background: #eee;
                    border-radius: 5px;
                }}
                .log-box::-webkit-scrollbar-thumb {{
                    background: #888;
                    border-radius: 5px;
                }}
                .log-box::-webkit-scrollbar-thumb:hover {{
                    background: #555;
                }}
                .log-box {{
                    scrollbar-color: #888 #eee;
                    scrollbar-width: thin;
                }}
            </style>
            <div class="log-box" style="
                background-color:#f9f9f9;
                color:#000;
                padding:10px;
                border-radius:5px;
                border:1px solid #ccc;
                height:400px;
                overflow:auto;
                font-family: monospace;
                white-space: pre-wrap;
                width: 100%;">
                {"<br>".join(line.strip() for line in last_lines)}
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.write("### Request Log")
    st.info("No logs yet.")
