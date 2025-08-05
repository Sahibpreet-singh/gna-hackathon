# Intelligent Firewall Log Analyzer 🔥

A smart, ML-assisted firewall logging system built with **Node.js**, **Python**, and **MongoDB**. It allows real-time monitoring of traffic, automatic prediction of malicious activity, and customizable firewall policies.

---

## 🚀 Features

- 🔍 **Real-time Traffic Analysis**  
  Automatically analyze incoming traffic data and predict whether to allow or block it using a Python-based ML model.

- 📊 **Dashboard Rendering**  
  Displays recent traffic logs in a clean EJS-powered dashboard.

- 🤖 **ML Integration (Python)**  
  Predicts whether a traffic packet is suspicious using `predict.py` and logs the decision.

- 🔐 **Dynamic Firewall Policies**  
  Get and update policies like blocked IPs, domains, and protocols.

- 🧾 **MongoDB Logging**  
  All traffic decisions and logs are stored in a MongoDB database.

---

## 🛠️ Tech Stack

- **Backend**: Node.js, Express.js  
- **Database**: MongoDB, Mongoose  
- **Python Integration**: `PythonShell` to run ML script  
- **Templating**: EJS  
- **Others**: CORS, JSON API, RESTful architecture

---

| Method | Route        | Description                            |
| ------ | ------------ | -------------------------------------- |
| POST   | `/predict`   | Predict traffic as allow/block via ML  |
| POST   | `/log`       | Log custom traffic manually            |
| GET    | `/logs`      | Get last 50 logs                       |
| GET    | `/policies`  | Fetch current firewall policies        |
| POST   | `/policies`  | Update firewall policies               |
| GET    | `/dashboard` | View logs in EJS-rendered UI dashboard |



🔮 Prediction Logic
The ML model (inside predict.py) takes the following inputs:

Packet Size

Request Frequency

Port

It returns:

"1" → suspicious → block

"0" → normal → allow


👤 Author
Made with 💻 by @Sahibpreet-singh for GNA Hackathon 2025.

