import requests
from bs4 import BeautifulSoup

# URL of the website
url = 'https://www.kayak.com/flights/SFO-LAX/2023-11-13/2023-11-20?sort=duration_a&fs=stops=-0'
url = 'https://www.etsy.com/search//home-and-living/kitchen-and-dining?q=decor&anchor_listing_id=1306400398&ref=hp_bubbles_sitewidepromo_10_23_freeshipping&mosv=sese&moci=1182317107864&mosi=1204694250525&is_merch_library=true&free_shipping=true'

# Send a GET request
response = requests.get(url)

# Ensure the request was successful
if response.status_code == 200:
    # Parse the HTML of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the entire HTML as a string
    html = str(soup)

    # Do something with the HTML, or just print it
    f = open("etsy.txt", "a")
    f.write(html)
    f.close()
else:
    print("Failed to retrieve the page")
