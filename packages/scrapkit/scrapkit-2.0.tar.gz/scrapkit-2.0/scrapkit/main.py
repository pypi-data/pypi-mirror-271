import requests
from bs4 import BeautifulSoup
import json

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
    
def getMetaTags(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tags = soup.find_all('meta')
        return meta_tags
    else:
        print("Failed to fetch meta tags. Status code:", response.status_code)
        return None

def getTextFromElement(url, element_tag):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(element_tag)
        text_list = [element.text for element in elements]
        return '\n'.join(text_list)
    else:
        print(f"Failed to fetch text from elements '{element_tag}'. Status code:", response.status_code)
        return None

def getDataTables(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        data = []
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                row_data = [col.text.strip() for col in cols]
                data.append(row_data)
        return data
    else:
        print("Failed to fetch data tables. Status code:", response.status_code)
        return None

def getJsonData(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            json_data = json.loads(response.text)
            return json_data
        except json.JSONDecodeError as e:
            print("Failed to parse JSON data:", e)
            return None
    else:
        print("Failed to fetch JSON data. Status code:", response.status_code)
        return None

def saveJson(json_data, filename="output.json"):
    if json_data:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4)
        print(f"JSON data saved to {filename}")
    else:
        print("No JSON data to save.")


