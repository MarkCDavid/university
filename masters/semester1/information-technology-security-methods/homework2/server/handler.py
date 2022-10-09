from sqlite3 import connect
import ssl
from typing import List, Tuple
import os


class Handler:
    
    def __init__(self, subject: 'str', connection: 'ssl.SSLSocket', address: 'Tuple[str, int]'):
        self.subject = subject
        self.connection = connection
        self.address = address
        self.finished = False

        self.connection.write(f"Connected as \"{subject}\"!".encode("utf-8"))

        if not os.path.exists(self.subject):
            os.mkdir(self.subject)
        
    def is_finished(self) -> 'bool':
        return self.finished

    def parse(self, data: 'str'):
        data = data.split(' ')
        return data[0], data[1:]

    def handle(self, data):
        command, arguments = self.parse(data)
        function = f"handler_{command}"
        if not hasattr(self, function):
            self.handler_no_function(command)
            return
        
        getattr(self, function)(arguments)

    def handler_no_function(self, command: 'str'):
        self.connection.write(f"Command \"{command}\" not found!".encode("utf-8"))

    def handler_exit(self, arguments: 'List[str]'):
        self.connection.close()
        self.finished = True
        print(f"Connection closed by \"{self.address[0]}:{self.address[1]}\"")

    def handler_write(self, arguments: 'List[str]'):
        if len(arguments) != 2:
            self.connection.write(f"Usage: \"write\" <filename> <contents>".encode("utf-8"))
            return

        filename = arguments[0]
        contents = arguments[1]

        with open(f"{self.subject}/{filename}", "w") as file:
            file.write(contents)

        self.connection.write(f"Successfully written file {filename}".encode("utf-8"))
        print(f"Writing file {filename} for {self.subject}")

    def handler_list(self, arguments: 'List[str]'):
        files = '\n'.join(os.listdir(self.subject))
        self.connection.write(f"Files:\n{files}".encode("utf-8"))
        print(f"Showing files for {self.subject}")

    def handler_read(self, arguments: 'List[str]'):
        if len(arguments) != 1:
            self.connection.write(f"Usage: \"read\" <filename>".encode("utf-8"))
            return

        filename = arguments[0]
        path = f"{self.subject}/{filename}"


        if not os.path.exists(path):
            self.connection.write(f"File \"{filename}\" does not exist!".encode("utf-8"))
            return

        with open(path, "r") as file:
            contents = file.read()

        self.connection.write(contents.encode("utf-8"))