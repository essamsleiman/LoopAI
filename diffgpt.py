import openai
import os

openai.api_key = "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"

with open('diff_short.txt','r') as file:
    text = " ".join(line.rstrip() for line in file)

print(len(text))
print(text[:100])

response_step_1 = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "system", "content": "You are a computer scientist that is really good that explaining code in natural language."},
            {"role": "user", "content": "Please read a diff between two HTML files of a website and output one sentence that describes how these changes reflect a user's preferences. In addition to the diff, you are provided information about the website"},
            {"role": "user", "content": "Info about website: Etsy is a shopping website with clothes and jewelery."},
            {"role": "user", "content": "This is the diff: " + text}],
  temperature=0,
  max_tokens=512
)

# print(response["choices"][0]["message"]["content"])
input_sentence = response_step_1["choices"][0]["message"]["content"]

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
breakpoint()