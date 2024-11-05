# 📢 XJTU SOM Lecture Notifier 2.0
Never miss another interesting lecture! This enhanced tool helps you stay updated with the latest academic lectures from the School of Management at Xi'an Jiaotong University (XJTU).

## 🆕 What's New!
- 💾 **Persistent Storage**: Now using SQLite database for reliable subscriber management and lecture tracking
- 🔒 **Email Validation**: Enhanced email validation for more secure subscription handling
- 🎯 **Smart Monitoring**: Improved lecture detection
- 🖼️ **Rich Email Content**: 
  - Beautiful HTML email template with consistent styling
  - Embedded lecture posters directly in emails
  - Recent lectures section showing the last 5 lectures
- 🛡️ **Error Handling**: Robust error handling for network issues and invalid requests
- 🔄 **Flexible API**: Support for both GET and POST requests in subscribe/unsubscribe endpoints

## ✨ Core Features
- 🔄 **Intelligent Auto-Updates**: 
  - Checks for new lectures every hour
- 📧 **Enhanced Email Notifications**: 
  - Professional HTML email template
  - Lecture title and details
  - Direct link to lecture page
  - Embedded event poster
  - List of recent lectures
  - Clean, responsive design
- 🎯 **Advanced Tracking**: 
  - SQLite database for reliable tracking
  - No duplicate notifications
  - Precise date-based filtering

## 🛠 Technical Stack
- **Backend**: Flask with SQLite
- **Web Scraping**: BeautifulSoup4 and Requests
- **Email**: SMTP with MIME support
- **Data Processing**: Pandas for efficient data handling
- **Database**: SQLite3 for persistent storage
- **Threading**: Background monitoring with daemon threads

## 🚀 How to Use
It's super simple! Just pop these URLs in your browser:

To Subscribe:
```
http://104.214.172.60:5008/subscribe/your_email@example.com
```
To Unsubscribe:
```
http://104.214.172.60:5008/unsubscribe/your_email@example.com
```

For example:
- Subscribe: `http://104.214.172.60:5008/subscribe/johndoe@example.com`
- Unsubscribe: `http://104.214.172.60:5008/unsubscribe/johndoe@example.com`

> ✈️ This service runs on a personal server and is completely free to use!

## 🏠 Local Development
1. Clone the repository:
```bash
git clone https://github.com/CYC202/subscribe-XJTU-SOM-lecture.git
```

2. Set up the environment variables:
```bash
export URL="your_target_url"
export EMAIL_ADDRESS="your_email"
export EMAIL_PASSWORD="your_email_password"
export PASSWORD="your_admin_password"
```

3. Initialize the database:
```bash
python init_db.py
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python app.py
```

### 📬 Email Example
<img src="./images/example.png" width="600" alt="Email Notification Example">

---

# 西交管理学院讲座订阅助手 2.0 
再也不用担心错过精彩讲座啦！这个升级版小工具会帮你实时追踪西安交通大学管理学院的最新学术讲座信息。

## 🆕 最新更新！
- 💾 **持久化存储**: 使用SQLite数据库实现可靠的订阅管理和讲座追踪
- 🔒 **邮箱验证**: 增强的邮箱验证功能，提供更安全的订阅处理
- 🎯 **智能监控**: 改进的讲座检测系统
- 🖼️ **丰富邮件内容**: 
  - 精美的HTML邮件模板，统一的样式设计
  - 讲座海报直接嵌入邮件
  - 最近讲座栏目展示最新5场讲座
- 🛡️ **错误处理**: 完善的网络问题和无效请求处理机制
- 🔄 **灵活API**: 支持GET和POST两种请求方式的订阅/退订接口

## 🎯 功能特色
- 🔄 **智能自动更新**: 
  - 每小时检查最新讲座信息
- 📧 **增强邮件通知**: 
  - 专业的HTML邮件模板
  - 讲座标题和详情
  - 讲座页面直接链接
  - 内嵌活动海报
  - 最近讲座列表
  - 清晰响应式设计
- 🎯 **高级追踪**: 
  - 使用SQLite数据库可靠追踪
  - 避免重复通知
  - 精确的日期过滤

## 🚀 使用方法
超级简单！在浏览器输入以下地址即可：

订阅：
```
http://104.214.172.60:5008/subscribe/你的邮箱@example.com
```
退订：
```
http://104.214.172.60:5008/unsubscribe/你的邮箱@example.com
```

示例：
- 订阅：`http://104.214.172.60:5008/subscribe/johndoe@example.com`
- 退订：`http://104.214.172.60:5008/unsubscribe/johndoe@example.com`

> ✈️ 这是个人服务器，完全免费提供给大家使用！

## 🏠 本地运行
1. 克隆仓库：
```bash
git clone https://github.com/CYC202/subscribe-XJTU-SOM-lecture.git
```

2. 配置环境变量：
```bash
export URL="your_target_url"
export EMAIL_ADDRESS="your_email"
export EMAIL_PASSWORD="your_email_password"
export PASSWORD="your_admin_password"
```

3. 初始化数据库：
```bash
python init_db.py
```

4. 安装依赖：
```bash
pip install -r requirements.txt
```

5. 运行应用：
```bash
python app.py
```

### 📬 邮件示例
<img src="./images/example.png" width="600" alt="邮件通知示例">

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
