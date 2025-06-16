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
    url=r'https://visitcount-ymbj8jwzkdo4rdnrnspkqm.streamlit.app/'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    st.write(f"DEBUG:DRIVER:{driver}")
    driver.get(url)
    time.sleep(5)
    html_doc = driver.page_source
    driver.quit()
wake_web()
