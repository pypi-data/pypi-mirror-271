#!/usr/bin/env python
import os
from uuid import uuid4

import requests
from openai import OpenAI


def generate_and_save_image(prompt, folder_path='./users/BOTRUN_FOLDER/img/'):
    client = OpenAI()
    image_response = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", quality="hd", n=1)
    image_url = image_response.data[0].url
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_data = requests.get(image_url).content
    file_name = f'{folder_path}2024-05-05_{uuid4()}.png'
    with open(file_name, 'wb') as file:
        file.write(image_data)
    print(f'Image saved as {folder_path}{file_name}')
