import json
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from nltk.corpus import stopwords
from collections import Counter
import pprint

def get_base_url(url):
    parts = url.split('/')
    return '/'.join(parts[:3])

def crawl_website(url, max_pages=None):
    base_url = get_base_url(url)
    visited_urls = set()
    inverted_index = {}
    total_pages = 0

    # Download NLTK stopwords
    stop_words = set(stopwords.words('english'))

    def scrape_page(current_url):
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                print("Scraping:", current_url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract quote texts
                quote_texts = [quote.text.strip() for quote in soup.find_all('span', class_='text')]
                update_index(quote_texts, current_url)

                # Extract tags information
                tags = [tag.text for tag in soup.find_all('a', class_='tag')]
                update_index(tags, current_url)

                # Extract author description if available
                author_description = soup.find('div', class_='author-description')
                if author_description:
                    description_text = author_description.text.strip()
                    update_index([description_text], current_url)

                # Extract links from the page
                links = [urljoin(current_url, link['href']) for link in soup.find_all('a', href=True)]
                return links
            else:
                print(f"Error: Failed to fetch {current_url}. Status code: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error: {e}")
            return []

    def update_index(texts, url):
        for text in texts:
            # Tokenize the text
            words = re.findall(r'\w+', text.lower())
            # Filter out stop words using NLTK stopwords
            words = [word for word in words if word not in stop_words]

            # Update the inverted index
            for word in words:
                if word not in inverted_index:
                    inverted_index[word] = {}
                if url not in inverted_index[word]:
                    inverted_index[word][url] = 1
                else:
                    inverted_index[word][url] += 1

    queue = [url]
    while queue and (max_pages is None or total_pages < max_pages):
        current_url = queue.pop(0)
        if current_url not in visited_urls and get_base_url(current_url) == base_url:
            links = scrape_page(current_url)
            queue.extend(links)
            total_pages += 1

    print("\nTotal pages crawled:", total_pages)
    return inverted_index

def save_index_to_file(index, filename):
    with open(filename, 'w') as f:
        json.dump(index, f, indent=3)
    print(f"Inverted index saved to {filename}")

def build():
    website_url = "https://quotes.toscrape.com/"
    print(f"Crawling {website_url}...")
    inverted_index = crawl_website(website_url)
    if inverted_index:
        save_index_to_file(inverted_index, "inverted_index.json")
        return inverted_index
    else:
        print("Error: Failed to create inverted index.")
        return None
    


### Load index
def load_index(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None


### Print index
def print_index(word):
    word = word.lower()
    try:
        for value in inverted_index:
            if value == word:
                pprint.pp(inverted_index[value])
                return
        print ("Word not found")
    except Exception as e:
        if inverted_index == None:
            print("Load the list first!")
        else:
            print("Error printing: ", e)

# Command line client
inverted_index = None
while True:
    command = input("Enter a command (build, load, print <word>, find <phrase>): ").lower()

    if command == "build":
        inverted_index = build()
    elif command == "load":
        inverted_index = load_index("inverted_index.json")
        if inverted_index:
            print("Inverted index loaded successfully.")
    elif command.startswith("print"):
        args = command.split()
        if len(args) < 2:
            print("Missing arguments for print command.")
        else:
            print_index(args[1])
    elif command.startswith("find"):
        args = command.split()
        if len(args) < 2:
            print("Missing arguments for find command.")
        else:
            #find_pages(args[1])
            pass
    elif command == "exit":
        print("Exiting search tool.")
        break
    else:
        print("Invalid command. Available commands: build, load, print <word>, find <phrase>")