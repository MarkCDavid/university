import json
import sys
import requests

def main():
    _, subject = sys.argv
    url = "https://ca.itsm.local:8005/generate"
   
    body = json.dumps({"subject": subject})
    response = requests.post(url, body, verify=False)
    response_json = response.json()

    if not response.ok:
        raise Exception(f"Failed to generate a certificate: {response_json['reason']}")
    
    with open(f"certs/{subject}.pem", "w") as cert_file:
        cert_file.write(response_json["cert_pem"])
    
    with open(f"certs/{subject}.key", "w") as key_file:
        key_file.write(response_json["cert_recovery"])

if __name__ == "__main__":
    main()