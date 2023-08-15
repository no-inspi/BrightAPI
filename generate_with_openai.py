import os
import openai
from decouple import config
import time
import fileinput

from pathlib import Path
import json

# time.sleep(1)

openai.api_key = config("OPENAI_API_KEY")

def get_categorie_for_openai():
  with open('categories.txt') as f:
    lines = f.readlines()


  return lines

def write_idea_to_file(ideas):
  f = open("idea_end.txt", "a")
  for idea in ideas:
    idea = idea+"\n"
    f.writelines(idea)

  f.close()

def get_response_from_openai(input):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=input,
    temperature=0.6,
    max_tokens=150,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=1
  )
  try:
    return response.choices[0].text
  except:
    return "error"


def delete_empty_line():
  with open("idea_end.txt", 'r') as r, open('idea_end_withoutblank.txt', 'w') as o:
    for line in r:
        #strip() function
        if line.strip():
            o.write(line)

def clean_file(filename):
  all_lines = []
  with open(filename) as f:
    lines = f.readlines()


  for line in lines:
    line = line.split(" ",1)
    all_lines.append(line[1])
  
  return all_lines


def get_idea_from_categories():
  resp_list = []

  categories = get_categorie_for_openai()
  for category in categories:
    time.sleep(5)
    input = "List of idea about "+category
    print(input)
    resp = get_response_from_openai(input)
    resp_list.append(resp)
  write_idea_to_file(resp_list)
  delete_empty_line()


def generate_image(description):
  
  print(description)
  openai.api_key = config("OPENAI_API_KEY")

  response = openai.Image.create(
      prompt=description,
      n=1,
      size="512x512",
      # response_format="b64_json",
  )

  return response['data'][0]['url']
  
# get_idea_from_categories()
# clean_file('idea_end_withoutblank.txt')