
#!/usr/bin/env python3
\"\"\"model_train.py

Train models for the AI-Phishing-Detection project.

- Email classifier: TF-IDF + Logistic Regression (fast baseline). Optionally export TF-IDF vectorizer.
- URL classifier: Feature-engineered XGBoost classifier.
- Saves models to ../models/ (creates folder if missing).

Usage:
    python src/model_train.py --emails ../data/emails.csv --urls ../data/phishing_urls.csv
\"\"\"

import argparse
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier

def train_email_model(emails_csv, out_dir):
    df = pd.read_csv(emails_csv)
    df = df.dropna(subset=['body','label'])
    X = df['body'].astype(str)
    y = df['label'].map({'legitimate':0, 'phishing':1})
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1,2))
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_tfidf, y_train)
    preds = clf.predict(X_test_tfidf)

    print(\"--- Email model evaluation ---\")
    print(classification_report(y_test, preds, target_names=['legitimate','phishing']))
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(clf, os.path.join(out_dir, 'email_tfidf_logreg.pkl'))
    joblib.dump(tfidf, os.path.join(out_dir, 'email_tfidf_vectorizer.pkl'))
    print(f\"Saved email model and vectorizer to {out_dir}\")


def extract_url_features(series):
    rows = []
    for url in series.astype(str):
        rows.append({
            'url_length': len(url),
            'num_digits': sum(c.isdigit() for c in url),
            'num_specials': sum(not c.isalnum() for c in url),
            'has_https': int(url.startswith('https')),
            'num_subdomains': url.count('.')-1,  # approximate
            'contains_at': int('@' in url),
            'contains_ip': int(any(ch.isdigit() for ch in url.split('//')[-1].split('/')[0]) and ('.' in url.split('//')[-1].split('/')[0]))
        })
    return pd.DataFrame(rows)


def train_url_model(urls_csv, out_dir):
    df = pd.read_csv(urls_csv)
    df = df.dropna(subset=['url','label'])
    X = extract_url_features(df['url'])
    y = df['label'].map({'legitimate':0, 'phishing':1})
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=100)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print(\"--- URL model evaluation ---\")
    print(classification_report(y_test, preds, target_names=['legitimate','phishing']))

    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(model, os.path.join(out_dir, 'xgboost_url_model.pkl'))
    print(f\"Saved URL model to {out_dir}\")


def main():
    parser = argparse.ArgumentParser(description='Train phishing detection models.')
    parser.add_argument('--emails', default='../data/emails.csv', help='Path to emails.csv')
    parser.add_argument('--urls', default='../data/phishing_urls.csv', help='Path to phishing_urls.csv')
    parser.add_argument('--out', default='../models', help='Output folder for saved models')
    args = parser.parse_args()

    print('Training email model...')
    train_email_model(args.emails, args.out)
    print('\\nTraining URL model...')
    train_url_model(args.urls, args.out)
    print('\\nAll models trained and saved.')

if __name__ == '__main__':
    main()
