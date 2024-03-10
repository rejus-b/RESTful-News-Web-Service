import requests
from getpass import getpass # For secure password input

class Client:
    def __init__(self):
        self.base_url = None
        self.session = None

    def login(self, url):
        self.base_url = url
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        # Set the url if http is not included, e.g. when calling localhost
        if not url.startswith("http://") and not url.startswith("https://"):
            self.base_url = "http://" + url
        
        login_url = f"{self.base_url}/api/login"

        # JSON payload 
        payload = {
            "username": username,
            "password": password
        }

        try:
            #response = requests.post("http://localhost:8000/api/login", json=payload)
            response = requests.post(login_url, json=payload)
            response_data = response.json()

            # If the http response is good tell them they logged in and make a session token
            if response.status_code == 200:
                self.session = requests.Session()
                print(response_data.get("message"))
            else:
                print(response_data.get("message"))
        except Exception as e:
            print("Error during login.")


    def logout(self):
        if self.session == None:
            print("You are not logged in.")
            return()
        
        logout_url = f"{self.base_url}/api/logout"
    
        response = self.session.post(logout_url)
        response_data = response.json()

        if response.status_code == 200:
            self.session = None
            print(response_data.get("message"))
        else:
            print(response_data.get("message"))


# Make a new client when the application is ran
client = Client()

while True:
    command = input("Enter a command (login, logout): ").lower()

    if command == "login":
        url = input("Enter the news service URL: ")
        client.login(url)
    elif command == "logout":
        client.logout()
    else:
        print("Invalid command. Available commands: login, logout")
