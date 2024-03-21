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
            if url.startswith("localhost"):
                self.base_url = "http://" + url
            else:
                self.base_url = "https://" + url
        
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


    def news(self, args):
        # This command is used to request news stories from a web service.
        # Flag include: -id, -cat, -reg, -date
        id_flag = "*"
        cat_flag = "*"
        reg_flag = "*"
        date_flag = "*"

        # Parse the switches
        for arg in args:
            if arg.startswith("-id="):
                id_flag = arg.split("=")[1].upper()
            elif arg.startswith("-cat="):
                cat_flag = arg.split("=")[1].upper()
            elif arg.startswith("-reg="):
                reg_flag = arg.split("=")[1].upper()
            elif arg.startswith("-date="):
                date_flag = arg.split("=")[1].upper()

        # First we need to extract all news agencies in the web service
        directory_url = "https://newssites.pythonanywhere.com/api/directory/"

        try:
            response = self.session.get(directory_url)
            if response.status_code == 200:
                directory_data = response.json()
        except:
            print("Could not extract the web service news agencies")
        

        # Now we need to check which ids we want
        if id_flag != "*":
            try:
                matching_agencies = []
                
                for agency in directory_data:
                    if agency["agency_code"] == id_flag:
                        matching_agencies.append(agency)
                
                directory_data = matching_agencies
            except:
                print("Could not find matching news agencies and IDs")

        # Now that we have matching news agencies lets parse it
        # First set the url for each valid agency
        count = 0
        for agency in directory_data:
            if count < 20:
                agency_url = f"{agency["url"]}/api/stories/"
                
                params = {
                    "story_cat": cat_flag,
                    "story_region": reg_flag,
                    "story_date": date_flag
                }

                # Now that you set the url, search through it
                try:
                    response = requests.get(agency_url, params=params)
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
                        print(f"No stories found at: {agency_url}")
                    else:
                        print("Failed to get stories. Status code:", response.status_code)
                except Exception as e:
                    print("Error while getting stories:", e)

                # Only print 20 stories
                count += 1
        print("\nPrinted all storie from the first 20 news agencies\n")

    def list(self):
        # This command is used to list all news services in the directory. 
        url = "https://newssites.pythonanywhere.com/api/directory/"

        try:
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()
                agency_list = data 
                count = 0
                for agency in agency_list:
                    if count < 20:
                        print("-" * 50)
                        print(f"Agency Name: {agency.get("agency_name")}")
                        print(f"URL: {agency.get("url")}")
                        print(f"Agency Code: {agency.get("agency_code")}")
                        print("-" * 50)
                        count += 1
                print("\nListed the first 20 news agencies.\n")
            else:
                print(f"Could not list: {response.content.decode()}")
        except:
            print("A list of news agencies could not be curated.")
            


    ## This is meant to be local testing only right now
    # def get_stories(self):
    #     url = f"{self.base_url}/api/stories/" 
    #     params = {
    #         "story_cat": "*",
    #         "story_region": "*",
    #         "story_date": "*"
    #     }

    #     try:
    #         response = requests.get(url, params=params) #params=params
    #         if response.status_code == 200:
    #             stories = response.json()["stories"]
    #             for story in stories:
    #                 print("-" * 50)
    #                 print("Key:", story["key"])
    #                 print("Headline:", story["headline"])
    #                 print("Category:", story["story_cat"])
    #                 print("Region:", story["story_region"])
    #                 print("Author:", story["author"])
    #                 print("Date:", story["story_date"])
    #                 print("Details:", story["story_details"])
    #                 print("-" * 50)
    #         elif response.status_code == 404:
    #             print("No stories found.")
    #         else:
    #             print("Failed to get stories. Status code:", response.status_code)
    #     except Exception as e:
    #         print("Error while getting stories:", e)



# Make a new client when the application is ran
client = Client()

while True:
    command = input("Enter a command (login, logout, post, delete <key>), news, list: ").lower()

    if command == "login":
        client.login()
    elif command == "logout":
        client.logout()
    elif command == "post":
        client.post_story()
    elif command.startswith("delete"):
        args = command.split()
        client.delete(args[1])
    elif command.startswith("news"):
        args = command.split()[1:]
        client.news(args)
    elif command == "list":
        client.list()
    elif command == "get_stories":
        client.get_stories()
    else:
        print("Invalid command. Available commands: login, logout, post, delete <key>")
