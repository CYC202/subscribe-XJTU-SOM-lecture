import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from datetime import datetime
import os
from flask import request


class LectureMonitor:
    def __init__(self, url, email_credentials_file, to_emails_file, storage_file):
        self.url = url
        self.email_address, self.email_password = self.load_email_credentials(email_credentials_file)
        self.to_emails = set(self.load_emails(to_emails_file))
        self.storage_file = storage_file
        self.sent_lectures = self.load_sent_lectures()
        self.recent_lectures = []  # Store recent lectures here

    def subscribe(self, new_email):
        """
        Subscribe a new email address.
        """
        if new_email not in self.to_emails:
            self.to_emails.add(new_email)  # Use set add to ensure uniqueness
            self.save_emails()
            return f"{new_email} has been successfully subscribed."
        else:
            return f"{new_email} is already in the subscription list."

    def unsubscribe(self, email_to_remove):
        """
        Unsubscribe an email address.
        """
        if email_to_remove in self.to_emails:
            self.to_emails.remove(email_to_remove)
            self.save_emails()
            return f"{email_to_remove} has been successfully unsubscribed."
        else:
            return f"{email_to_remove} was not found in the subscription list."

    def save_emails(self):
        """
        Save the subscription email list to a file.
        """
        try:
            with open('to_emails.txt', 'w') as file:
                file.writelines(f"{email}\n" for email in self.to_emails)
        except Exception as e:
            print(f"Error saving emails: {e}")

    def load_email_credentials(self, credentials_file):
        try:
            with open(credentials_file, 'r') as file:
                lines = file.readlines()
                return lines[0].strip(), lines[1].strip()
        except Exception as e:
            print(f"Error loading email credentials: {e}")
            return None, None

    def load_emails(self, emails_file):
        try:
            with open(emails_file, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Error loading emails: {e}")
            return []

    def load_sent_lectures(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as file:
                    return set(tuple(line.strip().split('|')) for line in file if line.strip())
            except Exception as e:
                print(f"Error loading sent lectures: {e}")
                return set()
        return set()

    def save_sent_lectures(self):
        """
        Save sent lectures to the storage file.
        """
        try:
            with open(self.storage_file, 'w') as file:
                file.writelines(f"{title}|{date}\n" for title, date in self.sent_lectures)
        except Exception as e:
            print(f"Error saving sent lectures: {e}")

    def get_page_content(self):
        """
        Fetch lecture information from the provided URL.
        """
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

            self.recent_lectures = result  # Store fetched lectures
            return pd.DataFrame(result)
        except requests.RequestException as e:
            print(f"Error fetching page content: {e}")
            return pd.DataFrame()

    def get_poster(self, url):
        """
        Fetch the poster image URL from the given lecture page.
        """
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

    def send_email(self, update_content):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_address
        msg['To'] = ", ".join(self.to_emails)
        msg['Subject'] = f"{datetime.now().strftime('%m月%d日')} 更新讲座"

        base_url = f"{request.scheme}://{request.host}"

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

            /* 响应式样式 */
            @media screen and (max-width: 600px) {
                .container {
                    padding: 15px;
                }
                h2 {
                    font-size: 20px;
                }
                .lecture {
                    padding: 10px;
                }
                h3 {
                    font-size: 18px;
                }
            }

            /* 特殊中文字体样式 */
            .chinese {
                font-family: 'Microsoft YaHei', '微软雅黑', sans-serif;
            }
            
            .unsubscribe {
                text-align: center;
                font-size: 10px;  /* 小号字体 */
                color: #888;
                margin-top: 20px;
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

        # Add recent lectures section
        recent_lectures_html = self.get_recent_lectures_html()
        html_content += f"""
            <h3>Recent Lectures</h3>
            <ul>
                {recent_lectures_html}
            </ul>
        """

        # # Convert to_emails to a list to get the first email for the unsubscribe link
        # email_list = list(self.to_emails)
        # unsubscribe_link = f'<a href="{base_url}/unsubscribe/{email_list[0]}">Unsubscribe</a>'
        # html_content += f"""
        #     <div class="unsubscribe">
        #         {unsubscribe_link}
        #     </div>
        #     </div>
        # </body>
        # </html>
        # """

        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        try:
            with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, self.to_emails, msg.as_string())
            print("邮件发送成功。")
        except smtplib.SMTPException as e:
            print(f"发送邮件时出错: {e}")


    def get_recent_lectures_html(self):
        # Get the last 5 lectures based on the order they were fetched
        recent_lectures = self.recent_lectures[1:6]  # Get the last 5 items
        return ''.join(f"<li><a href='{lecture['link']}'>{lecture['title']}</a></li>" for lecture in recent_lectures)

    def monitor(self):
        """
        Monitor the webpage for new lectures and send email notifications for new updates.
        """
        content = self.get_page_content()
        if content.empty:
            print("No content fetched.")
            return

        content['poster'] = content['link'].apply(self.get_poster)
        today = datetime.now().strftime('%Y-%m-%d')

        # Filter out today's new lectures that have not been sent
        new_content = content[content['date'].str.contains(today) & ~content.apply(lambda row: (row['title'], row['date']) in self.sent_lectures, axis=1)]

        if not new_content.empty:
            latest_content = new_content.head(1)
            self.send_email(latest_content)
            self.sent_lectures.update((row['title'], row['date']) for _, row in latest_content.iterrows())
            self.save_sent_lectures()


# Ensure all outputs are in English
# Use this script to monitor lectures, subscribe/unsubscribe users, etc.
