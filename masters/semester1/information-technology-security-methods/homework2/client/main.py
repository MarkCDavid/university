import sys
from os.path import exists
from itsmsocket import Socket

def load_certificate(subject: 'str'):
    cert_path = f"certs/{subject}.pem"
    if not exists(cert_path):
        raise Exception(f"Certificate for \"{subject}\" does not exist!")

    with open(cert_path, "rb") as cert_file:
        return cert_file.read().decode("utf-8")

def parse_argv():
    subject, hostname, port = None, "localhost", 8006

    if len(sys.argv) > 1:
        subject = sys.argv[1]

    if len(sys.argv) > 2:
        hostname = sys.argv[2]

    if len(sys.argv) > 3:
        port = sys.argv[3]

    return subject, hostname, port

def main():
    subject, hostname, port = parse_argv()
    certificate = load_certificate(subject)

    with Socket(certificate, hostname, port) as _socket:
        while True:
            _input = input(f"{subject} $ ")
            _socket.send(_input)

            if _input.strip() == "exit":
                return

            rows = _socket.receive()
            for row in rows.split('\n'):
                print("server >", row)

if __name__ == "__main__":
    main()