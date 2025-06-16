import streamlit as st
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

LOG_FILE = "visitor_logs.txt"

# --- Visit a URL with Playwright ---
def visit_with_playwright(url):
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=15000)
            page_title = page.title()
            browser.close()
        log = f"{now} ✅ {url} → Loaded '{page_title}'"
    except Exception as e:
        log = f"{now} ❌ {url} → Error: {e}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log + "\n")
    return log

# --- Streamlit UI ---
st.title("🧭 Playwright Visitor Bot")

urls_input = st.text_area("Enter one URL per line:", placeholder="https://example.com")
if st.button("Visit URLs"):
    urls = [u.strip() for u in urls_input.splitlines() if u.strip()]
    st.write(f"🌐 Visiting {len(urls)} site(s) using Playwright...")
    logs = [visit_with_playwright(url) for url in urls]
    st.success("✅ All done!")
    for log in logs:
        st.write(log)

# --- Log viewer ---
st.write("### 📜 Visit Log")
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()[-100:]
        st.markdown(
            f"""
            <div style='
                height: 300px; overflow-y: auto; 
                background: #f9f9f9; padding: 10px; 
                border: 1px solid #ccc; border-radius: 6px;
                font-family: monospace; white-space: pre-wrap;
                color: #000;'>
            {"<br>".join(line.strip() for line in lines)}
            </div>
            """, unsafe_allow_html=True
        )
else:
    st.info("No logs yet.")
