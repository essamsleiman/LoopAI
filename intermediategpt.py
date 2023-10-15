import openai
import os

openai.api_key = "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"

input_sentence = 'The changes in the HTML code reflect the users preference for selecting the "Neon Pink" option in the first variation and the "Medium" option in the second variation on the Etsy website.'

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "system", "content": "A user has interacted with a website. Give a description of this interaction on the website, write a short single-sentence statement about the user that describes their preferences and interests."},
            {"role": "user", "content": "This is the sentence describing the interaction: " + input_sentence}],
  temperature=0,
  max_tokens=512
)

print(response["choices"][0]["message"]["content"])