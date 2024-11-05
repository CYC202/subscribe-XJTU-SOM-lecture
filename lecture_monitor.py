import os
import sqlite3
from threading import Thread
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import base64
import time

class LectureMonitor:
    def __init__(self, url, email_address, email_password, db_file):
        self.url = url
        self.email_address = email_address
        self.email_password = email_password
        self.db_file = db_file
        self.sent_lectures = set()
        self.recent_lectures = []

    def subscribe(self, email):
        # Subscribe a new email
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscribers WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return f"{email} has already subscribed."
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        return f"{email} has been successfully subscribed."

    def unsubscribe(self, email):
        # Unsubscribe an email
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscribers WHERE email = ?", (email,))
        if not cursor.fetchone():
            conn.close()
            return f"{email} was not found in the subscription list."
        cursor.execute("DELETE FROM subscribers WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return f"{email} has been successfully unsubscribed."

    def get_subscribers(self):
        # Get all subscribers
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM subscribers")
        emails = [row[0] for row in cursor.fetchall()]
        conn.close()
        return emails

    def save_sent_lecture(self, title, date):
        # Save sent lecture information
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO sent_lectures (title, date) VALUES (?, ?)", (title, date))
        conn.commit()
        conn.close()

    def has_sent_lecture(self, title, date):
        # Check if lecture has already been sent
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sent_lectures WHERE title = ? AND date = ?", (title, date))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def get_page_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            list_items = soup.find_all('li', attrs={'data-aos': 'fade-up'})

            result = []
            for item in list_items:
                a_tag = item.find('a')
                if a_tag:
                    title = a_tag.find('h3').get_text(strip=True)
                    link = a_tag['href']
                    date = a_tag.find('span').get_text(strip=True)
                    full_link = f"https://som.xjtu.edu.cn/{link[3:]}"
                    result.append({'title': title, 'link': full_link, 'date': date})

            self.recent_lectures = result
            return pd.DataFrame(result)
        except requests.RequestException as e:
            # print(f"Error fetching page content: {e}")
            return pd.DataFrame()

    def get_poster(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tag = soup.find('img', class_='img_vsb_content')
            if img_tag:
                img_src = img_tag.get('src')
                return f"https://som.xjtu.edu.cn/{img_src}"
        except requests.RequestException as e:
            print(f"Error fetching poster: {e}")
        return None

    def get_recent_lectures_html(self):
        # Get the last 5 lectures based on the order they were fetched
        recent_lectures = self.recent_lectures[-5:]
        return ''.join(f"<li><a href='{lecture['link']}'>{lecture['title']}</a></li>" for lecture in recent_lectures)

    def send_email(self, update_content):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_address
        msg['To'] = ", ".join(self.get_subscribers())
        msg['Subject'] = f"{datetime.now().strftime('%m月%d日')} 更新讲座"

        html_content = """
        <html>
        <head>
        <style>
            body {
                font-family: 'Times New Roman', serif;
                background-color: #f9f9f9;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            h2 {
                color: #004080;
                text-align: center;
                border-bottom: 2px solid #004080;
                padding-bottom: 10px;
            }
            h3 {
                color: #333;
                margin-top: 30px;
            }
            .lecture {
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f4f4f4;
            }
            .lecture img {
                max-width: 100%;
                height: auto;
                margin-top: 10px;
                border-radius: 5px;
            }
            a {
                color: #004080;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            ul {
                padding-left: 20px;
            }
        </style>
        </head>
        <body>
            <div class="container">
                <h2 class="chinese">Academic Lecture Update</h2>
        """

        for _, row in update_content.iterrows():
            html_content += f"""
            <div class="lecture">
                <p class="chinese"><strong>Lecture Title: </strong> {row['title']}</p>
                <p class="chinese"><strong>Details: </strong> <a href="{row['link']}">{row['link']}</a></p>
                <p class="chinese"><strong>Notification Date: </strong> {row['date']}</p>
            """
            if row.get('poster'):
                image_data = requests.get(row['poster']).content
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                html_content += f'<img src="data:image/jpeg;base64,{image_base64}">'
            html_content += "</div>"

        # Add recent lectures section (moved outside of the loop)
        recent_lectures_html = self.get_recent_lectures_html()
        html_content += f"""
            <h3>Recent Lectures</h3>
            <ul>
                {recent_lectures_html}
            </ul>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        try:
            with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, self.get_subscribers(), msg.as_string())
        except smtplib.SMTPException as e:
            print(f"发送邮件时出错: {e}")

    def monitor(self):
        content = self.get_page_content()
        if content.empty:
            # print("No content fetched.")
            return

        content['poster'] = content['link'].apply(self.get_poster)
        # yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') # for testing
        today = datetime.now().strftime('%Y-%m-%d')
        new_content = content[content['date'].str.contains(today) & ~content.apply(lambda row: self.has_sent_lecture(row['title'], row['date']), axis=1)]

        if not new_content.empty:
            latest_content = new_content.head(1)
            self.send_email(latest_content)
            for _, row in latest_content.iterrows():
                self.save_sent_lecture(row['title'], row['date'])

    def start_monitoring(self, interval=3600):
        def run_monitor():
            time.sleep(6000) # Delay start by 100 minutes
            while True:
                self.monitor()
                time.sleep(interval)

        thread = Thread(target=run_monitor)
        thread.daemon = True
        thread.start()
