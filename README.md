# AI-Powered Phishing Detection and Mitigation System

An end-to-end **AI-driven Phishing Detection System** that detects and mitigates phishing threats using **BERT/RoBERTa**, **XGBoost**, and **CNN models**.  
It integrates **AES-256 encryption**, **OpenPhish threat intelligence**, and a **real-time Streamlit dashboard** for visualization — all containerized via **Docker**.

---

## 🚀 Features

- 🤖 **Intelligent Detection:** Hybrid engine combining NLP (BERT) + ML (XGBoost)
- 📬 **Email & URL Analysis:** Classifies spear-phishing emails and malicious URLs
- 🔐 **Data Security:** AES-256 encryption and anonymization
- 🌐 **Threat Intelligence:** Automated feed updates from OpenPhish APIs
- 📊 **Real-Time Dashboard:** Streamlit-powered visualization for analysts
- 🐳 **Containerized:** Fully Dockerized for scalable deployment

---

## 📂 Project Structure
```
AI-Phishing-Detection/
│
├── data/
│ ├── emails.csv
│ ├── phishing_urls.csv
│
├── notebooks/
│ ├── phishing_detection_bert.ipynb
│ ├── phishing_detection_xgboost.ipynb
│
├── src/
│ ├── model_train.py
│ ├── model_predict.py
│ ├── encrypt_data.py
│ ├── fetch_openphish.py
│
├── dashboard/
│ ├── app.py
│
├── docker/
│ ├── Dockerfile
│ ├── requirements.txt
│
├── README.md
```


---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/AI-Phishing-Detection.git
cd AI-Phishing-Detection
```

### 2️⃣ Set Up the Environment
```bash
pip install -r docker/requirements.txt
```

### 3️⃣ Train the Models
```bash
python src/model_train.py
```
### 4️⃣ Launch the Dashboard
```bash
cd dashboard
streamlit run app.py
```
---

### Docker Deployment
- Build Docker Image
```bash
cd docker
docker build -t ai-phishing-detection .
```

-Run the Container
```bash
docker run -p 8501:8501 ai-phishing-detection
```
-Visit 👉 http://localhost:8501 to access the dashboard.


### OpenPhish Integration

The app automatically fetches the latest phishing URLs via the OpenPhish feed. You can also manually run:
```bash
python src/fetch_openphish.py
```
### Data Security

Sensitive email data is encrypted using AES-256-GCM via:
```bash
python src/encrypt_data.py
```
---
Model Performance
```
| Model   | Dataset | Precision | Recall | F1-score |
| ------- | ------- | --------- | ------ | -------- |
| BERT    | Emails  | 94.3%     | 90.5%  | 92.2%    |
| XGBoost | URLs    | 95.1%     | 91.8%  | 93.4%    |

```
