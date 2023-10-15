from flask import Flask, request, jsonify
import openai
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import difflib
from bs4 import BeautifulSoup
import os
# openai.api_key = ""
openai.api_key =  ""
sample_url = 'https://www.walmart.com/ip/Grianlook-Mens-Fashion-Waffle-T-Shirts-Henley-Neck-Solid-Color-Pullover-Work-Long-Sleeve-T-shirt-Red-wine-2XL/1000446518'

app = Flask(__name__)

url_counter = 0
url1 = None
url2 = None

def get_HTML(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the entire HTML as a string
    html = str(soup)
    # print("HTML: "  + html)
    return html.splitlines()

@app.route('/')
def hello_world():
    return 'Hello, World!'

def get_preference(url_before, url_preference):
    print("url before: " + str(url_before))
    print("url after: " + str(url_preference))
    response_before = requests.get(url_before)
    response_preference = requests.get(url_preference)

    # Ensure the request was successful
    if response_before.status_code == 200:
        # Parse the HTML of the page with BeautifulSoup
        soup = BeautifulSoup(response_before.text, 'html.parser')
        # Get the entire HTML as a string
        html_before = str(soup)
        # print("html_before: ", html_before.splitlines()[0])
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

    open('file.txt', 'w').close()

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

    return str(option_list)

def get_diff(html1, html2): 
    # Find and print the diff:
    for line in difflib.unified_diff(
            html1, html2, lineterm=''):
        f = open("diff.txt", "a")
        f.write(line)
        f.close()

    with open('diff.txt') as diff_file:
        diff_file_text = diff_file.readlines()

    print("test 1 ")
    # open('diff.txt', 'w').close()

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

    print("OPTION LEGNTH: " + str(option_list))
    return str(option_list)

import requests

import json


def extract_characteristic(data):
    # data = request.get_json()  # Assuming the request contains JSON data
    openai.api_key =  ""
    print("begin call")

    response_step_1 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[{"role": "system", "content": "You are a computer scientist that is really good that explaining code in natural language."},
                {"role": "user", "content": "A person is looking to purchase something on a website. This is a diff file between before and after choosing preferences for the purchase. Can you tell me 2 things: the first is what the name of the item the user is trying to buy and second, the details about the users preference all in one line output: \n" + str(data)}],
    temperature=0,
    max_tokens=256
    )

    print("end call ")
    # print(response["choices"][0]["message"]["content"])
    input_sentence = response_step_1["choices"][0]["message"]["content"]

    print("INPUT SENTENCE: " + str(input_sentence))

    response_step_2 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "A user has interacted with a website. Give a description of this interaction on the website, write a short single-sentence statement about the user that describes their preferences and interests."},
                {"role": "user", "content": "This is the sentence describing the interaction: " + input_sentence}],
    temperature=0,
    max_tokens=512
    )

    user_descriptor = response_step_2["choices"][0]["message"]["content"]
    file1 = open("globaluserstore.txt", "a")  # append mode
    file1.write(user_descriptor + "\n")
    file1.close()

@app.route('/set_url', methods=['POST'])
def set_url():
    global url_counter
    global url1
    global url2
    data = request.get_json()  # Assuming the request contains JSON data
    
    url_HTML = data['url']
    if url_counter == 0:
        # url1 = get_HTML(url_HTML)
        url1 = url_HTML
        url2 = None
        url_counter = 1
    else:
        # url2 = get_HTML(url_HTML)
        url2 = url_HTML
        url_counter = 0

    if ((url1 != None) and (url2 != None)):
        print("starting diff")
        # diff = get_diff(url1, url2)
        diff = get_preference(url1, url2)
        print("get diff")
        extract_characteristic(diff)
        print("what?")
        return jsonify({"message": "set both URLs, updated the user store"})
    else:
        return jsonify({"message": "set URL 1"})
    

@app.route('/query', methods=['POST'])
def query():
    openai.api_key =  ""

    data = request.get_json()  # Assuming the request contains JSON data
    
    query = data['query']
    file1 = open('globaluserstore.txt', 'r')
    userstore = file1.readlines()
    messages = [{"role": "system", "content": "You are a smart personal assistant that will take in information about a user along with a query. Using the information about the user, execute the function that corresponds to the user's query."}]

    for description in userstore:
        messages.append({"role": "user", "content": description})

    messages.append({"role": "user", "content": "Question from user: " + query})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=[
        {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
            },
            "required": ["location"]
        }
        },
        {
        "name": "book_flight",
        "description": "Book a flight between two cities",
        "parameters": {
            "type": "object",
            "properties": {
            "first_city": {
                "type": "string",
                "description": "The city from which the flight will be departing"
            },
            "second_city": {
                "type": "string",
                "description": "The city to which the flight will be arriving"
            }
            },
            "required": ["first_city", "second_city"]
        }
        },
        {
        "name": "buy",
        "description": "Buy a product online for the user",
        "parameters": {
            "type": "object",
            "properties": {
            "object": {
                "type": "string",
                "description": "The object the user wants to buy. i.e. pants, shirt, plates, utensils, laptop, etc."
            },
            "size": {
                "type": "string",
                "description": "Size of the object that needs to be bought. i.e. small, medium, large"
            },
            "color": {
                "type": "string",
                "description": "Color of the object that needs to be bought"
            }
            },
            "required": ["object"]
        }
        }
        ],
        temperature=0,
        max_tokens=512
    )
    output_str = str(response["choices"][0]["message"]["function_call"])
    return jsonify({"output": output_str})

if __name__ == '__main__':
    app.run(debug=True)
