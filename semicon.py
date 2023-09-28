import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_exhibitor_details(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Assuming the data is structured in a way that it can be easily located
    seat = soup.find('div', {'class': 'seat-info'}).text.strip()
    overview = soup.find('div', {'class': 'overview'}).text.strip()
    product = soup.find('div', {'class': 'product'}).text.strip()
    return seat, overview, product

def main():
    url = 'https://expo.semi.org/china2023/public/exhibitors.aspx?&langID=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    exhibitor_data = []

    # Assuming the exhibitors are listed in a table
    exhibitors = soup.find_all('tr', {'class': 'exhibitor'})
    for exhibitor in exhibitors:
        name = exhibitor.find('td', {'class': 'name'}).text.strip()
        link = exhibitor.find('a')['href']
        seat, overview, product = get_exhibitor_details(link)
        exhibitor_data.append({
            'Name': name,
            'Seat': seat,
            'Overview': overview,
            'Product': product
        })

    # Create DataFrame
    df = pd.DataFrame(exhibitor_data)

    # Save to CSV
    df.to_csv('semiconlist.csv', index=False)

if __name__ == '__main__':
    main()
