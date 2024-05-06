import os
from uuid import uuid4

import dotenv
import requests
from openai import OpenAI

dotenv.load_dotenv()
from datetime import date


def dalle_gen_save(prompt, folder_path='./users/BOTRUN_FOLDER/img/'):
    client = OpenAI()
    image_response = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", quality="hd", n=1)
    image_url = image_response.data[0].url
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_data = requests.get(image_url).content
    today = date.today()
    today_date_string = today.strftime("%Y-%m-%d")
    file_name = f'{folder_path}{today_date_string}_{uuid4()}.png'
    with open(file_name, 'wb') as file:
        file.write(image_data)
    return file_name


def main():
    dalle_gen_save('一隻可愛貓咪與絢麗場景')


if __name__ == '__main__':
    main()
