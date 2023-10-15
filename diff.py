import difflib
import requests
from bs4 import BeautifulSoup
import openai
import os


def get_preference(url_before, url_preference):


    response_before = requests.get(url_before)
    response_preference = requests.get(url_preference)

    # Ensure the request was successful
    if response_before.status_code == 200:
        # Parse the HTML of the page with BeautifulSoup
        soup = BeautifulSoup(response_before.text, 'html.parser')
        # Get the entire HTML as a string
        html_before = str(soup)
        print("html_before: ", html_before.splitlines()[0])
        f = open("html_before.txt", "w")
        f.write(html_before)
        f.close()

    if response_preference.status_code == 200:
        # Parse the HTML of the page with BeautifulSoup
        soup = BeautifulSoup(response_preference.text, 'html.parser')
        # Get the entire HTML as a string
        html_preference = str(soup)
        f = open("html_preference.txt", "w")
        f.write(html_preference)
        f.close()

    with open('html_before.txt') as file_1:
        file_1_text = file_1.readlines()

    with open('html_preference.txt') as file_2:
        file_2_text = file_2.readlines()

    # Find and print the diff:
    for line in difflib.unified_diff(
            file_1_text, file_2_text, lineterm=''):
        f = open("diff.txt", "a")
        f.write(line)
        f.close()

    with open('diff.txt') as diff_file:
        diff_file_text = diff_file.readlines()

    i = 0
    start = 0
    found_start = False
    end = 0

    option_list = []
    found_title = False
    option_list.append(diff_file_text[0:1])
    while i < len(diff_file_text):
        if "<option" in diff_file_text[i]:
            option_list.append(diff_file_text[i:i+2])
        if  "<title" in diff_file_text[i] and found_title == False:
            option_list.append(diff_file_text[i:i+2])
            found_title = True
        i+=1

    print("option_list: ", len(option_list))
    count = 0
    for i in range(len(option_list)):
        print("option_list[i]: ", option_list[i])
        for k in range(len(option_list[i])):
            count+=len(option_list[i][k])
    print("count: ", count)
    openai.api_key = "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"

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[{"role": "system", "content": "You are a computer scientist that is really good that explaining code in natural language."},
                {"role": "user", "content": "A person is looking to purchase something on a website: " + str(url_preference) + "This is a diff file between before and after choosing preferences for the purchase. Can you tell me 2 things: the first is what the name of the item the user is trying to buy and second, the details about the users preference all in one line output: \n" + str(option_list)}],
    temperature=0,
    max_tokens=256
    )
    print("response['usage']['total_tokens']: ", response['usage']['total_tokens'])

    return response["choices"][0]["message"]["content"]


url_before = 'https://www.etsy.com/listing/1421206271/neon-shadow-block-embroidered-monogram?ref=cat_attribute_module_four_panel_378_2551'
url_preference = 'https://www.etsy.com/listing/1421206271/neon-shadow-block-embroidered-monogram?ref=cat_attribute_module_four_panel_378_2551&variation0=3256196774&variation1=3270581417'

preference = get_preference(url_before, url_preference)
print(f"Given url before: {url_before} and url with preferences chosen: {url_preference}")
print("The user preference is: ", preference)