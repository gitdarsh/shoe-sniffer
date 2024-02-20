import requests
from bs4 import BeautifulSoup
import csv

def scrape_stockx_data(page_number):
    url = f'https://stockx.com/sneakers?page={page_number}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.146 (Edition BRAVE) CryptoChrome/91.0.4472.124',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting sneaker names and images
        sneaker_info = []

        for product in soup.select('.css-tkc8ar'):
            image = product.find('img')
            if image:
                name = image.get('alt', 'No Name')
                image_url = image.get('src', '')

                sneaker_info.append({'name': name, 'image_url': image_url})

        return sneaker_info
    else:
        print(f"Failed to retrieve data from page {page_number}. Status code: {response.status_code}")
        return None

def save_to_csv(data, filename='sneaker_data.csv'):
    fieldnames = ['name', 'image_url']

    with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if csv_file.tell() == 0:  # Write header only if the file is empty
            writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    total_pages = 5  # Set the number of pages you want to scrape

    for page_number in range(1, total_pages + 1):
        data = scrape_stockx_data(page_number)

        if data:
            save_to_csv(data)
            print(f"Data from page {page_number} saved to sneaker_data.csv")
