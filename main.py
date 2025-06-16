import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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

        try:
            with open('weblist.txt', 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
                for url in urls:
                    try:
                        driver.get(url)
                        log_line = f" ✅ {url} → 200"
                    except:
                        log_line = f" ❌ {url} → Error"
                    print(log_line)
                    log_lines.append(log_line)
        except FileNotFoundError:
            log_lines.append(f" ❌ weblist.txt not found.")
wake_web()
