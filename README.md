# subscribe-XJTU-SOM-lecture

The **subscribe-XJTU-SOM-lecture** project aims to keep users informed about the latest lectures from the School of Management at Xi'an Jiaotong University (XJTU). Since lecture updates are only posted on the official university website, many users often miss important announcements. This application captures the latest lecture announcements every hour, ensuring that users never miss out on significant events.

Utilizing the Flask framework, the project creates an API that manages subscription and unsubscription requests. Subscribers will receive emails containing the lecture title, notification date, a poster, and an option to unsubscribe.

## Key Features:
- **Real-time Updates**: Receives and notifies users of new lectures every hour.
- **Email Notifications**: Delivers detailed lecture information directly to subscribers' inboxes.
- **Subscription Management**: Easily subscribe or unsubscribe from notifications with just a few clicks.
- **Monitoring**: Tracks and logs sent lectures to prevent duplicate notifications.

---

**subscribe-XJTU-SOM-lecture** 旨在帮助大家及时获取西交管理学院最新讲座信息。由于讲座更新仅在官方网站上发布，难以跟踪。该程序每小时监测讲座公告，确保大家及时收到重要活动的更新。

该项目使用 Flask 框架创建了一个 API，处理订阅和退订请求。订阅者将收到包含讲座题目、公告时间、海报和退订选项的电子邮件。

## 主要功能：
- **实时更新**：每小时获取并通知用户最新的讲座信息。
- **邮件通知**：将讲座详情直接发送到订阅者的邮箱。
- **订阅管理**：用户可以轻松地订阅或退订。
- **监测功能**：跟踪和记录已发送的讲座信息，以避免重复通知。

![image](https://github.com/user-attachments/assets/c92a7dd2-15b9-4fa0-aefe-fafae2279235)

> **Note**: You can subscribe to lecture updates by entering `http://104.214.172.60:5008/subscribe/your_email@example.com` in your browser.
>
> For example, you can use `http://104.214.172.60:5008/subscribe/johndoe@example.com`.
> 
> To unsubscribe, simply enter `http://104.214.172.60:5008/unsubscribe/your_email@example.com`, such as `http://104.214.172.60:5008/unsubscribe/johndoe@example.com`.
> 
> This is a personal server, provided free of charge.

> **注**：您可以通过在浏览器中输入 `http://104.214.172.60:5008/subscribe/你的邮箱@example.com` 来订阅讲座更新，例如 `http://104.214.172.60:5008/subscribe/johndoe@example.com`。
> 
> 若要退订，只需输入 `http://104.214.172.60:5008/unsubscribe/你的邮箱@example.com`，例如 `http://104.214.172.60:5008/unsubscribe/johndoe@example.com`。
> 
> 这是个人服务器，免费提供给大家使用。

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
