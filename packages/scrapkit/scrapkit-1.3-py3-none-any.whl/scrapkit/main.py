import requests
from bs4 import BeautifulSoup

def getTitle(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        return title
    else:
        print("Failed to fetch title. Status code:", response.status_code)
        return None

def getHTML(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch HTML content. Status code:", response.status_code)
        return None

def getText(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    else:
        print("Failed to fetch text content. Status code:", response.status_code)
        return None

def saveHTML(url, filename="output.html"):
    html_content = getHTML(url)
    if html_content:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML content saved to {filename}")
    else:
        print("Failed to save HTML content.")
