import requests
from getpass import getpass # For secure password input

class Client:
    def __init__(self):
        self.base_url = None
        self.session = requests.Session()
        self.logged_in = False

    def login(self):

        # Check if they are already logged in first
        if self.base_url is not None:
            print("You are already logged in, logout first.")
            return()
        
        # Get a URL
        url = input("Enter the news service URL: ")
        self.base_url = url
        
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        # Set the url if http is not included, e.g. when calling localhost
        if not url.startswith("http://") and not url.startswith("https://"):
            self.base_url = "http://" + url
        
        login_url = f"{self.base_url}/api/login"

        # plaintext payload 
        payload = {
            "username": username,
            "password": password
        }

        # If current session is none reset it
        if self.session is None:
            self.session = requests.Session()

        try:
            #response = requests.post("http://localhost:8000/api/login", json=payload)
            response = self.session.post(login_url, data=payload)
            # response_data = response.json()

            # If the http response is good tell them they logged in and make a session token
            if response.status_code == 200:
                # self.session = requests.Session()
                print(response.text)
            else:
                self.base_url = None
                print(response.text)
        except Exception as e:
            self.base_url = None
            print(f"Error during login. {e}")


    def logout(self):
        if self.base_url == None:
            print("You are not logged in.")
            return()
        
        logout_url = f"{self.base_url}/api/logout"
    
        response = self.session.post(logout_url) #, headers={'Cookie': f'sessionid={self.session_cookies}'}
        # response_data = response.json()

        if response.status_code == 200:
            self.session = None
            self.base_url = None
            print(response.text)
        else:
            print(response.text)


    def post_story(self):
        if self.base_url == None:
            print("You are not logged in.")
            return()
        
        headline = input("Enter the headline: ")
        category = input("Enter the category: ")
        region = input("Enter the region: ")
        details = input("Enter the details: ")

        post_url = f"{self.base_url}/api/stories"
        post_payload = {
            'headline': headline,
            'category': category,
            'region': region,
            'details': details
        }

        try:
            response = self.session.post(post_url, json=post_payload)
            # response_data = response.json()

            if response.status_code == 201:
                print("Story posted successfully.")
            else:
                print(f"Failed to post story: {response.text}")
        except Exception as e:
            print(f"Error during post: {str(e)}")


    def delete(self, key):
        if self.base_url == None:
            print("You are not logged in.")
            return() 
        
        # Convert key to an int
        try:
            key = int(key)
        except ValueError:
            print("Invalid story key. Please provide a valid integer.")
            return()
        
        delete_url = f"{self.base_url}/api/stories/{key}" 
        
        try:
            response = self.session.delete(delete_url)

            if response.status_code == 200:
                print("Story deleted successfully.")
            else:
                print(f"Failed to delete story: {response.text}")
        except Exception as e:
            print(f"Error during delete: {str(e)}")



    def get_stories(self):
        url = "http://localhost:8000/api/stories/"  # Replace "your-api-url" with the actual URL of your API
        params = {
            "story_cat": "*",
            "story_region": "*",
            "story_date": "*"
        }

        try:
            response = requests.get(url, params=params) #params=params
            if response.status_code == 200:
                stories = response.json()["stories"]
                for story in stories:
                    print("-" * 50)
                    print("Key:", story["key"])
                    print("Headline:", story["headline"])
                    print("Category:", story["story_cat"])
                    print("Region:", story["story_region"])
                    print("Author:", story["author"])
                    print("Date:", story["story_date"])
                    print("Details:", story["story_details"])
                    print("-" * 50)
            elif response.status_code == 404:
                print("No stories found.")
            else:
                print("Failed to get stories. Status code:", response.status_code)
        except Exception as e:
            print("Error while getting stories:", e)



# Make a new client when the application is ran
client = Client()

while True:
    command = input("Enter a command (login, logout, post, delete <key>): ").lower()

    if command == "login":
        client.login()
    elif command == "logout":
        client.logout()
    elif command == "post":
        client.post_story()
    elif command.startswith("delete"):
        split = command.split()
        client.delete(split[1])
    elif command == "get_stories":
        client.get_stories()
    else:
        print("Invalid command. Available commands: login, logout, post, delete <key>")
