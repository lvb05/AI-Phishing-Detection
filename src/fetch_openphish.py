
#!/usr/bin/env python3
import argparse
import requests
import pandas as pd
import os

OPENPHISH_FEED = 'https://openphish.com/feed.txt'

def fetch_feed(out_csv, source=None):
    urls = []
    if source:
        # read from local file
        with open(source, 'r') as f:
            for line in f:
                url = line.strip()
                if url:
                    urls.append(url)
    else:
        try:
            r = requests.get(OPENPHISH_FEED, timeout=15)
            r.raise_for_status()
            for line in r.text.splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
        except Exception as e:
            print('Warning: failed to fetch feed:', e)
    df = pd.DataFrame({'url': urls, 'label': ['phishing'] * len(urls)})
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f'Saved {len(df)} feed URLs to {out_csv}')

def main():
    parser = argparse.ArgumentParser(description='Fetch OpenPhish feed to CSV.')
    parser.add_argument('--out', default='../data/openphish.csv', help='Output CSV path')
    parser.add_argument('--source', help='Local source file (optional)')
    args = parser.parse_args()
    fetch_feed(args.out, source=args.source)

if __name__ == '__main__':
    main()
