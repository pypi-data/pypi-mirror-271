# webscraper.py

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

def getLinks(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a')]
        return links
    else:
        print("Failed to fetch links. Status code:", response.status_code)
        return None

def getImageUrls(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_urls = [img.get('src') for img in soup.find_all('img')]
        return img_urls
    else:
        print("Failed to fetch image URLs. Status code:", response.status_code)
        return None

def getElementByClass(url, class_name):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_=class_name)
        return elements
    else:
        print(f"Failed to fetch elements with class '{class_name}'. Status code:", response.status_code)
        return None

def getElementById(url, id_name):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(id=id_name)
        return element
    else:
        print(f"Failed to fetch element with id '{id_name}'. Status code:", response.status_code)
        return None

def submitForm(url, form_data):
    response = requests.post(url, data=form_data)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to submit form. Status code:", response.status_code)
        return None

def clickButton(url, button_id):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        button = form.find('button', id=button_id)
        action_url = form.get('action')
        button_data = {button.get('name'): button.get('value')}
        response = requests.post(action_url, data=button_data)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to click button. Status code:", response.status_code)
            return None
    else:
        print("Failed to fetch webpage. Status code:", response.status_code)
        return None
