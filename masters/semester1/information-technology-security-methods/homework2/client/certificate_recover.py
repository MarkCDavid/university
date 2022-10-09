import json
import sys
import requests
from os.path import exists

def load_key(subject: 'str'):
    key_path = f"certs/{subject}.key"
    if not exists(key_path):
        raise Exception(f"Key file \"{key_path}\" for \"{subject}\" does not exist!")

    with open(key_path, "rb") as key_file:
        return key_file.read().decode("utf-8")

def main():
    _, subject = sys.argv
    url = "http://localhost:8005/recover"

    key = load_key(subject)

    body = json.dumps({"subject": subject, "key": key})
    response = requests.post(url, body)
    response_json = response.json()
    
    if not response.ok:
        raise Exception(f"Failed to recover a certificate: {response_json['reason']}")
    
    with open(f"certs/{subject}.pem", "w") as cert_file:
        cert_file.write(response_json["cert_pem"])
    
    with open(f"certs/{subject}.key", "w") as key_file:
        key_file.write(response_json["cert_recovery"])

if __name__ == "__main__":
    main()