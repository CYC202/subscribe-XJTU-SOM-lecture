# 📢 XJTU SOM Lecture Notifier

Never miss another interesting lecture! This neat little tool helps you stay updated with the latest academic lectures from the School of Management at Xi'an Jiaotong University (XJTU).

## 🤔 Why This Tool?

Ever missed an exciting lecture because you forgot to check the university website? We've all been there! That's exactly why this project exists. Instead of constantly checking the website, let the notifications come to you!

## ✨ What It Does

- 🔄 **Auto-Updates**: Checks for new lectures every hour
- 📧 **Email Notifications**: Get all the juicy details right in your inbox
  - Lecture title
  - Date and time
  - Event poster
  - Easy unsubscribe option
- 🎯 **Smart Tracking**: No duplicate notifications - we keep track of what we've sent!

## 🛠 Tech Behind It

Built with Flask because, well, sometimes simple is better! The API handles all the subscribe/unsubscribe magic, making sure your email preferences are taken care of.

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

> 💝 This service runs on a personal server and is completely free to use!

---

# 西交管理学院讲座订阅助手 

再也不用担心错过精彩讲座啦！这个小工具会帮你实时追踪西安交通大学管理学院的最新学术讲座信息。

## 🤔 为什么需要这个工具？

是不是经常因为忘记查看学院网站而错过感兴趣的讲座？这个项目就是为解决这个问题而生的。不用再时刻盯着网站，让通知来找你！

## ✨ 功能特色

- 🔄 **自动更新**：每小时检查最新讲座信息
- 📧 **邮件通知**：重要信息直达邮箱
  - 讲座标题
  - 时间日期
  - 活动海报
  - 一键退订选项
- 🎯 **智能追踪**：不会重复发送已通知的讲座

## 🛠 技术实现

使用 Flask 框架搭建，简单可靠！API 轻松处理订阅/退订请求，妥善管理您的邮件偏好。

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

> 💝 这是个人服务器，完全免费提供给大家使用！

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
