import requests
from bs4 import BeautifulSoup

# URL of the website
url = 'https://www.kayak.com/flights/SFO-LAX/2023-11-13/2023-11-20?sort=duration_a&fs=stops=-0'

# Send a GET request
response = requests.get(url)

# Ensure the request was successful
if response.status_code == 200:
    # Parse the HTML of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the entire HTML as a string
    html = str(soup)

    # Do something with the HTML, or just print it
    f = open("kayak.txt", "a")
    f.write(html)
    f.close()
else:
    print("Failed to retrieve the page")
