
import argparse
import joblib
import os
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

def predict_email(text):
    vec_path = os.path.join(MODEL_DIR, 'email_tfidf_vectorizer.pkl')
    clf_path = os.path.join(MODEL_DIR, 'email_tfidf_logreg.pkl')
    if not os.path.exists(vec_path) or not os.path.exists(clf_path):
        raise FileNotFoundError('Email model or vectorizer not found. Run src/model_train.py first.')
    vectorizer = joblib.load(vec_path)
    clf = joblib.load(clf_path)
    X = vectorizer.transform([text])
    pred = clf.predict(X)[0]
    return {0: 'legitimate', 1: 'phishing'}[int(pred)]

def extract_url_features_single(url):
    return {
        'url_length': len(url),
        'num_digits': sum(c.isdigit() for c in url),
        'num_specials': sum(not c.isalnum() for c in url),
        'has_https': int(url.startswith('https')),
        'num_subdomains': url.count('.')-1,
        'contains_at': int('@' in url),
        'contains_ip': int(any(ch.isdigit() for ch in url.split('//')[-1].split('/')[0]) and ('.' in url.split('//')[-1].split('/')[0]))
    }

def predict_url(url):
    clf_path = os.path.join(MODEL_DIR, 'xgboost_url_model.pkl')
    if not os.path.exists(clf_path):
        raise FileNotFoundError('URL model not found. Run src/model_train.py first.')
    model = joblib.load(clf_path)
    feats = extract_url_features_single(url)
    X = pd.DataFrame([feats])
    pred = model.predict(X)[0]
    return {0: 'legitimate', 1: 'phishing'}[int(pred)]

def main():
    parser = argparse.ArgumentParser(description='Make a prediction using trained models.')
    parser.add_argument('--email', type=str, help='Email body text to classify')
    parser.add_argument('--url', type=str, help='URL to classify')
    args = parser.parse_args()

    if args.email:
        print('Email prediction:', predict_email(args.email))
    if args.url:
        print('URL prediction:', predict_url(args.url))

if __name__ == '__main__':
    main()
