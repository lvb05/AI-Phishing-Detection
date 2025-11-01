
#!/usr/bin/env python3
\"\"\"encrypt_data.py

Simple AES-256-GCM encryption/decryption utilities for protecting email data.
Requires: cryptography

Usage examples:
    python src/encrypt_data.py --encrypt --infile ../data/emails.csv --outfile ../data/emails.enc
    python src/encrypt_data.py --decrypt --infile ../data/emails.enc --outfile ../data/emails_decrypted.csv
\"\"\"

import argparse
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json

def derive_key(password: bytes, salt: bytes):
    # PBKDF2-HMAC-SHA256 -> 32 bytes key
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200000)
    return kdf.derive(password)

def encrypt_file(infile, outfile, password):
    salt = os.urandom(16)
    key = derive_key(password.encode(), salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    with open(infile, 'rb') as f:
        plaintext = f.read()
    ct = aesgcm.encrypt(nonce, plaintext, None)
    payload = {
        'salt': base64.b64encode(salt).decode(),
        'nonce': base64.b64encode(nonce).decode(),
        'ciphertext': base64.b64encode(ct).decode()
    }
    with open(outfile, 'w') as f:
        json.dump(payload, f)
    print(f'Encrypted {infile} -> {outfile}')

def decrypt_file(infile, outfile, password):
    with open(infile, 'r') as f:
        payload = json.load(f)
    salt = base64.b64decode(payload['salt'])
    nonce = base64.b64decode(payload['nonce'])
    ct = base64.b64decode(payload['ciphertext'])
    key = derive_key(password.encode(), salt)
    aesgcm = AESGCM(key)
    pt = aesgcm.decrypt(nonce, ct, None)
    with open(outfile, 'wb') as f:
        f.write(pt)
    print(f'Decrypted {infile} -> {outfile}')

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt files using AES-256-GCM.')
    parser.add_argument('--encrypt', action='store_true')
    parser.add_argument('--decrypt', action='store_true')
    parser.add_argument('--infile', required=True)
    parser.add_argument('--outfile', required=True)
    parser.add_argument('--password', required=True, help='Passphrase used to derive encryption key')
    args = parser.parse_args()

    if args.encrypt:
        encrypt_file(args.infile, args.outfile, args.password)
    elif args.decrypt:
        decrypt_file(args.infile, args.outfile, args.password)
    else:
        parser.error('Specify --encrypt or --decrypt')

if __name__ == '__main__':
    main()
