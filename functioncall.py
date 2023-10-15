import openai
import os 

openai.api_key = "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"

# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[{"role": "system", "content": "You are a teacher teaching elementary school students math. Give easy to understand, descriptive explanations to each question."}, {"role": "user", "content": "what is 2+2?"}],
#   temperature=0,
#   max_tokens=256
# )

# print(response["choices"][0]["message"]["content"])

file1 = open('globaluserstore.txt', 'r')
userstore = file1.readlines()

messages = [{"role": "system", "content": "You are a smart personal assistant that will take in information about a user along with a query. Using the information about the user, execute the function that corresponds to the user's query."}]

for description in userstore:
    messages.append({"role": "user", "content": description})

messages.append({"role": "user", "content": "Question from user: I want to buy a sweater"})

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

print(response)
print(str(response["choices"][0]["message"]["function_call"]))
breakpoint()