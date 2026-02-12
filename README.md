# Multimodal Phishing Detection System

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0-green)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.1.3-orange)](https://xgboost.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **production‑ready, multimodal AI system** that detects phishing emails and URLs with **97% accuracy**.  
Combines **URL lexical features (XGBoost)** + **email text (TF‑IDF + XGBoost)** → **stacked ensemble** for robust, real‑time inference.

---

##  **Screenshots & Demo**

| **Model Performance** | **Live API** | **Detection Demo** |
|----------------------|--------------|-------------------|
| ![F1 Score](screenshots/01_model_performance.png) | ![API](screenshots/02_api_running.png) | ![Phishing Alert](screenshots/04_phishing_detected2.png) |

**Feature Importance**  
<img src="screenshots/05_feature_importance.png" alt="Top 20 TF-IDF Features" width="400"/>

---

##  **Key Features**

- ✅ **Multimodal fusion** – URL structure + email text  
- ✅ **XGBoost on 4 lexical features** – `url_count`, `url_length_max`, `url_subdom_max`, `attachment_count`  
- ✅ **TF‑IDF + XGBoost on email body** – captures linguistic phishing cues  
- ✅ **Stacked ensemble (Logistic Regression)** – F1 **0.96–0.97** on test set  
- ✅ **FastAPI backend** – low‑latency predictions  
- ✅ **Streamlit dashboard** – interactive risk gauge, real‑time feedback  
- ✅ **Explainability** – top TF‑IDF feature importance chart  

---

##  **Dataset**

- **MeAJOR Corpus v2.0** (Zenodo) – 108k+ emails, 41 pre‑engineered features, anonymized.  
- 80/10/10 stratified split → 86,947 train / 10,868 val / 10,869 test.

---

## **Model Architecture**
┌─────────────────┐ ┌─────────────────┐
│ URL Features │ │ Email Text │
│ (4 numerical) │ │ (raw string) │
└────────┬────────┘ └────────┬────────┘
│ │
▼ ▼
┌─────────────────┐ ┌─────────────────┐
│ XGBoost (URL) │ │ TF‑IDF + XGB │
│ (trained) │ │ (trained) │
└────────┬────────┘ └────────┬────────┘
│ │
└───────────┬───────────┘
▼
┌─────────────────────┐
│ Meta‑Learner (LR) │
│ probability stack │
└────────┬──────────┘
▼
┌─────────────┐
│ PHISHING / │
│ BENIGN │
└─────────────┘

---

## ⚙️ **Installation & Setup**

### 1️⃣ Clone the repository
